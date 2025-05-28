import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from components.PieChart import PieChart

def Home():
    # st.set_page_config(page_title="IDS Home", layout="wide")
    st.title("🛡️ Intelligent Intrusion Detection System (IDS) Dashboard")

    st.markdown("""
    Welcome to your **AI-powered Network Traffic Analyzer**.  
    This tool leverages machine learning to detect threats from CSV-formatted network flow data.

    🔐 **Key System Capabilities**
    - 📁 Upload `.csv` files (from Wireshark + CICFlowMeter)
    - ⚠️ Detect threats: **DDoS, DoS, PortScan, Botnet, Brute Force, Web Attack, Heartbleed, Infiltration**
    - 📊 Interactive dashboards: pie charts, scatter plots, heatmaps & flow timelines
    - 🧠 Real-time predictions using trained models (ML/PCA/scaler/label encoder)
    - 📎 Generate and download full threat reports in **CSV & PDF**
    - ✍️ Label and track anomalies for future model retraining
    """)

    st.markdown("---")
    st.subheader("📊 Sample Visualizations")

    # Layout 3 charts in one row
    col1, col2, col3 = st.columns([1, 1, 1.2])  # Adjust column width ratios as needed

    with col1:
        st.markdown("**Attack Type Distribution (Pie Chart)**")
        sample_attack_data = {
            "BENIGN": 150,
            "DoS": 50,
            "DDoS": 45,
            "PortScan": 30,
            "Brute Force": 12,
            "Web Attack": 8,
            "Bot": 6,
            "Infiltration": 2,
            "Heartbleed": 1
        }
        PieChart(sample_attack_data)

    with col2:
        st.markdown("**Traffic Scatter Plot (Packets vs Bytes)**")
        scatter_df = pd.DataFrame({
            "Packets": np.random.randint(10, 500, 100),
            "Bytes": np.random.randint(100, 10000, 100),
            "Label": np.random.choice(["BENIGN", "DDoS", "PortScan"], 100)
        })
        st.scatter_chart(scatter_df, x="Packets", y="Bytes", color="Label")

    with col3:
        st.markdown("**Feature Correlation (Heatmap)**")
        corr_data = pd.DataFrame(np.random.rand(6, 6), 
                                 columns=[f'F{i}' for i in range(1, 7)])
        fig, ax = plt.subplots(figsize=(4, 3.5))  # Smaller figure to reduce height
        sns.heatmap(corr_data.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("💻 Simulating Attacks with Kali Linux")

    col_text, col_img = st.columns([3, 1])
    with col_text:
        st.markdown("""
        We use **Kali Linux**, a professional cybersecurity and ethical hacking platform, to simulate various cyberattacks in a controlled lab environment.  

        🔧 **Simulated Attacks:**
        - **DDoS/DoS Attacks** – via tools like `hping3`, `slowloris`
        - **Port Scanning** – using `nmap`, `zenmap`
        - **Brute Force** – with `hydra`, `medusa`
        - **Botnet Traffic** – custom scripts or Metasploit payloads
        - **Web Exploits & Heartbleed** – CVE-based simulations

        🔍 These simulations help validate model performance by:
        - Generating **realistic threat patterns**
        - Enabling **controlled testing of detection capabilities**
        - Providing **benchmark datasets** for retraining
        """)

    with col_img:
        st.image("assets/kali.jpeg", width=400, caption="Kali Linux - Penetration Testing OS")


    st.markdown("---")
    st.subheader("🌟 Benefits to Users")
    st.markdown("""
    ✅ Detect and respond to threats quickly  
    ✅ Visualize network behavior in real-time  
    ✅ Download detailed forensic reports  
    ✅ Improve your cybersecurity posture using intelligent analysis  
    ✅ Easily extend or retrain with new datasets
    """)

    st.markdown("---")
    st.subheader("🚀 Ready to Detect Threats?")
    st.markdown("Go to the **Upload** page and start analyzing your traffic logs now.")
    if st.button("Go to Upload Page"):
        st.query_params["page"] = "Upload"

    st.markdown("---")
    st.markdown("""
    <footer style='text-align:center; font-size:0.9rem; color:gray; margin-top:2rem;'>
        Developed by <b>Shagufta Riaz</b> & <b>Zayab Akhtar</b> | BS Software Engineering - Final Year Project 2025<br>
        📧 Contact: shaguftariaz771@gmail.com | zayabakhtar112@gmail.com
    </footer>
    """, unsafe_allow_html=True)
