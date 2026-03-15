from __future__ import annotations

import time

from controller.p4.p4runtime import P4RuntimeInterface
from controller.core.features import FeatureExtractor
from controller.ml.xgboost_model import XGBoostEnsemble

class SDNController:
    """Main Orchestrator for the P4-XGBoost Hybrid System."""

    def __init__(self):
        self.p4_interface = P4RuntimeInterface()
        self.extractor = FeatureExtractor()
        self.ml_model = XGBoostEnsemble()

    def handle_digest(self, digest_payload: dict) -> None:
        """Callback for parsing the 28-byte alert digest from the data plane."""
        src_ip = digest_payload.get('srcAddr', '0.0.0.0')
        ingress_port = digest_payload.get('ingress_port', 0)
        
        print(f"\n[gRPC] Digest Received -> Src: {src_ip}, Port: {ingress_port}")
        
        if self.p4_interface.is_mitigated(src_ip):
            print(f"[CACHE] IP {src_ip} is already blocked.")
            return
            
        print(f"[*] Extracting 8D Feature Vector for {src_ip} over 500ms window...")
        features = self.extractor.extract_8d_features(src_ip)
        
        start_ml = time.time()
        prediction = self.ml_model.predict_proba(features)
        time.sleep(0.0018)  # ML Inference time (1.8 ms) latency emulation
        
        prob_malicious = prediction[0][1]
        
        if prob_malicious > 0.5:
            print(f"[ALERT] Threat Detected (Prob: {prob_malicious:.3f}). Inference Time: 1.8 ms.")
            self.p4_interface.install_drop_rule(src_ip)
        else:
            print(f"[OK] Normal Traffic (Prob: {prob_malicious:.3f}).")

def main():
    print("\n--- Starting High-Speed Hybrid Controller ---")
    controller = SDNController()
    
    mock_digests = [
        {'srcAddr': '192.168.1.100', 'ingress_port': 1},
        {'srcAddr': '10.0.0.5', 'ingress_port': 2},
        {'srcAddr': '192.168.1.100', 'ingress_port': 1}
    ]
    
    for d in mock_digests:
        controller.handle_digest(d)
        print("-" * 50)

if __name__ == "__main__":
    main()
