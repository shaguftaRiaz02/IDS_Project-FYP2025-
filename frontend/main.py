import streamlit as st
from pages.Home import Home
from pages.Upload import Upload

# ✅ Must be first Streamlit command
st.set_page_config(page_title="IDS Project", layout="wide")

def main():
    st.sidebar.title("🛡️ IDS Project Navigation")

    # ✅ Get current query params using new API
    query_params = st.query_params
    default_page = query_params.get("page", "Home")

    # ✅ Sidebar menu with default page
    page = st.sidebar.radio("Go to", ["Home", "Upload"], index=["Home", "Upload"].index(default_page))

    # ✅ Set query params using the new API (assignment)
    st.query_params["page"] = page

    # ✅ Render selected page
    if page == "Home":
        Home()
    elif page == "Upload":
        Upload()

if __name__ == "__main__":
    main()
