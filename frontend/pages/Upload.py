import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from components.FileUploader import FileUploader
from components.FlowTable import FlowTable
from components.PieChart import PieChart


def generate_pdf_report(filename, total_flows, attack_counts, summary_stats):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 50, "Network Flow Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(30, height - 80, f"File: {filename}")
    c.drawString(30, height - 100, f"Total Flows: {total_flows}")

    c.drawString(30, height - 130, "Attack Type Distribution:")
    y = height - 150
    if attack_counts:
        for attack, count in attack_counts.items():
            percent = (count / total_flows) * 100 if total_flows else 0
            c.drawString(50, y, f"- {attack}: {count} flows ({percent:.2f}%)")
            y -= 20
    else:
        c.drawString(50, y, "No attacks detected.")
        y -= 20

    y -= 10
    c.drawString(30, y, "Prediction Confidence Overview:")
    y -= 20

    min_conf = summary_stats.get('min_confidence', 0) * 100
    avg_conf = summary_stats.get('average_confidence', 0) * 100
    max_conf = summary_stats.get('max_confidence', 0) * 100

    c.drawString(50, y, f"- Minimum Confidence: {min_conf:.2f}%")
    y -= 20
    c.drawString(50, y, f"- Average Confidence: {avg_conf:.2f}%")
    y -= 20
    c.drawString(50, y, f"- Maximum Confidence: {max_conf:.2f}%")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def Upload():
    st.header("Network Flow Upload & Analysis")

    # Restore from session state or initialize to None
    results = st.session_state.get('results', None)
    uploaded_df = st.session_state.get('uploaded_df', None)
    uploaded_filename = st.session_state.get('uploaded_filename', None)

    def handle_results(results_data, filename, df):
        st.session_state['results'] = results_data
        st.session_state['uploaded_df'] = df
        st.session_state['uploaded_filename'] = filename
        # Streamlit automatically reruns when session_state changes

    FileUploader(on_upload_success=handle_results)

    # Fallback if no upload data passed yet
    if uploaded_df is None:
        try:
            uploaded_df = pd.read_csv("temp_uploaded.csv")
            uploaded_filename = "temp_uploaded.csv"
            st.session_state['uploaded_df'] = uploaded_df
            st.session_state['uploaded_filename'] = uploaded_filename
        except Exception:
            uploaded_df = None
            uploaded_filename = None

    # Show PDF report download button early, if results exist
    if results and uploaded_df is not None:
        total_flows = results.get("total_flows", len(uploaded_df))
        attack_counts = results.get("attack_counts", {})
        summary_stats = results.get("summary_stats", {})

        pdf_buffer = generate_pdf_report(
            uploaded_filename,
            total_flows,
            attack_counts,
            summary_stats
        )
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="network_flow_report.pdf",
            mime="application/pdf"
        )

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
