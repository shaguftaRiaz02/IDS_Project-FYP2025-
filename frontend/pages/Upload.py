import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors

from components.FileUploader import FileUploader
from components.FlowTable import FlowTable
from components.PieChart import PieChart


def generate_pdf_report(filename, total_flows, attack_counts, summary_stats):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - margin

    def draw_heading(text, font_size=14, gap=20):
        nonlocal y
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(margin, y, text)
        y -= gap

    def draw_text_line(text, font_size=11, gap=15):
        nonlocal y
        c.setFont("Helvetica", font_size)
        c.drawString(margin + 20, y, text)
        y -= gap

    def draw_divider(gap=15):
        nonlocal y
        c.setStrokeColor(colors.grey)
        c.line(margin, y, width - margin, y)
        y -= gap

    # Report Title
    draw_heading("📄 Network Flow Analysis Report", 16)
    draw_divider()

    # Basic Info
    draw_text_line(f"📁 File Analyzed: {filename}")
    draw_text_line(f"📊 Total Network Flows: {total_flows}")
    draw_divider()

    # Attack Distribution
    draw_heading("🛡️ Attack Type Distribution")
    if attack_counts:
        for attack, count in attack_counts.items():
            percent = (count / total_flows) * 100 if total_flows else 0
            draw_text_line(f"• {attack}: {count} flows ({percent:.2f}%)")
    else:
        draw_text_line("✅ No attacks detected in the uploaded dataset.")
    draw_divider()

    # Prediction Confidence
    draw_heading("📈 Prediction Confidence Overview")
    min_conf = summary_stats.get('min_confidence', 0) * 100
    avg_conf = summary_stats.get('average_confidence', 0) * 100
    max_conf = summary_stats.get('max_confidence', 0) * 100

    draw_text_line(f"• Minimum Confidence: {min_conf:.2f}%")
    draw_text_line(f"• Average Confidence: {avg_conf:.2f}%")
    draw_text_line(f"• Maximum Confidence: {max_conf:.2f}%")
    draw_divider()

    # Suggestions based on average confidence
    draw_heading("🔍 Recommendations Based on Confidence")
    if avg_conf >= 85:
        draw_text_line("✅ High confidence in results. You may rely on this analysis for threat monitoring.")
    elif 60 <= avg_conf < 85:
        draw_text_line("⚠️ Moderate confidence. Cross-verify suspicious flows with additional tools or human review.")
    else:
        draw_text_line("🚨 Low confidence. Retrain model or investigate data quality for more accurate insights.")

    c.setFillColor(colors.black)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def Upload():
    st.header("Network Flow Upload & Analysis")

    results = st.session_state.get('results', None)
    uploaded_df = st.session_state.get('uploaded_df', None)
    uploaded_filename = st.session_state.get('uploaded_filename', None)

    def handle_results(results_data, filename, df):
        st.session_state['results'] = results_data
        st.session_state['uploaded_df'] = df
        st.session_state['uploaded_filename'] = filename

    FileUploader(on_upload_success=handle_results)

    if uploaded_df is None:
        try:
            uploaded_df = pd.read_csv("temp_uploaded.csv")
            uploaded_filename = "temp_uploaded.csv"
            st.session_state['uploaded_df'] = uploaded_df
            st.session_state['uploaded_filename'] = uploaded_filename
        except Exception:
            uploaded_df = None
            uploaded_filename = None

    if results and uploaded_df is not None:
        total_flows = results.get("total_flows", len(uploaded_df))
        attack_counts = results.get("attack_counts", {})
        summary_stats = results.get("summary_stats", {})

        # PDF download button
        pdf_buffer = generate_pdf_report(uploaded_filename, total_flows, attack_counts, summary_stats)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name="network_flow_report.pdf",
            mime="application/pdf"
        )

        # Summary section
        st.markdown(f"**File uploaded:** `{uploaded_filename}`")
        st.markdown(f"**Total flows (rows):** {total_flows}")
        if attack_counts and total_flows > 0:
            st.markdown("**Attack type distribution:**")
            for attack, count in attack_counts.items():
                percent = (count / total_flows) * 100
                st.markdown(f"- {attack}: {count} flows ({percent:.2f}%)")
        else:
            st.markdown("✅ No attacks detected in uploaded data.")

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
                sns.barplot(x="Count", y="Attack Type", data=df_attack, hue="Attack Type", palette="viridis", legend=False)
                plt.xlabel("Count")
                plt.ylabel("")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.write("No attack data to show.")

        st.subheader("Uploaded Network Flow Data")
        st.dataframe(uploaded_df)

        st.markdown("---")

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
- 🤖 **Average Confidence:** {average_conf * 100:.2f}%
- 🚀 **Maximum Confidence:** {max_conf * 100:.2f}%

📜 These values show how sure the model was when classifying flows as normal or malicious.
        """)

        st.subheader("Detailed Flow Data")
        FlowTable(results, uploaded_df)
