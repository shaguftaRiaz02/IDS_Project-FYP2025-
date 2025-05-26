import joblib
from pathlib import Path
import pandas as pd

class ModelPredictor:
    def __init__(self):
        base_path = Path(__file__).parent.parent / "models"
        self.model = joblib.load(base_path / "best_hids_model.pkl")
        self.scaler = joblib.load(base_path / "scaler_model.pkl")
        self.encoder = joblib.load(base_path / "label_encoder.pkl")
        self.pca = joblib.load(base_path / "pca_model.pkl")

        # Load feature columns
        with open(base_path / "feature_columns.txt", "r") as f:
            self.feature_columns = [line.strip() for line in f.readlines()]

    def predict(self, input_df):
        # Reindex input DataFrame to match training columns (fill missing with 0)
        input_df = input_df.reindex(columns=self.feature_columns, fill_value=0)

        scaled_data = self.scaler.transform(input_df)
        reduced_data = self.pca.transform(scaled_data)
        prediction = self.model.predict(reduced_data)

        print("Raw prediction output:", prediction)
        print("Prediction dtype:", prediction.dtype)

        if prediction.dtype == 'object':
            return prediction

        try:
            decoded = self.encoder.inverse_transform(prediction)
            return decoded
        except Exception as e:
            print("Error during inverse transform:", e)
            return None
