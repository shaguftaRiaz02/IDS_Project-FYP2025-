import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from components.FileUploader import FileUploader
from components.FlowTable import FlowTable
from components.PieChart import PieChart

def Upload():
    st.header("Network Flow Upload & Analysis")

    results = None
    
    def handle_results(data):
        nonlocal results
        results = data

    FileUploader(on_upload_success=handle_results)

    if results:
        st.write("### Debug: Results received")
        st.write(results)

        total_flows = results.get("total_flows")
        attack_counts = results.get("attack_counts", {})
        summary_stats = results.get("summary_stats", {})

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Attack Type Distribution (Pie Chart)")
            if attack_counts:
                PieChart(attack_counts)
            else:
                st.write("No attack data to show.")

        with col2:
            st.subheader("Attack Counts (Bar Chart)")
            if attack_counts:
                df_attack = pd.DataFrame(list(attack_counts.items()), columns=["Attack Type", "Count"])
                plt.figure(figsize=(5,3))
                sns.barplot(x="Count", y="Attack Type", data=df_attack, palette="viridis")
                plt.xlabel("Count")
                plt.ylabel("")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.write("No attack data to show.")

        st.markdown("---")

        col3, col4 = st.columns([1, 2])

        with col3:
            st.subheader("Summary Report")
            summary_text = f"""
**Total Flows:** {total_flows if total_flows is not None else 'N/A'}  
Number of flows analyzed

**Average Confidence:** {summary_stats.get('average_confidence', 'N/A') if summary_stats.get('average_confidence') is None else f"{summary_stats.get('average_confidence'):.2f}"}  
Mean prediction confidence

**Max Confidence:** {summary_stats.get('max_confidence', 'N/A') if summary_stats.get('max_confidence') is None else f"{summary_stats.get('max_confidence'):.2f}"}  
Highest prediction confidence

**Min Confidence:** {summary_stats.get('min_confidence', 'N/A') if summary_stats.get('min_confidence') is None else f"{summary_stats.get('min_confidence'):.2f}"}  
Lowest prediction confidence
            """
            st.markdown(summary_text)

        with col4:
            st.subheader("Detailed Flow Data")
            FlowTable(results)  # Pass full results dict here
