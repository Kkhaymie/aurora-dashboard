# app.py
# -------------------------------------------------------
# Aurora Retail & Digital Services
# AI-Powered Executive Dashboard — Task 1
# Built with Streamlit + Plotly + Grok AI
# -------------------------------------------------------

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data_loader import (
    load_data,
    get_kpis,
    get_monthly_trend,
    get_region_performance,
    get_channel_performance,
    get_budget_vs_actual,
    get_churn_by_segment,
    get_category_performance,
    build_ai_summary,
)
from ai_insights import generate_executive_insights

# -------------------------------------------------------
# PAGE CONFIGURATION
# Must be the very first Streamlit command
# -------------------------------------------------------
st.set_page_config(
    page_title="Aurora Executive Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# CUSTOM CSS — Professional dark-accented styling
# -------------------------------------------------------
st.markdown("""
    <style>
    /* Main background */
    .main { background-color: #f4f6f9; }

    /* KPI card styling */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 5px solid #4f46e5;
        margin-bottom: 10px;
    }
    .kpi-label {
        font-size: 13px;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin: 4px 0;
    }
    .kpi-delta {
        font-size: 13px;
        color: #6b7280;
    }

    /* Section headers */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #1f2937;
        margin: 24px 0 12px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #e5e7eb;
    }

    /* AI insight box */
    .ai-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 24px;
        color: white;
        margin-top: 10px;
    }

    /* Sidebar */
    .css-1d391kg { background-color: #1e1e2e; }
    </style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# LOAD DATA (cached so it only loads once per session)
# -------------------------------------------------------
@st.cache_data
def cached_load():
    return load_data()

df_raw = cached_load()


# -------------------------------------------------------
# SIDEBAR — FILTERS
# All charts and KPIs react to these filters
# -------------------------------------------------------
with st.sidebar:
    st.image("https://via.placeholder.com/200x60/4f46e5/ffffff?text=Aurora+Dashboard",
             use_column_width=True)
    st.markdown("## 🔽 Filters")

    # Year filter
    years = sorted(df_raw["year"].unique(), reverse=True)
    selected_years = st.multiselect(
        "📅 Year",
        options=years,
        default=years,
    )

    # Region filter
    regions = sorted(df_raw["region"].unique())
    selected_regions = st.multiselect(
        "🗺️ Region",
        options=regions,
        default=regions,
    )

    # Channel filter
    channels = sorted(df_raw["channel"].unique())
    selected_channels = st.multiselect(
        "📡 Channel",
        options=channels,
        default=channels,
    )

    # Customer Segment filter
    segments = sorted(df_raw["customer_segment"].unique())
    selected_segments = st.multiselect(
        "👥 Customer Segment",
        options=segments,
        default=segments,
    )

    # Category filter
    categories = sorted(df_raw["category"].unique())
    selected_categories = st.multiselect(
        "📦 Product Category",
        options=categories,
        default=categories,
    )

    st.markdown("---")
    st.caption("Aurora Retail & Digital Services Ltd.")
    st.caption("AI-Powered Executive Dashboard")


# -------------------------------------------------------
# APPLY FILTERS TO DATAFRAME
# -------------------------------------------------------
df = df_raw[
    (df_raw["year"].isin(selected_years)) &
    (df_raw["region"].isin(selected_regions)) &
    (df_raw["channel"].isin(selected_channels)) &
    (df_raw["customer_segment"].isin(selected_segments)) &
    (df_raw["category"].isin(selected_categories))
]

# Guard against empty filtered data
if df.empty:
    st.warning("⚠️ No data matches your current filters. Please adjust the sidebar filters.")
    st.stop()


# -------------------------------------------------------
# CALCULATE ALL METRICS FROM FILTERED DATA
# -------------------------------------------------------
kpis = get_kpis(df)
trend_df = get_monthly_trend(df)
region_df = get_region_performance(df)
channel_df = get_channel_performance(df)
budget_df = get_budget_vs_actual(df)
churn_df = get_churn_by_segment(df)
category_df = get_category_performance(df)


# -------------------------------------------------------
# DASHBOARD HEADER
# -------------------------------------------------------
st.markdown("""
    <h1 style='color:#1f2937; font-size:32px; font-weight:800; margin-bottom:0;'>
    🌐 Aurora Retail & Digital Services
    </h1>
    <p style='color:#6b7280; font-size:16px; margin-top:4px;'>
    AI-Powered Executive Dashboard • Real-time Business Intelligence
    </p>
    <hr style='border:1px solid #e5e7eb; margin:16px 0;'>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# ROW 1 — KPI CARDS (6 cards across the top)
# -------------------------------------------------------
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>',
            unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">${kpis['total_revenue']/1e6:.1f}M</div>
            <div class="kpi-delta">All channels combined</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    margin_color = "#10b981" if kpis['profit_margin'] >= 20 else "#ef4444"
    st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{margin_color};">
            <div class="kpi-label">Total Profit</div>
            <div class="kpi-value">${kpis['total_profit']/1e6:.1f}M</div>
            <div class="kpi-delta">Margin: {kpis['profit_margin']:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    attainment_color = "#10b981" if kpis['budget_attainment'] >= 100 else "#f59e0b"
    st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{attainment_color};">
            <div class="kpi-label">Budget Attainment</div>
            <div class="kpi-value">{kpis['budget_attainment']:.1f}%</div>
            <div class="kpi-delta">Variance: ${kpis['revenue_variance']/1e6:.1f}M</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Customers</div>
            <div class="kpi-value">{kpis['total_customers']:,}</div>
            <div class="kpi-delta">Unique customers</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    churn_color = "#ef4444" if kpis['churn_rate'] > 15 else "#f59e0b"
    st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{churn_color};">
            <div class="kpi-label">Churn Rate</div>
            <div class="kpi-value">{kpis['churn_rate']:.1f}%</div>
            <div class="kpi-delta">{kpis['churned_customers']:,} churned</div>
        </div>
    """, unsafe_allow_html=True)

with col6:
    sentiment_color = "#10b981" if kpis['avg_sentiment'] >= 0 else "#ef4444"
    st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{sentiment_color};">
            <div class="kpi-label">Avg Sentiment</div>
            <div class="kpi-value">{kpis['avg_sentiment']:.2f}</div>
            <div class="kpi-delta">Scale: -1 to +1</div>
        </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------
# ROW 2 — REVENUE & PROFIT TREND + BUDGET VS ACTUAL
# -------------------------------------------------------
st.markdown('<div class="section-header">📉 Revenue & Profit Trends</div>',
            unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    # Monthly revenue and profit trend line chart
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_df["month_period"],
        y=trend_df["revenue"],
        name="Revenue",
        line=dict(color="#4f46e5", width=3),
        fill="tozeroy",
        fillcolor="rgba(79,70,229,0.08)",
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend_df["month_period"],
        y=trend_df["profit"],
        name="Profit",
        line=dict(color="#10b981", width=2.5, dash="dot"),
    ))
    fig_trend.update_layout(
        title="Monthly Revenue vs Profit",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        legend=dict(orientation="h", y=1.1),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=340,
        margin=dict(l=20, r=20, t=50, b=40),
        xaxis=dict(tickangle=-45, showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    # Budget vs Actual by Department — horizontal bar
    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(
        y=budget_df["department"],
        x=budget_df["budgeted"],
        name="Budgeted",
        orientation="h",
        marker_color="#e5e7eb",
    ))
    fig_budget.add_trace(go.Bar(
        y=budget_df["department"],
        x=budget_df["actual"],
        name="Actual",
        orientation="h",
        marker_color="#4f46e5",
    ))
    fig_budget.update_layout(
        title="Budget vs Actual by Dept",
        barmode="overlay",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=340,
        margin=dict(l=20, r=20, t=50, b=40),
        legend=dict(orientation="h", y=1.1),
        xaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_budget, use_container_width=True)


# -------------------------------------------------------
# ROW 3 — REGION + CHANNEL + CATEGORY PERFORMANCE
# -------------------------------------------------------
st.markdown('<div class="section-header">🗺️ Performance by Region, Channel & Category</div>',
            unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)

with col_a:
    # Revenue by Region — filled bar chart
    fig_region = px.bar(
        region_df,
        x="region",
        y="revenue",
        color="region",
        title="Revenue by Region",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig_region.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=300,
        margin=dict(l=10, r=10, t=50, b=30),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col_b:
    # Revenue by Channel — donut chart
    fig_channel = px.pie(
        channel_df,
        names="channel",
        values="revenue",
        title="Revenue by Channel",
        hole=0.5,
        color_discrete_sequence=["#4f46e5", "#10b981", "#f59e0b"],
    )
    fig_channel.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=30),
        paper_bgcolor="white",
    )
    fig_channel.update_traces(textposition="outside", textinfo="percent+label")
    st.plotly_chart(fig_channel, use_container_width=True)

with col_c:
    # Revenue by Product Category — horizontal bar
    fig_cat = px.bar(
        category_df,
        x="revenue",
        y="category",
        orientation="h",
        title="Revenue by Category",
        text_auto=".2s",
        color="revenue",
        color_continuous_scale="Blues",
    )
    fig_cat.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=300,
        margin=dict(l=10, r=10, t=50, b=30),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
    )
    st.plotly_chart(fig_cat, use_container_width=True)


# -------------------------------------------------------
# ROW 4 — CHURN ANALYSIS
# -------------------------------------------------------
st.markdown('<div class="section-header">⚠️ Customer Churn Analysis</div>',
            unsafe_allow_html=True)

col_churn1, col_churn2 = st.columns([1, 2])

with col_churn1:
    # Churn pie chart
    churn_summary = df.groupby("churn_flag")["customer_id"].nunique().reset_index()
    churn_summary.columns = ["Status", "Customers"]
    churn_summary["Status"] = churn_summary["Status"].map(
        {"Yes": "Churned", "No": "Retained"}
    )
    fig_churn_pie = px.pie(
        churn_summary,
        names="Status",
        values="Customers",
        title="Overall Churn Rate",
        hole=0.6,
        color="Status",
        color_discrete_map={"Churned": "#ef4444", "Retained": "#10b981"},
    )
    fig_churn_pie.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=30),
        paper_bgcolor="white",
    )
    st.plotly_chart(fig_churn_pie, use_container_width=True)

with col_churn2:
    # Churn by segment — grouped bar
    fig_churn_seg = px.bar(
        churn_df,
        x="customer_segment",
        y="customers",
        color="churn_flag",
        barmode="group",
        title="Churn vs Retention by Customer Segment",
        color_discrete_map={"Yes": "#ef4444", "No": "#10b981"},
        labels={"churn_flag": "Churn Status", "customers": "Customers"},
    )
    fig_churn_seg.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=300,
        margin=dict(l=10, r=10, t=50, b=30),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
    )
    st.plotly_chart(fig_churn_seg, use_container_width=True)


# -------------------------------------------------------
# ROW 5 — AI-GENERATED EXECUTIVE INSIGHTS
# -------------------------------------------------------
st.markdown('<div class="section-header">🤖 AI-Generated Executive Insights (Powered by Grok)</div>',
            unsafe_allow_html=True)

st.info("Click the button below to generate a fresh AI insight report based on the currently filtered data.")

if st.button("🚀 Generate Executive Insights", type="primary", use_container_width=True):
    with st.spinner("🤖 Grok AI is analyzing your business data..."):
        # Build the data summary from current filtered data
        ai_summary = build_ai_summary(kpis, region_df, channel_df, budget_df, churn_df)

        # Send to Grok and get insights back
        insights = generate_executive_insights(ai_summary)

    # Display insights in a styled container
    st.markdown("### 📋 Executive Insight Report")
    st.markdown(insights)

    # Download button for the insight report
    st.download_button(
        label="📥 Download Insight Report",
        data=insights,
        file_name="aurora_executive_insights.txt",
        mime="text/plain",
    )


# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:#9ca3af; font-size:13px; padding:10px;'>
    Aurora Retail & Digital Services Ltd. •
    AI-Powered Executive Dashboard •
    Built with Streamlit & Grok AI
    </div>
""", unsafe_allow_html=True)
