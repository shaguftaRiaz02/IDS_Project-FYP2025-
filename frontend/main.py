import streamlit as st
from pages.Home import Home
from pages.Upload import Upload

st.set_page_config(page_title="IDS Project", layout="wide")

def main():
    st.sidebar.title("🛡️ IDS Project Navigation")

    # Get current query param (use new API)
    query_params = st.query_params
    default_page = query_params.get("page", "Home")

    # Sidebar overrides query param
    page = st.sidebar.radio("Go to", ["Home", "Upload"], index=["Home", "Upload"].index(default_page))

    # Render selected page
    if page == "Home":
        Home()
    elif page == "Upload":
        Upload()

    # Sync sidebar selection back to query param
    st.query_params["page"] = page

if __name__ == "__main__":
    main()
