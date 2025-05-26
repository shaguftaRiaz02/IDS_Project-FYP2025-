from backend.utils.model_predictor import ModelPredictor
import pandas as pd
from backend.preprocessing import preprocess_uploaded_csv

# Initialize predictor instance
predictor = ModelPredictor()
print("Encoder classes:", predictor.encoder.classes_)

# Load and preprocess CSV
df = pd.read_csv("data/traffic test.pcap_Flow.csv")
processed_df = preprocess_uploaded_csv(df)

# Apply PCA on full dataset
pca_all = predictor.pca.transform(processed_df)
pca_all_df = pd.DataFrame(pca_all, columns=predictor.model.feature_names_in_)

# Ensure features match model input
expected_features = predictor.model.feature_names_in_
if list(pca_all_df.columns) != list(expected_features):
    raise ValueError("Input columns don't match model expectations.")

# Predict all rows
predictions = predictor.predict(pca_all_df)
df["Prediction"] = predictions
df.to_csv("output_predictions_all.csv", index=False)

# Show summary
print("🔍 Prediction summary:\n", df["Prediction"].value_counts())
