import streamlit as st
from components.PieChart import PieChart

def Home():
    st.title("🛡️ IDS Project — Intelligent Network Flow Analysis")
    st.markdown("""
    Welcome to the Intrusion Detection System project dashboard.

    This tool analyzes network flow CSV data to detect cyber-attacks using AI-powered models.

    **Get started by uploading your network traffic data** and explore detailed threat insights.
    """)

    # Get Started button that navigates to Upload page
    if st.button("🚀 Get Started"):
        st.query_params["page"] = "Upload"

    # Sample demo data for the pie chart
    sample_attack_data = {
        "Normal": 150,
        "DDoS": 45,
        "PortScan": 25,
        "Botnet": 12,
        "Other": 8
    }

    st.subheader("Sample Attack Type Distribution")
    PieChart(sample_attack_data)

    st.markdown("---")
    st.markdown("""
    <footer style='text-align:center; font-size:0.8rem; color:gray; margin-top:2rem;'>
        Developed by Shagufta Riaz | Software Engineering FYP 2025 | Contact: shagufta@example.com
    </footer>
    """, unsafe_allow_html=True)
