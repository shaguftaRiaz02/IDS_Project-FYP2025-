import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

from components.FileUploader import FileUploader
from components.FlowTable import FlowTable
from components.PieChart import PieChart

def Upload():
    st.header("Network Flow Upload & Analysis")

    results = None
    uploaded_df = None
    uploaded_filename = None

    def handle_results(results_data, filename, df):
        nonlocal results, uploaded_filename, uploaded_df
        results = results_data
        uploaded_filename = filename
        uploaded_df = df

    FileUploader(on_upload_success=handle_results)

    # fallback if no upload data passed yet
    if uploaded_df is None:
        try:
            uploaded_df = pd.read_csv("temp_uploaded.csv")
            uploaded_filename = "temp_uploaded.csv"
        except Exception:
            uploaded_df = None
            uploaded_filename = None

    if results and uploaded_df is not None:
        total_flows = results.get("total_flows", len(uploaded_df))
        attack_counts = results.get("attack_counts", {})

        desc_lines = []
        desc_lines.append(f"**File uploaded:** `{uploaded_filename}`")
        desc_lines.append(f"**Total flows (rows):** {total_flows}")

        if attack_counts and total_flows > 0:
            desc_lines.append("**Attack type distribution:**")
            for attack, count in attack_counts.items():
                percent = (count / total_flows) * 100
                desc_lines.append(f"- {attack}: {count} flows ({percent:.2f}%)")
        else:
            desc_lines.append("No attacks detected in uploaded data.")

        st.markdown("\n".join(desc_lines))

        col1, col2 = st.columns(2)

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
                plt.figure(figsize=(5, 3))
                sns.barplot(x="Count", y="Attack Type", data=df_attack, palette="viridis")
                plt.xlabel("Count")
                plt.ylabel("")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.write("No attack data to show.")

        st.subheader("Uploaded Network Flow Data")
        st.dataframe(uploaded_df)

        st.markdown("---")

        # Summary report with plot
        summary_stats = results.get("summary_stats", {})
        average_conf = summary_stats.get('average_confidence', 0)
        max_conf = summary_stats.get('max_confidence', 0)
        min_conf = summary_stats.get('min_confidence', 0)

        st.markdown("### 📊 Prediction Confidence Overview")

        conf_df = pd.DataFrame({
            'Confidence Type': ['Minimum Confidence', 'Average Confidence', 'Maximum Confidence'],
            'Value': [min_conf, average_conf, max_conf]
        })

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=conf_df['Confidence Type'],
            y=conf_df['Value'],
            mode='lines+markers',
            line=dict(color='royalblue', width=2),
            marker=dict(size=10)
        ))
        fig.update_layout(
            yaxis=dict(range=[0, 1], title='Confidence Score'),
            xaxis=dict(title='Metric'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
### 🔍 Confidence Breakdown (in %)

- 🐢 **Minimum Confidence:** {min_conf * 100:.2f}%
  - This represents the lowest certainty recorded by the model across all network flows.
  - If this value is below 50%, it indicates the model was unsure about at least one flow.

- 🤖 **Average Confidence:** {average_conf * 100:.2f}%
  - The overall mean confidence score across all predictions.
  - Values above 70% generally indicate reliable model predictions.

- 🚀 **Maximum Confidence:** {max_conf * 100:.2f}%
  - The highest confidence score observed.
  - A value close to 100% means the model was very certain about some flows.

📜 These confidence values reflect the model's certainty in classifying each network flow as normal or malicious, helping users understand the reliability of the predictions.
        """)

        st.subheader("Detailed Flow Data")
        FlowTable(results, uploaded_df)
