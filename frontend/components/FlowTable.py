import streamlit as st
import pandas as pd

def FlowTable(results, flow_data_df):
    detailed = results.get("detailed_results", [])

    # If detailed_results empty
    if not detailed:
        st.write("No detailed results found")
        return

    # Flatten chunks if list of lists
    if isinstance(detailed[0], list):
        all_flows = []
        for chunk in detailed:
            all_flows.extend(chunk)
        preds_df = pd.DataFrame(all_flows)
    else:
        preds_df = pd.DataFrame(detailed)

    # Make sure preds_df has 'predicted_label' and 'confidence' columns or adapt to your keys
    # Example column names in preds_df: 'predicted_label', 'confidence'

    # Merge flow data with prediction results on a unique key
    # Here, let's assume order matches or you can merge on a flow ID if available

    # If both dataframes have the same length and order:
    merged_df = flow_data_df.copy()
    merged_df['Predicted Label'] = preds_df.get('predicted_label', preds_df.get('Label', 'N/A'))
    merged_df['Confidence (%)'] = preds_df.get('confidence', 0) * 100

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

    # Filter columns that exist in merged_df
    cols_to_show = [col for col in display_cols.keys() if col in merged_df.columns]

    df_display = merged_df[cols_to_show].rename(columns=display_cols)

    # Format Confidence
    df_display['Confidence (%)'] = df_display['Confidence (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")

    # Round Duration
    if 'Duration (s)' in df_display.columns:
        df_display['Duration (s)'] = df_display['Duration (s)'].round(2)

    st.subheader("Network Flow Details")
    st.dataframe(df_display, use_container_width=True)
