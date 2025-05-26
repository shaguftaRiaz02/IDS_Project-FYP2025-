import streamlit as st

def ResultCard(title: str, value: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="border: 1px solid #e6e6e6; border-radius: 10px; padding: 1rem; background-color: #f9f9f9;">
            <h4 style="margin-bottom: 0.5rem;">{title}</h4>
            <h2 style="color: #4CAF50;">{value}</h2>
            <p style="font-size: 0.9rem; color: #777;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
