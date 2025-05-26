import streamlit as st
from components.FileUploader import FileUploader
from components.ResultCard import ResultCard
from components.PieChart import PieChart
from components.FlowTable import FlowTable

def Upload():
    st.header("Network Flow Upload & Analysis")

    results = None
    
    def handle_results(data):
        nonlocal results
        results = data

    FileUploader(on_upload_success=handle_results)

    if results:
        st.write("DEBUG: results received:", results)  # This should not error if 'st' is imported

        total_flows = results.get("total_flows")
        if total_flows is not None:
            ResultCard(
                title="Total Flows",
                value=str(total_flows),
                subtitle="Number of flows analyzed"
            )

        attack_counts = results.get("attack_counts", {})
        if attack_counts:
            for attack, count in attack_counts.items():
                if attack is not None and count is not None:
                    ResultCard(
                        title=f"Attack Type: {attack}",
                        value=str(count),
                        subtitle="Number of detected flows"
                    )

        summary_stats = results.get("summary_stats", {})
        if summary_stats:
            avg_conf = summary_stats.get("average_confidence")
            max_conf = summary_stats.get("max_confidence")
            min_conf = summary_stats.get("min_confidence")

            if avg_conf is not None:
                ResultCard(
                    title="Average Confidence",
                    value=f"{avg_conf:.2f}",
                    subtitle="Mean prediction confidence"
                )
            if max_conf is not None:
                ResultCard(
                    title="Max Confidence",
                    value=f"{max_conf:.2f}",
                    subtitle="Highest prediction confidence"
                )
            if min_conf is not None:
                ResultCard(
                    title="Min Confidence",
                    value=f"{min_conf:.2f}",
                    subtitle="Lowest prediction confidence"
                )

        PieChart(results)
        FlowTable(results)
