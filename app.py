# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qDG5DcNxt342ctKApQtGR-jXxFb6MIZc
"""

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="SaaS MRR Forecast Dashboard", layout="wide")

# Load the forecast data
df = pd.read_csv("Best_MRR_Forecast_Final.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.title("📈 SaaS MRR Forecasting Dashboard")
st.markdown("An enterprise-grade MRR forecasting system using LightGBM, Prophet, and SARIMAX")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
segments = df["Segment"].unique()
selected_segments = st.sidebar.multiselect("Select Segment(s):", options=segments, default=list(segments))

# Filter data
df_filtered = df[df["Segment"].isin(selected_segments)]

# KPI section
latest = df_filtered.sort_values("Date").groupby("Segment").tail(1)
col1, col2, col3 = st.columns(3)
col1.metric("Latest Forecasted MRR", f"${latest['Hybrid_Predicted_MRR'].sum():,.0f}")
col2.metric("Latest Actual MRR", f"${latest['Actual_MRR'].sum():,.0f}")
col3.metric("MAE", f"${(df_filtered['Actual_MRR'] - df_filtered['Hybrid_Predicted_MRR']).abs().mean():,.0f}")

# Line chart
st.subheader("📊 Actual vs Forecasted MRR")
fig = px.line(
    df_filtered,
    x="Date",
    y=["Actual_MRR", "Hybrid_Predicted_MRR"],
    color_discrete_map={"Actual_MRR": "black", "Hybrid_Predicted_MRR": "#1f77b4"},
    title="Monthly Actual vs Forecasted MRR"
)
fig.update_layout(xaxis_title="Date", yaxis_title="MRR ($)", legend_title="Metric", height=500)
st.plotly_chart(fig, use_container_width=True)

# Error table
st.subheader("🧮 Forecast Accuracy Table")
df_filtered["Error_%"] = 100 * abs(df_filtered["Hybrid_Predicted_MRR"] - df_filtered["Actual_MRR"]) / (df_filtered["Actual_MRR"] + 1e-8)
summary = df_filtered.groupby("Date")[["Actual_MRR", "Hybrid_Predicted_MRR", "Error_%"]].mean().reset_index()
st.dataframe(summary.style.format({"Actual_MRR": "${:,.0f}", "Hybrid_Predicted_MRR": "${:,.0f}", "Error_%": "{:.2f}%"}))

# Footer
st.markdown("---")
st.markdown("© 2025 • Built by Muhammed Swalih | [GitHub](https://github.com/swaliher/saas-mrr-forecasting)")
