import streamlit as st
import pandas as pd
import plotly.express as px

def FlowTable(results, flow_data_df):
    detailed = results.get("detailed_results", [])

    # If detailed_results is empty
    if not detailed:
        st.write("No detailed results found")
        return

    # Flatten chunks if it's a list of lists
    if isinstance(detailed[0], list):
        all_flows = []
        for chunk in detailed:
            all_flows.extend(chunk)
        preds_df = pd.DataFrame(all_flows)
    else:
        preds_df = pd.DataFrame(detailed)

    # Create merged DataFrame with prediction results
    merged_df = flow_data_df.copy()
    merged_df['Predicted Label'] = preds_df.get('predicted_label', preds_df.get('Label', 'N/A'))
    merged_df['Confidence (%)'] = preds_df.get('confidence_score', 0) * 100

    # Select and rename columns for display
    display_cols = {
        'Src IP': 'Source IP',
        'Dst IP': 'Destination IP',
        'Protocol': 'Protocol',
        'Flow Duration': 'Duration (s)',
        'Predicted Label': 'Predicted Label',
        'Confidence (%)': 'Confidence (%)',
        'Timestamp': 'Timestamp'
    }

    # Filter only the columns that exist
    cols_to_show = [col for col in display_cols.keys() if col in merged_df.columns]
    df_display = merged_df[cols_to_show].rename(columns=display_cols)

    # Format Confidence column
    df_display['Confidence (%)'] = df_display['Confidence (%)'].apply(
        lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A"
    )

    # Round Duration
    if 'Duration (s)' in df_display.columns:
        df_display['Duration (s)'] = df_display['Duration (s)'].round(2)

    # Display flow table
    st.subheader("Network Flow Details")
    st.dataframe(df_display, use_container_width=True)

    # 🚨 Identify IPs under attack
    st.subheader("🛡️ IPs Potentially Under Attack")
    malicious_flows = merged_df[merged_df['Predicted Label'] != 'Normal']

    if not malicious_flows.empty and 'Dst IP' in malicious_flows.columns:
        ip_counts = malicious_flows['Dst IP'].value_counts().reset_index()
        ip_counts.columns = ['Destination IP', 'Malicious Flow Count']
        st.dataframe(ip_counts.head(10), use_container_width=True)

        # Show alert for top destination IP
        top_ip = ip_counts.iloc[0]
        if top_ip['Malicious Flow Count'] > 5:
            st.error(f"🚨 Alert: `{top_ip['Destination IP']}` is under potential attack "
                     f"with **{top_ip['Malicious Flow Count']}** malicious flows.")
    else:
        st.success("✅ No destination IPs show signs of attack in current data.")

    # Scatter plot: Flow Duration vs Confidence
    if 'Flow Duration' in merged_df.columns and 'Confidence (%)' in merged_df.columns:
        hover_cols = [col for col in ['Src IP', 'Dst IP', 'Protocol'] if col in merged_df.columns]

        fig = px.scatter(
            merged_df,
            x='Flow Duration',
            y='Confidence (%)',
            color='Predicted Label',
            hover_data=hover_cols,
            title='Flow Duration vs Confidence Score Scatter Plot'
        )
        st.subheader("Flow Duration vs Confidence Scatter Plot")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Required columns for scatter plot not found.")
