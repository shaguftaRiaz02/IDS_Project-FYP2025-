import joblib
from pathlib import Path
import pandas as pd
import numpy as np

class ModelPredictor:
    def __init__(self):
        base_path = Path(__file__).parent.parent / "models"
        
        # Load model and preprocessing objects
        self.model = joblib.load(base_path / "best_hids_model.pkl")
        self.scaler = joblib.load(base_path / "scaler_model.pkl")
        self.encoder = joblib.load(base_path / "label_encoder.pkl")
        self.pca = joblib.load(base_path / "pca_model.pkl")
        
        # Load feature columns
        with open(base_path / "feature_columns.txt", "r") as f:
            self.feature_columns = [line.strip() for line in f.readlines()]

    def predict(self, input_df: pd.DataFrame):
        if input_df.empty:
            raise ValueError("Input DataFrame is empty. Cannot make predictions.")

        # Match input to expected columns
        input_df = input_df.reindex(columns=self.feature_columns, fill_value=0)

        # Ensure numeric type
        input_df = input_df.apply(pd.to_numeric, errors='coerce').fillna(0)

        # Apply scaler and PCA
        try:
            scaled_data = self.scaler.transform(input_df)
            reduced_data = self.pca.transform(scaled_data)
        except Exception as e:
            raise RuntimeError(f"Error during preprocessing: {e}")

        # Make predictions
        try:
            prediction = self.model.predict(reduced_data)
            print("Raw prediction output:", prediction)
            print("Prediction dtype:", prediction.dtype)
        except Exception as e:
            raise RuntimeError(f"Model prediction failed: {e}")

        # Decode labels if necessary
        try:
            if prediction.dtype == object or isinstance(prediction[0], str):
                return prediction
            decoded = self.encoder.inverse_transform(prediction)
            return decoded
        except Exception as e:
            print("Error during inverse transform:", e)
            return prediction  # fallback to raw output
