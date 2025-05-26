# components/PieChart.py

import streamlit as st
import pandas as pd
import altair as alt

def PieChart(data: dict, title: str = "Attack Type Distribution"):
    df = pd.DataFrame({
        "Label": list(data.keys()),
        "Count": list(data.values())
    })

    chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Label", type="nominal"),
        tooltip=["Label", "Count"]
    ).properties(
        width=400,
        height=400,
        title=title
    )

    st.altair_chart(chart, use_container_width=True)
