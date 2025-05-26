import streamlit as st
from utils.api_client import upload_csv

def FileUploader(on_upload_success):
    st.title("Upload Network Flow CSV")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Save to a temporary file for sending to backend
        with open("temp_uploaded.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.info(f"Uploaded file: {uploaded_file.name}")

        if st.button("Analyze"):
            with st.spinner("Sending file to backend for prediction..."):
                try:
                    results = upload_csv("temp_uploaded.csv")
                    st.success("Analysis completed!")
                    on_upload_success(results)
                except Exception as e:
                    st.error(f"Failed to get prediction: {e}")
