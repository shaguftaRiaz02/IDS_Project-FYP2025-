from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from io import StringIO
from backend.preprocessing import preprocess_uploaded_csv
from backend.predict import Predictor
from collections import Counter
from pathlib import Path
from typing import Dict, Any

app = FastAPI()

# ✅ CORS middleware for frontend (Streamlit) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:8501"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route for quick test
@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

# ✅ Set up paths and load model
BASE_DIR = Path(__file__).parent  # backend folder

predictor = Predictor(
    model_path=str(BASE_DIR / 'models' / 'best_hids_model.pkl'),
    scaler_path=str(BASE_DIR / 'models' / 'scaler_model.pkl'),
    encoder_path=str(BASE_DIR / 'models' / 'label_encoder.pkl'),
    pca_path=str(BASE_DIR / 'models' / 'pca_model.pkl')
)

# ✅ Prediction endpoint
@app.post("/predict")
async def predict(csv_file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        contents = await csv_file.read()
        s = contents.decode('utf-8')
        df = pd.read_csv(StringIO(s))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file or encoding: {e}")

    try:
        processed_df = preprocess_uploaded_csv(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing failed: {e}")

    try:
        prediction_results = predictor.predict(processed_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    labels = [res["predicted_label"] for res in prediction_results]
    attack_counts = dict(Counter(labels))

    confidences = [res["confidence_score"] for res in prediction_results if res["confidence_score"] is not None]
    summary_stats = {}
    if confidences:
        summary_stats = {
            "average_confidence": sum(confidences) / len(confidences),
            "max_confidence": max(confidences),
            "min_confidence": min(confidences),
        }

    return {
        "total_flows": len(prediction_results),
        "attack_counts": attack_counts,
        "summary_stats": summary_stats,
        "detailed_results": prediction_results
    }
