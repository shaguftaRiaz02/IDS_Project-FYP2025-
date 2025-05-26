import joblib
import numpy as np

class Predictor:
    def __init__(self, model_path, scaler_path, encoder_path, pca_path, debug=False):
        self.debug = debug
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)
            self.pca = joblib.load(pca_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model components: {e}")

    def predict(self, df):
        try:
            scaled = self.scaler.transform(df)
            pca_features = self.pca.transform(scaled)
            pred_encoded = self.model.predict(pca_features)

            if self.debug:
                print("Predicted encoded labels:", pred_encoded)
                print("Encoder classes:", self.encoder.classes_)

            if isinstance(pred_encoded[0], str):
                pred_labels = pred_encoded
            else:
                pred_labels = self.encoder.inverse_transform(pred_encoded)

            pred_proba = self.model.predict_proba(pca_features) if hasattr(self.model, 'predict_proba') else None

            results = []
            for i, label in enumerate(pred_labels):
                confidence = None
                if pred_proba is not None:
                    label_index = list(self.encoder.classes_).index(label)
                    confidence = float(pred_proba[i][label_index])
                results.append({
                    "predicted_label": label,
                    "confidence_score": confidence,
                    "explanation": ""  # Placeholder
                })

            return results
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
