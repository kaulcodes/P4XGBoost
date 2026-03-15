from __future__ import annotations

class XGBoostEnsemble:
    """
    Mock XGBoost Model matching the paper params:
    - 100 estimators
    - max tree depth 6
    - learning rate 0.1
    - binary:logistic
    """
    
    def __init__(self):
        print("[INFO] Initializing XGBoost Ensemble...")
        print("[PARAMS] n_estimators=100, max_depth=6, eta=0.1, objective='binary:logistic'")
        
    def predict_proba(self, features: list[float]) -> list[list[float]]:
        """
        Predicts malicious probability based on the 8D vector.
        Features mapping: [pkt_rate, byte_rate, duration, proto_var, port_div, size_var, tcp_flags, inter_arrival]
        """
        pkt_rate = features[0]
        
        if pkt_rate > 500:
            return [[0.01, 0.99]]
        return [[0.99, 0.01]]
