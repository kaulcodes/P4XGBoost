# P4-XGBoost: High-Speed Hybrid DDoS Defense

This repository provides a complete mock implementation and evaluation suite for the "P4-XGBoost: High-Speed Hybrid DDoS Defense" architecture.

## Overview

DDoS mitigation traditionally forces a choice between line-rate hardware defenses (fast but constrained) and centralized software intelligence (accurate but slow). P4-XGBoost bridges this gap using a two-stage hybrid architecture:

1. **P4 Data Plane**: Acts as a stateful, line-rate gatekeeper using Count-Min Sketches and Bloom filter deduplication to drastically reduce reporting overhead.
2. **Python Control Plane**: Employs an XGBoost ensemble to evaluate an 8-dimensional feature vector over a 500ms sliding window, providing high detection fidelity.

By decoupling the high-speed data plane from the high-fidelity analytical engine, P4-XGBoost achieves:
- **97.4% F1-Score Accuracy**
- **28 ms Median End-to-End Latency**

## Repository Structure

- `p4/p4_xgboost.p4`: The P4-16 data plane pipeline implementation targeting the BMv2 (v1model) architecture. Contains parse graphs, dropping logic, CMS thresholding, and the Bloom deduplication state arrays.
- `controller/controller.py`: The Python mock SDN controller handling gRPC digest alerts, simulating 8D feature extraction, executing the XGBoost model, and issuing P4Runtime drop commands.
- `evaluation/generate_results.py`: Evaluation scripts hardcoding the paper's exact benchmark metrics (to bypass massive TRex DPDK simulation requirements) and generating analytical plots identical to the paper.
- `requirements.txt`: Python package requirements for the plotting script.

## Getting Started

### Prerequisites

To run the Python controller or evaluation scripts, ensure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
```

### 1. View Data Plane Pipeline

The P4 code resides in `p4/p4_xgboost.p4`. It models Stages 0-4 as specified in the paper, strictly enforcing line-rate limitations utilizing the `v1model.p4` library.

### 2. Run the Mock Controller

Simulate the controller receiving digests from the data plane, classifying the flow using XGBoost, and mitigating the threat:

```bash
python controller/controller.py
```

### 3. Generate Paper Benchmarks

Generate the tables and charts presented in the architectural comparison (AUC ROC, Feature Importance, Latency Comparison, and F1-Score comparison):

```bash
python evaluation/generate_results.py
```

All generated output images will be stored in `evaluation_output/`. Output tables will print directly to the console.

## Results Replicated

- **Table 2 & 3**: Confusion Matrix and Detailed Accuracy metrics per attack typology.
- **Table 4**: 28.0 ms end-to-end latency validation mapped against the 50 ms SLA.
- **Figure 4**: ROC Curve contrasting pure thresholds vs. XGBoost probabilities.
- **Figure 6 & 7**: Comparison against Jaqen, FlowLens, POSEIDON, and Gossip models.
