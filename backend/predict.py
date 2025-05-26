import joblib
import numpy as np

class Predictor:
    def __init__(self, model_path, scaler_path, encoder_path, pca_path):
        # Load the model, scaler, label encoder, and PCA objects
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.encoder = joblib.load(encoder_path)
        self.pca = joblib.load(pca_path)

    def predict(self, df):
        # Scale the features
        scaled = self.scaler.transform(df)

        # Apply PCA transformation
        pca_features = self.pca.transform(scaled)

        # Predict using the trained model
        pred_encoded = self.model.predict(pca_features)

        # Debug prints - remove or comment out in production
        print("Predicted encoded labels:", pred_encoded)
        print("Encoder classes:", self.encoder.classes_)

        # Determine if model output is encoded labels or class names directly
        if isinstance(pred_encoded[0], str):
            # Model directly outputs class names (e.g., 'Normal', 'AttackName')
            pred_labels = pred_encoded
        else:
            # Model outputs encoded labels (integers), convert to class names
            pred_labels = self.encoder.inverse_transform(pred_encoded)

        # Get prediction probabilities if available
        if hasattr(self.model, 'predict_proba'):
            pred_proba = self.model.predict_proba(pca_features)
        else:
            pred_proba = None

        results = []
        for i, label in enumerate(pred_labels):
            confidence = None
            if pred_proba is not None:
                # Find index of predicted label in encoder classes
                label_index = list(self.encoder.classes_).index(label)
                confidence = float(pred_proba[i][label_index])

            results.append({
                "predicted_label": label,
                "confidence_score": confidence,
                "explanation": ""  # Add explanation logic later if needed
            })

        return results
