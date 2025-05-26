import streamlit as st
import pandas as pd

def FlowTable(results):
    detailed = results.get("detailed_results", [])

    # If detailed_results is empty
    if not detailed:
        st.write("No detailed results found")
        return

    # Check if it's a list of lists (chunks)
    if isinstance(detailed[0], list):
        # Flatten chunks
        all_flows = []
        for chunk in detailed:
            all_flows.extend(chunk)
        df = pd.DataFrame(all_flows)
    else:
        # Already flat list of dicts
        df = pd.DataFrame(detailed)

    st.subheader("Network Flow Details")
    st.dataframe(df)
