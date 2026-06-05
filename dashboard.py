import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aurora | Executive Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: #0d1120 !important;
    border-right: 1px solid #1e2540 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 2rem 3rem !important; }

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, #0f1629 0%, #1a2040 50%, #0f1629 100%);
    border: 1px solid #1e2d5a;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(167,139,250,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    color: #63b3ed;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.4rem;
    color: #f0f4ff;
    margin: 0 0 0.4rem 0;
    line-height: 1.15;
}
.hero-sub {
    font-size: 0.9rem;
    color: #7a85a3;
    font-weight: 300;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: #111827;
    border: 1px solid #1e2540;
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.blue::before   { background: linear-gradient(90deg, #3b82f6, #63b3ed); }
.kpi-card.green::before  { background: linear-gradient(90deg, #10b981, #34d399); }
.kpi-card.purple::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.kpi-card.amber::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.kpi-card.red::before    { background: linear-gradient(90deg, #ef4444, #f87171); }
.kpi-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4b5680;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #f0f4ff;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-sub {
    font-size: 0.72rem;
    color: #4b5680;
}
.kpi-positive { color: #34d399 !important; }
.kpi-negative { color: #f87171 !important; }
.kpi-neutral  { color: #fbbf24 !important; }

/* ── Section Headers ── */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #c8d0e8;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2540;
}

/* ── Insight Box ── */
.insight-box {
    background: linear-gradient(135deg, #0f1a2e, #111827);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    padding: 1.5rem;
    font-size: 0.9rem;
    line-height: 1.8;
    color: #c8d0e8;
    white-space: pre-wrap;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] p {
    color: #7a85a3 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #161d30 !important;
    border: 1px solid #1e2540 !important;
    color: #e8eaf0 !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Divider ── */
hr { border-color: #1e2540 !important; }

/* ── Plotly chart backgrounds ── */
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ─────────────────────────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#7a85a3', size=11),
    xaxis=dict(gridcolor='#1e2540', linecolor='#1e2540', tickcolor='#1e2540'),
    yaxis=dict(gridcolor='#1e2540', linecolor='#1e2540', tickcolor='#1e2540'),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#c8d0e8')),
    margin=dict(l=20, r=20, t=40, b=20),
    title_font=dict(family='DM Serif Display', color='#c8d0e8', size=15),
)
PALETTE = ['#3b82f6','#8b5cf6','#10b981','#f59e0b','#ef4444','#06b6d4']

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("aurora_clean.csv")
    sales = df.drop_duplicates(subset='transaction_id').copy()
    budget = df.copy()
    return df, sales, budget

df, sales_df, budget_df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ◈ Aurora Analytics")
    st.markdown("---")
    st.markdown("**FILTERS**")

    regions  = ["All"] + sorted(sales_df['region'].dropna().unique().tolist())
    channels = ["All"] + sorted(sales_df['channel'].dropna().unique().tolist())
    segments = ["All"] + sorted(sales_df['customer_segment'].dropna().unique().tolist())
    years    = ["All"] + sorted(sales_df['year'].dropna().unique().astype(str).tolist())

    sel_region  = st.selectbox("Region",   regions)
    sel_channel = st.selectbox("Channel",  channels)
    sel_segment = st.selectbox("Segment",  segments)
    sel_year    = st.selectbox("Year",     years)

    st.markdown("---")
    st.markdown("<span style='font-size:0.7rem;color:#2d3655'>Aurora Retail & Digital Services<br>Gen AI for Data Analysts Project</span>", unsafe_allow_html=True)

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = sales_df.copy()
if sel_region  != "All": filtered = filtered[filtered['region'] == sel_region]
if sel_channel != "All": filtered = filtered[filtered['channel'] == sel_channel]
if sel_segment != "All": filtered = filtered[filtered['customer_segment'] == sel_segment]
if sel_year    != "All": filtered = filtered[filtered['year'] == int(sel_year)]

fbudget = budget_df.copy()
if sel_year != "All": fbudget = fbudget[fbudget['year'] == int(sel_year)]

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_revenue       = filtered['revenue'].sum()
total_profit        = filtered['profit'].sum()
profit_margin       = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_budgeted      = fbudget['budgeted_revenue'].sum()
total_actual        = fbudget['actual_revenue'].sum()
budget_variance_pct = ((total_actual - total_budgeted) / total_budgeted * 100) if total_budgeted > 0 else 0
churn_rate          = filtered['churn_flag'].value_counts(normalize=True).get('Yes', 0) * 100
best_region         = filtered.groupby('region')['revenue'].sum().idxmax() if not filtered.empty else "N/A"
best_channel        = filtered.groupby('channel')['revenue'].sum().idxmax() if not filtered.empty else "N/A"

# ── Hero ──────────────────────────────────────────────────────────────────────
filter_label = " · ".join([x for x in [
    sel_region if sel_region != "All" else None,
    sel_channel if sel_channel != "All" else None,
    sel_segment if sel_segment != "All" else None,
    sel_year if sel_year != "All" else None,
] if x])
filter_label = filter_label or "All Regions · All Channels · All Segments · 2021–2024"

st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Executive Intelligence Dashboard</div>
    <div class="hero-title">Aurora Retail & Digital Services</div>
    <div class="hero-sub">Viewing: {filter_label}</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
bv_class = "kpi-positive" if budget_variance_pct >= 0 else "kpi-negative"
bv_sign  = "+" if budget_variance_pct >= 0 else ""
cr_class = "kpi-negative" if churn_rate > 25 else "kpi-neutral"

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card blue">
    <div class="kpi-label">Total Revenue</div>
    <div class="kpi-value">${total_revenue/1e6:.2f}M</div>
    <div class="kpi-sub">Gross sales (deduplicated)</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">Total Profit</div>
    <div class="kpi-value">${total_profit/1e6:.2f}M</div>
    <div class="kpi-sub">{profit_margin:.1f}% profit margin</div>
  </div>
  <div class="kpi-card purple">
    <div class="kpi-label">Profit Margin</div>
    <div class="kpi-value">{profit_margin:.1f}%</div>
    <div class="kpi-sub">Revenue to profit ratio</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-label">vs Budget</div>
    <div class="kpi-value {bv_class}">{bv_sign}{budget_variance_pct:.1f}%</div>
    <div class="kpi-sub">Actual vs budgeted revenue</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-label">Churn Rate</div>
    <div class="kpi-value {cr_class}">{churn_rate:.1f}%</div>
    <div class="kpi-sub">{int(filtered['churn_flag'].eq('Yes').sum()):,} customers lost</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Revenue Performance</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    rev_region = filtered.groupby('region')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
    fig = go.Figure(go.Bar(
        x=rev_region['revenue'], y=rev_region['region'],
        orientation='h',
        marker=dict(color=PALETTE[:len(rev_region)], line=dict(width=0)),
        text=[f"${v/1e6:.2f}M" for v in rev_region['revenue']],
        textposition='outside', textfont=dict(color='#c8d0e8', size=11)
    ))
    fig.update_layout(**CHART_THEME, title='Revenue by Region', height=280)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    rev_chan = filtered.groupby('channel')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
    fig = go.Figure(go.Bar(
        x=rev_chan['revenue'], y=rev_chan['channel'],
        orientation='h',
        marker=dict(color=PALETTE[1:4], line=dict(width=0)),
        text=[f"${v/1e6:.2f}M" for v in rev_chan['revenue']],
        textposition='outside', textfont=dict(color='#c8d0e8', size=11)
    ))
    fig.update_layout(**CHART_THEME, title='Revenue by Channel', height=280)
    st.plotly_chart(fig, use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Profitability & Customer Health</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    seg_profit = filtered.groupby('customer_segment')['profit'].sum().reset_index()
    fig = go.Figure(go.Bar(
        x=seg_profit['customer_segment'], y=seg_profit['profit'],
        marker=dict(color=PALETTE[:3], line=dict(width=0)),
        text=[f"${v/1e6:.2f}M" for v in seg_profit['profit']],
        textposition='outside', textfont=dict(color='#c8d0e8', size=11)
    ))
    fig.update_layout(**CHART_THEME, title='Profit by Customer Segment', height=300)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    churn_counts = filtered['churn_flag'].value_counts().reset_index()
    churn_counts.columns = ['Status', 'Count']
    fig = go.Figure(go.Pie(
        labels=churn_counts['Status'], values=churn_counts['Count'],
        hole=0.55,
        marker=dict(colors=['#ef4444','#10b981'], line=dict(color='#0a0e1a', width=2)),
        textfont=dict(color='#c8d0e8', size=11)
    ))
    fig.update_layout(**CHART_THEME, title='Churn vs Retained', height=300,
                      annotations=[dict(text=f"{churn_rate:.1f}%<br><span style='font-size:10px'>Churn</span>",
                                        x=0.5, y=0.5, font_size=18, showarrow=False,
                                        font=dict(color='#f0f4ff'))])
    st.plotly_chart(fig, use_container_width=True)

# ── Monthly Trend ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
monthly = filtered.groupby('month')['revenue'].sum().reset_index().sort_values('month')
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly['month'], y=monthly['revenue'],
    mode='lines+markers',
    line=dict(color='#3b82f6', width=2.5),
    marker=dict(size=5, color='#63b3ed'),
    fill='tozeroy',
    fillcolor='rgba(59,130,246,0.08)'
))
fig.update_layout(**CHART_THEME, title='Monthly Revenue Trend (2021–2024)', height=300)
fig.update_xaxes(tickangle=45, nticks=20)
st.plotly_chart(fig, use_container_width=True)

# ── AI Insights ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">AI Executive Briefing</div>', unsafe_allow_html=True)
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")

def get_ai_insights(kpis):
    prompt = f"""You are a senior business analyst preparing an executive briefing for Aurora Retail & Digital Services.

Current Performance:
- Total Revenue: ${kpis['total_revenue']:,.0f}
- Total Profit: ${kpis['total_profit']:,.0f}
- Profit Margin: {kpis['profit_margin']:.1f}%
- Revenue vs Budget: {kpis['budget_variance_pct']:+.1f}%
- Churn Rate: {kpis['churn_rate']:.1f}%
- Best Region: {kpis['best_region']}
- Best Channel: {kpis['best_channel']}

Write a 3-paragraph executive summary:
1. Overall performance assessment
2. Key risks and concerns
3. Recommended actions

Keep it jargon-free and suitable for a non-technical executive audience."""

    r = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
        json={"model": "mistral-small-latest",
              "messages": [{"role": "user", "content": prompt}],
              "max_tokens": 600}
    )
    return r.json()['choices'][0]['message']['content']

if st.button("⚡ Generate AI Executive Summary"):
    if not MISTRAL_API_KEY:
        st.error("Set your MISTRAL_API_KEY environment variable first.")
    else:
        with st.spinner("Analysing performance data..."):
            kpis_dict = dict(total_revenue=total_revenue, total_profit=total_profit,
                             profit_margin=profit_margin, budget_variance_pct=budget_variance_pct,
                             churn_rate=churn_rate, best_region=best_region, best_channel=best_channel)
            insights = get_ai_insights(kpis_dict)
        st.markdown(f'<div class="insight-box">{insights}</div>', unsafe_allow_html=True)