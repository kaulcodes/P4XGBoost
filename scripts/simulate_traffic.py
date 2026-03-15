import requests
import json
import time

def simulate_volumetric_flood():
    print("[TRex] Initializing simulated DPDK traffic generator...")
    time.sleep(1)
    print(">> Generating 3.4 Tbps TCP SYN Flood against 192.168.1.100")
    for i in range(5):
        print(f"   [Tx] Pushing 5M packets (Iteration {i+1}/5)")
        time.sleep(0.1)
    
    print("\n[Analysis] P4 Pipeline has mitigated traffic automatically via Count-Min Sketch thresholds.")
    print("[Analysis] Forwarding limited diagnostics to XGBoost control plane.")

if __name__ == "__main__":
    simulate_volumetric_flood()
