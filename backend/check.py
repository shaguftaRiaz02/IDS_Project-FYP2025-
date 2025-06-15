from predict import Predictor
from preprocessing import preprocess_uploaded_csv
import pandas as pd

predictor = Predictor(
    model_path='models/best_hids_model.pkl',
    scaler_path='models/scaler_model.pkl',
    encoder_path='models/label_encoder.pkl',
    pca_path='models/pca_model.pkl',
    debug=True
)

# Optional: Load and test your infiltration.csv here to trigger prediction
df = pd.read_csv("E:/FYP_2025 (2)/FYP_2025/IDS-Project/data/infiltration.csv")
processed_df = preprocess_uploaded_csv(df)
results = predictor.predict(processed_df, cheat_mode=False)

for res in results[:5]:
    print(res)
