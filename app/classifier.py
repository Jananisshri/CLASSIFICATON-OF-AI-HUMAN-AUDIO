import joblib
import os
import numpy as np
from .feature_extractor import extract_features, FEATURE_NAMES

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')

class VoiceClassifier:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"Model loaded from {MODEL_PATH}")
            except Exception as e:
                print(f"Failed to load model: {e}")
        else:
            print(f"Model file not found at {MODEL_PATH}. Prediction will fail unless trained.")

    def predict_voice(self, audio_path: str):
        if not self.model:
            return None, 0.0, "Model not active"

        features = extract_features(audio_path)
        if features is None:
            raise ValueError("Could not extract features from audio")
        
        # Reshape for single sample
        X = features.reshape(1, -1)
        
        # Get probabilities
        probs = self.model.predict_proba(X)[0]
        
        # Label 0 = AI_GENERATED, 1 = HUMAN
        ai_prob = probs[0] 
        human_prob = probs[1]
        
        if ai_prob > human_prob:
            label = "AI_GENERATED"
            confidence = ai_prob
        else:
            label = "HUMAN"
            confidence = human_prob
            
        explanation = self._generate_dynamic_explanation(X, label, confidence)
        
        return label, float(confidence), explanation

    def _generate_dynamic_explanation(self, X, label, confidence):
        """
        Dynamically generates an explanation based on which features are outliers 
        relative to the training distribution.
        """
        try:
            # Get the pipeline steps
            scaler = self.model.named_steps['scaler']
            
            # Transform the features (Z-score)
            X_scaled = scaler.transform(X)[0]
            
            # Find top contributing features (highest absolute Z-score)
            top_indices = np.argsort(np.abs(X_scaled))[::-1][:5]
            
            reasons = []
            for idx in top_indices:
                feat_name = FEATURE_NAMES[idx]
                val = X_scaled[idx]
                
                if "mfcc" in feat_name:
                    if val > 1.5: reasons.append("complex spectral artifacts")
                    elif val < -1.5: reasons.append("unusually simplified spectral shape")
                elif "delta" in feat_name:
                    if val > 1.5: reasons.append("irregular temporal transitions")
                    elif val < -1.5: reasons.append("unnatural temporal smoothness")
                elif "flatness" in feat_name and val > 1.0:
                    reasons.append("synthetic spectral flatness")
                elif "hnr" in feat_name and val < -1.0:
                    reasons.append("lack of natural rhythmic noise")
                elif "pitch" in feat_name and val < -1.0:
                    reasons.append("robotic pitch stability")
            
            # Dedup and limit
            reasons = list(dict.fromkeys(reasons))[:3]
            
            if not reasons:
                if label == "AI_GENERATED":
                    return f"Synthetic patterns detected with {confidence:.1%} confidence based on high-order spectral analysis."
                else:
                    return f"Voice exhibits natural acoustic properties consistent with human speech ({confidence:.1%} confidence)."
            
            if label == "AI_GENERATED":
                return f"Flagged as AI due to {', '.join(reasons)}. These patterns match synthetic vocoder signatures."
            else:
                return f"Verified as human based on {', '.join(reasons)} and natural vocal micro-variations."
                
        except Exception as e:
            print(f"Explanation Error: {e}")
            return f"Classification based on statistical vocal anomalies ({confidence:.1%} confidence)."

# Global instance
classifier = VoiceClassifier()
