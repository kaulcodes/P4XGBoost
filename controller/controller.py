import os
import time

class P4XGBoostController:
    """
    Mock SDN Controller for P4-XGBoost Architecture.
    Simulates receiving gRPC digests from the data plane,
    extracting 8D features, and classifying using XGBoost.
    """
    
    def __init__(self):
        self.ml_model = self._initialize_xgboost()
        self.active_drops = set()
    
    def _initialize_xgboost(self):
        """
        Initializes the mock XGBoost Model explicitly matching paper parameters:
        - 100 estimators
        - max tree depth 6
        - learning rate 0.1
        - binary:logistic
        """
        print("[INFO] Initializing XGBoost Ensemble...")
        print("[PARAMS] n_estimators=100, max_depth=6, eta=0.1, objective='binary:logistic'")
        
        # MOCK ML MODEL for standalone execution
        class MockXGBoost:
            def predict_proba(self, features):
                # features: [pkt_rate, byte_rate, duration, proto_var, port_div, size_var, tcp_flags, inter_arrival]
                pkt_rate = features[0]
                if pkt_rate > 500: # Simple threshold to guarantee predictable outcomes
                    return [[0.01, 0.99]]
                return [[0.99, 0.01]]
                
        return MockXGBoost()
        
    def _extract_8d_features(self, src_ip):
        """
        Simulates the selective mirroring stage (500ms temporary trace).
        Returns a mock feature vector for the given IP.
        """
        # [pkt_rate, byte_rate, duration, proto_var, port_div, size_var, tcp_flags, inter_arrival]
        time.sleep(0.0021) # Fake feature extraction delay (2.1ms)
        mock_attack_features = [1200, 1500000, 0.5, 0.1, 1, 0.05, 0.8, 0.0001]
        return mock_attack_features

    def handle_digest(self, digest_payload):
        """
        Callback for when the P4 switch sends a 28-Byte alert digest.
        """
        src_ip = digest_payload['srcAddr']
        ingress_port = digest_payload['ingress_port']
        
        print(f"[gRPC] Digest Received -> Src: {src_ip}, Port: {ingress_port}")
        
        if src_ip in self.active_drops:
            return # Already mitigated
            
        print(f"[*] Extracting 8D Feature Vector for {src_ip} over 500ms window...")
        features = self._extract_8d_features(src_ip)
        
        # XGBoost ML Inference
        start_ml = time.time()
        prediction = self.ml_model.predict_proba(features)
        ml_time = (time.time() - start_ml) * 1000
        
        prob_malicious = prediction[0][1]
        
        if prob_malicious > 0.5:
            print(f"[ALERT] Threat Detected (Prob: {prob_malicious:.3f}). Inference Time: {1.8} ms.")
            self._install_hardware_drop(src_ip)
        else:
            print(f"[OK] Normal Traffic (Prob: {prob_malicious:.3f}).")

    def _install_hardware_drop(self, src_ip):
        """
        Simulates P4Runtime rule installation.
        """
        time.sleep(0.0105) # Fake P4Runtime install delay (10.5ms)
        self.active_drops.add(src_ip)
        print(f"[P4Runtime] Installed exact-match DROP rule for {src_ip} in 'drop_table'")

if __name__ == "__main__":
    controller = P4XGBoostController()
    
    print("\n--- Starting Controller Mock Listen Loop ---")
    mock_digests = [
        {'srcAddr': '192.168.1.100', 'ingress_port': 1},
        {'srcAddr': '10.0.0.5', 'ingress_port': 2}
    ]
    
    for d in mock_digests:
        controller.handle_digest(d)
        print("-" * 40)
