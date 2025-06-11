import joblib
import numpy as np
import pandas as pd
import os

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

        # Load feature column names
        feature_path = os.path.join(os.path.dirname(model_path), "feature_columns.txt")
        try:
            with open(feature_path, "r") as f:
                self.feature_columns = f.read().splitlines()
        except Exception as e:
            raise RuntimeError(f"Failed to load feature columns from '{feature_path}': {e}")

    def predict(self, df):
        try:
            # Ensure input is a DataFrame with correct column names
            if not isinstance(df, pd.DataFrame):
                df = pd.DataFrame(df, columns=self.feature_columns)
            else:
                df.columns = self.feature_columns

            # Preprocess
            scaled = self.scaler.transform(df)
            pca_features = self.pca.transform(scaled)

            # Predict
            pred_encoded = self.model.predict(pca_features)

            if self.debug:
                print("Predicted encoded labels:", pred_encoded)
                print("Encoder classes:", self.encoder.classes_)

            # Decode predictions
            if isinstance(pred_encoded[0], str):
                pred_labels = pred_encoded
            else:
                pred_labels = self.encoder.inverse_transform(pred_encoded)

            # Probabilities
            pred_proba = self.model.predict_proba(pca_features) if hasattr(self.model, 'predict_proba') else None

            # Format results
            results = []
            for i, label in enumerate(pred_labels):
                confidence = None
                if pred_proba is not None:
                    label_index = list(self.encoder.classes_).index(label)
                    confidence = float(pred_proba[i][label_index])
                results.append({
                    "predicted_label": label,
                    "confidence_score": confidence,
                    "explanation": ""  # Placeholder for SHAP, LIME, etc.
                })

            return results
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
