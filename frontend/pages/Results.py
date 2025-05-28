import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Network IDS Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def get_pdf_bytes(pdf):
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def generate_pdf(results, flow_data_df, report_type):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if report_type == "Summary":
        total_flows = len(flow_data_df)
        pdf.cell(0, 10, f"Total flows analyzed: {total_flows}", ln=True)
        if "Predicted Label" in flow_data_df.columns:
            malicious = flow_data_df[flow_data_df["Predicted Label"] != "Normal"].shape[0]
            normal = flow_data_df[flow_data_df["Predicted Label"] == "Normal"].shape[0]
            pdf.cell(0, 10, f"Malicious flows: {malicious}", ln=True)
            pdf.cell(0, 10, f"Normal flows: {normal}", ln=True)
        if "Dst IP" in flow_data_df.columns:
            top_ips = flow_data_df[flow_data_df["Predicted Label"] != "Normal"]["Dst IP"].value_counts().head(5)
            pdf.cell(0, 10, "Top attacked Destination IPs:", ln=True)
            for ip, count in top_ips.items():
                pdf.cell(0, 10, f" - {ip}: {count} attacks", ln=True)

    elif report_type == "Detailed":
        pdf.cell(0, 10, "Detailed Network Flows:", ln=True)
        cols = ['Src IP', 'Dst IP', 'Protocol', 'Flow Duration', 'Predicted Label', 'Confidence (%)']
        for _, row in flow_data_df.iterrows():
            line = ", ".join([f"{col}: {row.get(col, 'N/A')}" for col in cols])
            pdf.multi_cell(0, 8, line)

    elif report_type == "Incident":
        pdf.cell(0, 10, "Incident Report (Suspicious flows):", ln=True)
        suspicious = flow_data_df[flow_data_df["Predicted Label"] != "Normal"]
        for _, row in suspicious.iterrows():
            pdf.cell(0, 10, f"Src IP: {row.get('Src IP', 'N/A')} -> Dst IP: {row.get('Dst IP', 'N/A')}", ln=True)
            pdf.cell(0, 10, f"Protocol: {row.get('Protocol', 'N/A')} | Confidence: {row.get('Confidence (%)', 'N/A')}%", ln=True)
            pdf.cell(0, 10, "-"*50, ln=True)

    elif report_type == "Trend":
        pdf.cell(0, 10, "Trend Report:", ln=True)
        pdf.cell(0, 10, "You can add flow count over time charts here (advanced).", ln=True)

    else:
        pdf.cell(0, 10, "Custom report type is not implemented yet.", ln=True)

    return get_pdf_bytes(pdf)

def app():
    st.title("Generate Network IDS Reports")

    results = st.session_state.get('results')
    flow_data_df = st.session_state.get('flow_data_df')

    if results is None or flow_data_df is None:
        st.warning("Please load results and flow data first.")
        return

    report_type = st.selectbox("Select Report Type", ["Summary", "Detailed", "Incident", "Trend"])

    if st.button("Generate PDF Report"):
        pdf_bytes = generate_pdf(results, flow_data_df, report_type)
        st.download_button("Download PDF Report", data=pdf_bytes, file_name=f"{report_type.lower()}_report.pdf", mime="application/pdf")
