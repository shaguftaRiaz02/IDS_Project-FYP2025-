import streamlit as st
import pandas as pd
from utils.api_client import upload_csv

def FileUploader(on_upload_success):
    st.title("Upload Network Flow CSV")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        st.info(f"Uploaded file: {uploaded_file.name}")

        if st.button("Analyze"):
            with st.spinner("Sending file to backend for prediction..."):
                try:
                    # Save temp file for backend
                    with open("temp_uploaded.csv", "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Read raw CSV for showing data later
                    df = pd.read_csv(uploaded_file)

                    results = upload_csv("temp_uploaded.csv")

                    st.success("Analysis completed!")

                    # Pass results, filename, and raw df to callback
                    on_upload_success(results, uploaded_file.name, df)

                except Exception as e:
                    st.error(f"Failed to get prediction: {e}")
