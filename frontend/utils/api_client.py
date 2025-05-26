import requests

BACKEND_URL = "http://127.0.0.1:8000"

def upload_csv(file_path: str) -> dict:
    """
    Upload a CSV file to the backend /predict endpoint and get prediction results.
    """
    with open(file_path, "rb") as f:
        files = {"csv_file": (file_path, f, "text/csv")}
        response = requests.post(f"{BACKEND_URL}/predict", files=files)
        response.raise_for_status()
        return response.json()
