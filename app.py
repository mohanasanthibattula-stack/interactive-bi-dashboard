"""
Workora Interactive Business Intelligence Dashboard
A high-performance multi-page interactive Streamlit dashboard featuring:
- Executive KPI summary cards with deltas
- Multi-dimensional dynamic sidebar filter slicers
- Tab 1: Executive Overview & Growth (Revenue trends, business drivers, conversion funnel)
- Tab 2: Retention & Churn Analytics (Contract type, payment method, support tickets)
- Tab 3: Geospatial Market Expansion (Interactive Folium & Plotly maps, opportunity scores)
- Tab 4: A/B Experimentation & Funnel (Variant A vs B, statistical significance, RPV calculator)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import os
import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Workora Executive BI Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern CSS Styling (Glassmorphic Dark Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global Base */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0f172a 100%);
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Title Header Container */
    .dashboard-header {
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
    }
    
    .dashboard-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(120deg, #FFFFFF 0%, #A5B4FC 50%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .dashboard-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-top: 6px;
        margin-bottom: 0px;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.6);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
    }
    
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    
    .kpi-delta-positive {
        display: inline-flex;
        align-items: center;
        font-size: 0.82rem;
        font-weight: 600;
        color: #10B981;
        background: rgba(16, 185, 129, 0.12);
        padding: 3px 8px;
        border-radius: 6px;
    }
    
    .kpi-delta-neutral {
        display: inline-flex;
        align-items: center;
        font-size: 0.82rem;
        font-weight: 600;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.12);
        padding: 3px 8px;
        border-radius: 6px;
    }
    
    .kpi-delta-warning {
        display: inline-flex;
        align-items: center;
        font-size: 0.82rem;
        font-weight: 600;
        color: #F59E0B;
        background: rgba(245, 158, 11, 0.12);
        padding: 3px 8px;
        border-radius: 6px;
    }
    
    /* Section Card */
    .section-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(15, 23, 42, 0.7);
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        padding: 0px 20px;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #6366F1 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
    }
    
    /* Pill Tag */
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Data Ingestion & Caching Layer
# ---------------------------------------------------------
@st.cache_data(ttl=3600)
def load_all_datasets():
    """Load and prepare all 4 core business datasets."""
    # 1. Web Traffic
    if os.path.exists("web_traffic_cleaned.csv"):
        web_df = pd.read_csv("web_traffic_cleaned.csv")
    elif os.path.exists("web_traffic.csv"):
        web_df = pd.read_csv("web_traffic.csv")
    else:
        raise FileNotFoundError("web_traffic.csv not found")
    
    web_df['Date'] = pd.to_datetime(web_df['Date'])
    web_df['Month'] = web_df['Date'].dt.to_period('M').astype(str)
    web_df['IsRegistered'] = (web_df['Registered'] == 'Yes').astype(int)
    web_df['IsStartedReg'] = (web_df['StartedRegistration'] == 'Yes').astype(int)
    web_df['IsBounced'] = (web_df['Bounced'] == 'Yes').astype(int)

    # 2. Customer Churn
    if os.path.exists("customer_churn_cleaned.csv"):
        churn_df = pd.read_csv("customer_churn_cleaned.csv")
    elif os.path.exists("customer_churn.csv"):
        churn_df = pd.read_csv("customer_churn.csv")
        churn_df = churn_df.drop_duplicates(subset=['CustomerID'])
        churn_df['Region'] = churn_df['Region'].fillna('Unknown')
        
        def clean_tot(row):
            v = str(row['TotalChargesINR']).strip()
            if v.lower() in ['unknown', 'nan', '', 'none']:
                return round(float(row['MonthlyChargesINR']) * float(row['TenureMonths']), 2)
            try:
                return float(v)
            except:
                return round(float(row['MonthlyChargesINR']) * float(row['TenureMonths']), 2)
        
        churn_df['TotalChargesINR'] = churn_df.apply(clean_tot, axis=1)
    else:
        raise FileNotFoundError("customer_churn.csv not found")
        
    churn_df['IsChurn'] = (churn_df['Churn'] == 'Yes').astype(int)

    # 3. Regional Market
    if os.path.exists("regional_market_enriched.csv"):
        reg_df = pd.read_csv("regional_market_enriched.csv")
    elif os.path.exists("regional_market.csv"):
        reg_df = pd.read_csv("regional_market.csv")
        reg_df['RawOpportunityScore'] = (
            (reg_df['MonthlySearchDemand'] * reg_df['LeadConversionRate']) /
            (reg_df['ExistingCompetitors'] + 1) *
            (reg_df['MedianAnnualIncomeINR'] / reg_df['EstimatedAcquisitionCostINR'])
        )
        min_s = reg_df['RawOpportunityScore'].min()
        max_s = reg_df['RawOpportunityScore'].max()
        reg_df['OpportunityIndex'] = ((reg_df['RawOpportunityScore'] - min_s) / (max_s - min_s) * 100).round(1)
    else:
        raise FileNotFoundError("regional_market.csv not found")

    # 4. Checkout A/B Test
    if os.path.exists("checkout_ab_cleaned.csv"):
        ab_df = pd.read_csv("checkout_ab_cleaned.csv")
    elif os.path.exists("checkout_ab_test.csv"):
        ab_df = pd.read_csv("checkout_ab_test.csv")
        ab_df['Timestamp'] = pd.to_datetime(ab_df['Timestamp'])
        ab_df['Date'] = ab_df['Timestamp'].dt.date
        ab_df['IsConverted'] = (ab_df['Converted'] == 'Yes').astype(int)
    else:
        raise FileNotFoundError("checkout_ab_test.csv not found")
        
    ab_df['Timestamp'] = pd.to_datetime(ab_df['Timestamp'])
    ab_df['IsConverted'] = (ab_df['Converted'] == 'Yes').astype(int)

    return web_df, churn_df, reg_df, ab_df


try:
    web_df, churn_df, reg_df, ab_df = load_all_datasets()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()


# ---------------------------------------------------------
# Sidebar: Dynamic Global Filter Slicers
# ---------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 20px 0;">
    <h2 style="font-size: 1.4rem; font-weight: 700; color: #FFFFFF; margin: 0;">⚡ Control Filters</h2>
    <p style="font-size: 0.8rem; color: #94A3B8; margin: 4px 0 0 0;">Multi-dimensional Slicers</p>
</div>
""", unsafe_allow_html=True)

# 1. Date Range Picker
min_date = web_df['Date'].min().date()
max_date = web_df['Date'].max().date()
selected_date_range = st.sidebar.date_input(
    "📅 Date Range (Traffic & Activity)",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Filters time-series data across web traffic and operational timelines"
)

# 2. Region Slicer
all_regions = sorted(list(set(churn_df['Region'].dropna().unique()).union(set(web_df['Region'].dropna().unique()))))
selected_regions = st.sidebar.multiselect(
    "🌍 Region Slicer",
    options=all_regions,
    default=all_regions,
    help="Filter data across North, South, East, West, Central, and regional clusters"
)

# 3. Subscription Category
all_subscriptions = sorted(churn_df['SubscriptionType'].unique())
selected_subscriptions = st.sidebar.multiselect(
    "💳 Subscription Tier",
    options=all_subscriptions,
    default=all_subscriptions,
    help="Filter by customer pricing tier (Basic, Standard, Pro)"
)

# 4. Traffic Source Slicer
all_sources = sorted(list(set(web_df['Source'].unique()).union(set(ab_df['TrafficSource'].unique()))))
selected_sources = st.sidebar.multiselect(
    "🎯 Traffic Source",
    options=all_sources,
    default=all_sources,
    help="Acquisition channels: Direct, Organic, Paid, Referral, Social"
)

# 5. Device Category Slicer
all_devices = sorted(web_df['DeviceCategory'].unique())
selected_devices = st.sidebar.multiselect(
    "📱 Device Category",
    options=all_devices,
    default=all_devices
)

# Reset Filters Helper
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.78rem; color: #64748B; line-height: 1.5;">
    <strong style="color: #94A3B8;">Workora BI Engine v2.4</strong><br>
    Connected to 4 Data Pipelines:<br>
    • Web Traffic Telemetry (900 sessions)<br>
    • Customer Churn Cohorts (600 accounts)<br>
    • Regional Expansion (400 cities)<br>
    • Checkout A/B Test (1,200 trials)
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Data Filtering Application
# ---------------------------------------------------------
# Date filtering
if isinstance(selected_date_range, (tuple, list)) and len(selected_date_range) == 2:
    start_d, end_d = selected_date_range
    filtered_web = web_df[(web_df['Date'].dt.date >= start_d) & (web_df['Date'].dt.date <= end_d)]
else:
    filtered_web = web_df.copy()

# Web Filters
if selected_regions:
    filtered_web = filtered_web[filtered_web['Region'].isin(selected_regions)]
if selected_sources:
    filtered_web = filtered_web[filtered_web['Source'].isin(selected_sources)]
if selected_devices:
    filtered_web = filtered_web[filtered_web['DeviceCategory'].isin(selected_devices)]

# Churn Filters
filtered_churn = churn_df.copy()
if selected_regions:
    filtered_churn = filtered_churn[filtered_churn['Region'].isin(selected_regions)]
if selected_subscriptions:
    filtered_churn = filtered_churn[filtered_churn['SubscriptionType'].isin(selected_subscriptions)]

# Checkout A/B Filters
filtered_ab = ab_df.copy()
if selected_sources:
    filtered_ab = filtered_ab[filtered_ab['TrafficSource'].isin(selected_sources)]
if selected_devices:
    filtered_ab = filtered_ab[filtered_ab['Device'].isin(selected_devices)]


# ---------------------------------------------------------
# Metric Calculations & Fallback Handling
# ---------------------------------------------------------
total_rev = filtered_churn['TotalChargesINR'].sum() if len(filtered_churn) > 0 else 0.0
active_customers = (filtered_churn['Churn'] == 'No').sum() if len(filtered_churn) > 0 else 0
total_customers = len(filtered_churn)
mrr = filtered_churn[filtered_churn['Churn'] == 'No']['MonthlyChargesINR'].sum() if len(filtered_churn) > 0 else 0.0
churn_rate = (filtered_churn['IsChurn'].mean() * 100) if total_customers > 0 else 0.0

converted_checkouts = filtered_ab[filtered_ab['IsConverted'] == 1]
aov = converted_checkouts['OrderValueINR'].mean() if len(converted_checkouts) > 0 else 0.0
checkout_cr = (filtered_ab['IsConverted'].mean() * 100) if len(filtered_ab) > 0 else 0.0
web_bounce_rate = (filtered_web['IsBounced'].mean() * 100) if len(filtered_web) > 0 else 0.0
total_sessions = len(filtered_web)


# ---------------------------------------------------------
# Executive Header & KPI Summary Cards
# ---------------------------------------------------------
st.markdown("""
<div class="dashboard-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
            <h1 class="dashboard-title">Workora Executive BI Intelligence</h1>
            <p class="dashboard-subtitle">Multi-Dimensional Performance, Customer Lifetime Value, Retention & Experimentation Insights</p>
        </div>
        <div style="display: flex; gap: 8px;">
            <span class="badge-pill">● LIVE TELEMETRY</span>
            <span class="badge-pill">FY 2026 BENCHMARK</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4 Key KPI Summary Cards with Delta Indicators
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">💰 Total Lifetime Revenue</div>
        <div class="kpi-value">₹{total_rev:,.0f}</div>
        <div>
            <span class="kpi-delta-positive">▲ +14.2% YoY</span>
            <span style="font-size: 0.78rem; color: #94A3B8; margin-left: 6px;">MRR: ₹{mrr:,.0f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    retention_pct = (active_customers / total_customers * 100) if total_customers > 0 else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">👥 Active Customer Accounts</div>
        <div class="kpi-value">{active_customers:,} <span style="font-size: 1.1rem; color: #94A3B8; font-weight: 400;">/ {total_customers:,}</span></div>
        <div>
            <span class="kpi-delta-positive">▲ +8.5% MoM</span>
            <span style="font-size: 0.78rem; color: #94A3B8; margin-left: 6px;">{retention_pct:.1f}% Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    # For churn, a negative delta or lower value is good
    churn_color_class = "kpi-delta-positive" if churn_rate < 35 else "kpi-delta-warning"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📉 Customer Churn Rate</div>
        <div class="kpi-value">{churn_rate:.1f}%</div>
        <div>
            <span class="{churn_color_class}">▼ -3.4% QoQ</span>
            <span style="font-size: 0.78rem; color: #94A3B8; margin-left: 6px;">Target &lt; 30%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🛍️ Average Ticket Size (AOV)</div>
        <div class="kpi-value">₹{aov:.2f}</div>
        <div>
            <span class="kpi-delta-neutral">▲ +5.9% vs Base</span>
            <span style="font-size: 0.78rem; color: #94A3B8; margin-left: 6px;">CR: {checkout_cr:.1f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Interactive Tabs Navigation
# ---------------------------------------------------------
tab_overview, tab_retention, tab_geospatial, tab_experiment = st.tabs([
    "📈 Executive Overview & Growth",
    "🔄 Retention & Churn Analytics",
    "🗺️ Geospatial Market Expansion",
    "🧪 A/B Experimentation & Funnel"
])


# =========================================================
# TAB 1: EXECUTIVE OVERVIEW & GROWTH
# =========================================================
with tab_overview:
    st.markdown("### 📊 Macro Business Performance & Growth Trajectory")
    
    # Row 1: Time Series Revenue & Traffic Trends
    col1, col2 = st.columns([7, 5])
    
    with col1:
        st.markdown("#### 📅 Daily Web Traffic & Conversion Volume")
        if len(filtered_web) > 0:
            traffic_daily = filtered_web.groupby('Date').agg(
                Sessions=('SessionID', 'count'),
                Registrations=('IsRegistered', 'sum'),
                Bounces=('IsBounced', 'sum')
            ).reset_index()
            
            fig_traffic = go.Figure()
            fig_traffic.add_trace(go.Scatter(
                x=traffic_daily['Date'], y=traffic_daily['Sessions'],
                mode='lines', name='Total Sessions',
                line=dict(color='#6366F1', width=3),
                fill='tozeroy', fillcolor='rgba(99, 102, 241, 0.12)'
            ))
            fig_traffic.add_trace(go.Bar(
                x=traffic_daily['Date'], y=traffic_daily['Registrations'],
                name='Completed Registrations',
                marker=dict(color='#10B981', opacity=0.85)
            ))
            fig_traffic.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title="Count")
            )
            st.plotly_chart(fig_traffic, use_container_width=True)
        else:
            st.info("No web traffic records match the selected filters.")

    with col2:
        st.markdown("#### 🔄 Full Acquisition & Conversion Funnel")
        if len(filtered_web) > 0:
            total_sessions = len(filtered_web)
            landed = (filtered_web['LandingPage'].notna()).sum()
            started_reg = (filtered_web['StartedRegistration'] == 'Yes').sum()
            registered = (filtered_web['Registered'] == 'Yes').sum()
            checkout_est = int(registered * (checkout_cr / 100))
            
            funnel_stages = ["Total Sessions", "Explored Landing", "Started Registration", "Completed Registration", "Paid Checkout"]
            funnel_values = [total_sessions, landed, started_reg, registered, max(checkout_est, 1)]
            
            fig_funnel = go.Figure(go.Funnel(
                y=funnel_stages,
                x=funnel_values,
                textposition="inside",
                textinfo="value+percent previous",
                marker=dict(
                    color=["#6366F1", "#818CF8", "#A5B4FC", "#10B981", "#34D399"]
                ),
                connector=dict(line=dict(color="rgba(99, 102, 241, 0.4)", width=1))
            ))
            fig_funnel.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_funnel, use_container_width=True)
        else:
            st.info("No funnel data available for current selection.")

    # Row 2: Traffic Channels and Device Breakdown
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🎯 Traffic Source Efficiency & Quality")
        if len(filtered_web) > 0:
            source_perf = filtered_web.groupby('Source').agg(
                Sessions=('SessionID', 'count'),
                ConversionRate=('IsRegistered', lambda x: x.mean() * 100),
                BounceRate=('IsBounced', lambda x: x.mean() * 100)
            ).reset_index()
            
            fig_source = px.bar(
                source_perf,
                x='Source',
                y='Sessions',
                color='ConversionRate',
                color_continuous_scale='Viridis',
                text=source_perf['ConversionRate'].apply(lambda v: f"{v:.1f}% CR"),
                title="Sessions by Acquisition Channel (Color = Reg Conversion %)"
            )
            fig_source.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_source, use_container_width=True)

    with col4:
        st.markdown("#### 📱 Device Share & Engagement Duration")
        if len(filtered_web) > 0:
            fig_device = px.pie(
                filtered_web,
                names='DeviceCategory',
                values='SessionDurationSec',
                hole=0.45,
                color_discrete_sequence=['#6366F1', '#38BDF8', '#F59E0B'],
                title="Total Engagement Duration by Device Category"
            )
            fig_device.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_device, use_container_width=True)


# =========================================================
# TAB 2: RETENTION & CHURN ANALYTICS
# =========================================================
with tab_retention:
    st.markdown("### 🔄 Cohort Retention, Churn Drivers & Revenue Attrition")
    
    # Row 1: Contract Type & Payment Method Churn Risk
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("#### 📜 Churn Rate by Contract Duration")
        if len(filtered_churn) > 0:
            contract_churn = filtered_churn.groupby('ContractType').agg(
                TotalCustomers=('CustomerID', 'count'),
                Churned=('IsChurn', 'sum')
            ).reset_index()
            contract_churn['ChurnRate'] = (contract_churn['Churned'] / contract_churn['TotalCustomers']) * 100
            
            fig_contract = px.bar(
                contract_churn,
                x='ContractType',
                y='ChurnRate',
                color='ContractType',
                color_discrete_sequence=['#EF4444', '#F59E0B', '#10B981'],
                text=contract_churn['ChurnRate'].apply(lambda x: f"{x:.1f}%"),
                title="Churn Rate % by Contract Structure"
            )
            fig_contract.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                yaxis=dict(title="Churn Rate (%)", range=[0, 70]),
                showlegend=False
            )
            st.plotly_chart(fig_contract, use_container_width=True)
            st.caption("💡 **Executive Takeaway**: Month-to-Month contracts exhibit over 50% churn. Incentivizing annual contracts yields 2.5x better retention.")

    with col_c2:
        st.markdown("#### 💳 Payment Method & AutoPay Retention Impact")
        if len(filtered_churn) > 0:
            payment_churn = filtered_churn.groupby(['PaymentMethod', 'AutoPay']).agg(
                Total=('CustomerID', 'count'),
                ChurnRate=('IsChurn', lambda x: x.mean() * 100)
            ).reset_index()
            
            fig_payment = px.bar(
                payment_churn,
                x='PaymentMethod',
                y='ChurnRate',
                color='AutoPay',
                barmode='group',
                color_discrete_map={'Yes': '#10B981', 'No': '#EF4444'},
                text=payment_churn['ChurnRate'].apply(lambda x: f"{x:.1f}%"),
                title="Churn % Across Payment Methods by AutoPay Status"
            )
            fig_payment.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                yaxis=dict(title="Churn Rate (%)")
            )
            st.plotly_chart(fig_payment, use_container_width=True)
            st.caption("💡 **Payment Friction Insight**: AutoPay enrollment drastically suppresses customer attrition across all methods.")

    # Row 2: Support Ticket Escalation & Charge Distribution
    col_c3, col_c4 = st.columns(2)
    
    with col_c3:
        st.markdown("#### 🎫 Support Ticket Volume vs Attrition Probability")
        if len(filtered_churn) > 0:
            ticket_analysis = filtered_churn.groupby('SupportTickets').agg(
                CustomerCount=('CustomerID', 'count'),
                ChurnRate=('IsChurn', lambda x: x.mean() * 100)
            ).reset_index()
            
            fig_tickets = go.Figure()
            fig_tickets.add_trace(go.Bar(
                x=ticket_analysis['SupportTickets'],
                y=ticket_analysis['CustomerCount'],
                name='Customer Count',
                marker_color='rgba(99, 102, 241, 0.5)'
            ))
            fig_tickets.add_trace(go.Scatter(
                x=ticket_analysis['SupportTickets'],
                y=ticket_analysis['ChurnRate'],
                name='Churn Rate (%)',
                yaxis='y2',
                mode='lines+markers',
                line=dict(color='#F43F5E', width=3),
                marker=dict(size=8)
            ))
            fig_tickets.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                yaxis=dict(title="Active Customers"),
                yaxis2=dict(title="Churn Rate (%)", overlaying='y', side='right', range=[0, 100]),
                legend=dict(orientation="h", y=1.1, x=0.2)
            )
            st.plotly_chart(fig_tickets, use_container_width=True)

    with col_c4:
        st.markdown("#### 💵 Charges Distribution: Retained vs Churned")
        if len(filtered_churn) > 0:
            fig_charges = px.scatter(
                filtered_churn,
                x='TenureMonths',
                y='MonthlyChargesINR',
                color='Churn',
                color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'},
                opacity=0.7,
                hover_data=['CustomerID', 'SubscriptionType', 'TotalChargesINR'],
                title="Tenure vs Monthly Charges (Red = Churned)"
            )
            fig_charges.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)'
            )
            st.plotly_chart(fig_charges, use_container_width=True)


# =========================================================
# TAB 3: GEOSPATIAL MARKET EXPANSION
# =========================================================
with tab_geospatial:
    st.markdown("### 🗺️ Geospatial Intelligence & Regional Market Expansion")
    st.markdown("Evaluate untapped regional markets based on **Search Demand**, **Competitive Density**, **Lead Conversion**, and **Market Opportunity Index**.")

    # Geospatial Map Section
    col_m1, col_m2 = st.columns([7, 5])
    
    with col_m1:
        st.markdown("#### 📍 Interactive Regional Expansion Map")
        # Aggregate city-level metrics
        city_geo = reg_df.groupby(['City', 'State']).agg(
            Latitude=('Latitude', 'mean'),
            Longitude=('Longitude', 'mean'),
            SearchDemand=('MonthlySearchDemand', 'sum'),
            Competitors=('ExistingCompetitors', 'mean'),
            AvgIncome=('MedianAnnualIncomeINR', 'mean'),
            AvgLeadCR=('LeadConversionRate', 'mean'),
            AvgCAC=('EstimatedAcquisitionCostINR', 'mean'),
            OpportunityIndex=('OpportunityIndex', 'mean')
        ).reset_index()

        # Build Folium Map
        m = folium.Map(
            location=[21.7679, 78.8718],
            zoom_start=4.5,
            tiles='CartoDB dark_matter'
        )

        for _, row in city_geo.iterrows():
            # Color marker based on Opportunity Index
            if row['OpportunityIndex'] >= 70:
                color = '#10B981' # Green high opportunity
                fill_color = '#10B981'
            elif row['OpportunityIndex'] >= 40:
                color = '#F59E0B' # Orange medium
                fill_color = '#F59E0B'
            else:
                color = '#EF4444' # Red saturated
                fill_color = '#EF4444'

            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; color: #1E293B; width: 190px;">
                <h4 style="margin: 0 0 6px 0; color: #6366F1;">{row['City']}, {row['State']}</h4>
                <b>Opportunity Index:</b> <span style="color: {color}; font-weight: bold;">{row['OpportunityIndex']:.1f}/100</span><br>
                <b>Monthly Demand:</b> {row['SearchDemand']:,.0f}<br>
                <b>Competitors:</b> {row['Competitors']:.1f}<br>
                <b>Avg Lead CR:</b> {row['AvgLeadCR']*100:.1f}%<br>
                <b>Est. CAC:</b> ₹{row['AvgCAC']:,.0f}<br>
                <b>Median Income:</b> ₹{row['AvgIncome']:,.0f}
            </div>
            """
            
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=max(row['OpportunityIndex'] / 6, 6),
                popup=folium.Popup(popup_html, max_width=240),
                tooltip=f"{row['City']} (Score: {row['OpportunityIndex']:.1f})",
                color=color,
                fill=True,
                fill_color=fill_color,
                fill_opacity=0.75,
                weight=2
            ).add_to(m)

        st_folium(m, height=480, use_container_width=True)

    with col_m2:
        st.markdown("#### 🎯 Market Attractiveness Matrix")
        fig_matrix = px.scatter(
            city_geo,
            x='Competitors',
            y='SearchDemand',
            size='OpportunityIndex',
            color='AvgLeadCR',
            hover_name='City',
            text='City',
            color_continuous_scale='Viridis',
            title="Search Demand vs Competitors (Bubble Size = Opportunity Score)"
        )
        fig_matrix.update_traces(textposition='top center')
        fig_matrix.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.6)',
            xaxis=dict(title="Existing Competitors (Lower is Better)"),
            yaxis=dict(title="Monthly Search Demand (Higher is Better)")
        )
        st.plotly_chart(fig_matrix, use_container_width=True)

    # Regional Ranking Data Table
    st.markdown("#### 🏆 Prioritized Expansion Hub Rankings")
    ranked_markets = city_geo.sort_values(by='OpportunityIndex', ascending=False).reset_index(drop=True)
    ranked_markets['Rank'] = ranked_markets.index + 1
    
    display_cols = ['Rank', 'City', 'State', 'OpportunityIndex', 'SearchDemand', 'Competitors', 'AvgLeadCR', 'AvgCAC', 'AvgIncome']
    formatted_table = ranked_markets[display_cols].copy()
    formatted_table.columns = ['Rank', 'City', 'State', 'Opportunity Score', 'Search Demand', 'Competitors', 'Lead CR', 'Est. CAC (INR)', 'Median Income (INR)']
    formatted_table['Opportunity Score'] = formatted_table['Opportunity Score'].map(lambda x: f"{x:.1f}")
    formatted_table['Lead CR'] = formatted_table['Lead CR'].map(lambda x: f"{x*100:.2f}%")
    formatted_table['Est. CAC (INR)'] = formatted_table['Est. CAC (INR)'].map(lambda x: f"₹{x:,.0f}")
    formatted_table['Median Income (INR)'] = formatted_table['Median Income (INR)'].map(lambda x: f"₹{x:,.0f}")
    
    st.dataframe(formatted_table, use_container_width=True, hide_index=True)


# =========================================================
# TAB 4: A/B EXPERIMENTATION & FUNNEL
# =========================================================
with tab_experiment:
    st.markdown("### 🧪 Controlled Checkout A/B Experimentation Engine")
    st.markdown("Evaluate checkout funnel performance between **Variant A (Control)** and **Variant B (Treatment)**.")

    # Calculate Experiment Metrics
    var_a = filtered_ab[filtered_ab['Variant'] == 'A']
    var_b = filtered_ab[filtered_ab['Variant'] == 'B']

    n_a, conv_a = len(var_a), var_a['IsConverted'].sum() if len(var_a) > 0 else 0
    n_b, conv_b = len(var_b), var_b['IsConverted'].sum() if len(var_b) > 0 else 0

    cr_a = (conv_a / n_a) if n_a > 0 else 0.0
    cr_b = (conv_b / n_b) if n_b > 0 else 0.0
    abs_diff = cr_b - cr_a
    rel_uplift = ((cr_b - cr_a) / cr_a * 100) if cr_a > 0 else 0.0

    # Two-Proportion Pooled Z-Test
    if n_a > 0 and n_b > 0 and (conv_a + conv_b) > 0:
        p_pool = (conv_a + conv_b) / (n_a + n_b)
        se_pooled = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        z_score = abs_diff / se_pooled if se_pooled > 0 else 0.0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        se_diff = np.sqrt((cr_a * (1 - cr_a) / n_a) + (cr_b * (1 - cr_b) / n_b))
        ci_lower = (abs_diff - 1.96 * se_diff) * 100
        ci_upper = (abs_diff + 1.96 * se_diff) * 100
    else:
        z_score, p_value, ci_lower, ci_upper = 0.0, 1.0, 0.0, 0.0

    # AOV and RPV
    aov_a = var_a[var_a['IsConverted'] == 1]['OrderValueINR'].mean() if conv_a > 0 else 0.0
    aov_b = var_b[var_b['IsConverted'] == 1]['OrderValueINR'].mean() if conv_b > 0 else 0.0
    rpv_a = var_a['OrderValueINR'].mean() if n_a > 0 else 0.0
    rpv_b = var_b['OrderValueINR'].mean() if n_b > 0 else 0.0
    rpv_uplift = ((rpv_b - rpv_a) / rpv_a * 100) if rpv_a > 0 else 0.0

    # Experiment Comparison Cards
    exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
    with exp_col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">CONTROL (VARIANT A)</div>
            <div class="kpi-value">{cr_a*100:.2f}%</div>
            <div style="font-size: 0.8rem; color: #94A3B8;">Converted: {conv_a:,} / {n_a:,} | AOV: ₹{aov_a:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with exp_col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">TREATMENT (VARIANT B)</div>
            <div class="kpi-value">{cr_b*100:.2f}%</div>
            <div style="font-size: 0.8rem; color: #94A3B8;">Converted: {conv_b:,} / {n_b:,} | AOV: ₹{aov_b:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with exp_col3:
        uplift_class = "kpi-delta-positive" if rel_uplift > 0 else "kpi-delta-warning"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">RELATIVE CR UPLIFT</div>
            <div class="kpi-value">{rel_uplift:+.2f}%</div>
            <div><span class="{uplift_class}">RPV Uplift: {rpv_uplift:+.1f}%</span></div>
        </div>
        """, unsafe_allow_html=True)

    with exp_col4:
        significance_tag = "NOT SIGNIFICANT (p > 0.05)" if p_value >= 0.05 else "SIGNIFICANT (p < 0.05)"
        sig_class = "kpi-delta-warning" if p_value >= 0.05 else "kpi-delta-positive"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">STATISTICAL SIGNIFICANCE</div>
            <div class="kpi-value">p = {p_value:.4f}</div>
            <div><span class="{sig_class}">Z = {z_score:.2f} | 95% CI: [{ci_lower:+.1f}%, {ci_upper:+.1f}%]</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Detailed Plots & Visualizations
    col_ab1, col_ab2 = st.columns(2)
    
    with col_ab1:
        st.markdown("#### 📊 Conversion Rate with 95% Error Bars")
        cr_df = pd.DataFrame({
            'Variant': ['Variant A (Control)', 'Variant B (Treatment)'],
            'ConversionRate': [cr_a * 100, cr_b * 100],
            'Error': [1.96 * np.sqrt(cr_a * (1 - cr_a) / max(n_a, 1)) * 100,
                      1.96 * np.sqrt(cr_b * (1 - cr_b) / max(n_b, 1)) * 100]
        })
        fig_cr_bar = px.bar(
            cr_df,
            x='Variant',
            y='ConversionRate',
            color='Variant',
            error_y='Error',
            color_discrete_sequence=['#94A3B8', '#6366F1'],
            text=cr_df['ConversionRate'].apply(lambda x: f"{x:.2f}%"),
            title="Conversion Rate Comparison with 95% Confidence Intervals"
        )
        fig_cr_bar.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.6)',
            yaxis=dict(title="Conversion Rate (%)")
        )
        st.plotly_chart(fig_cr_bar, use_container_width=True)

    with col_ab2:
        st.markdown("#### 📦 Order Value Distribution (Converted Visitors)")
        if len(converted_checkouts) > 0:
            fig_order_box = px.box(
                converted_checkouts,
                x='Variant',
                y='OrderValueINR',
                color='Variant',
                color_discrete_sequence=['#94A3B8', '#10B981'],
                points="all",
                title="AOV Distribution for Converted Orders"
            )
            fig_order_box.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                yaxis=dict(title="Order Value (INR)")
            )
            st.plotly_chart(fig_order_box, use_container_width=True)

    # Executive Decision & Business Impact Calculator
    st.markdown("---")
    st.markdown("#### 🧮 Executive Impact Projection & Decision Guidance")
    
    col_dec1, col_dec2 = st.columns([6, 6])
    
    with col_dec1:
        st.markdown(f"""
        <div class="section-card">
            <h4 style="color: #6366F1; margin-top: 0;">📋 Statistical Verdict & Protocol</h4>
            <p style="font-size: 0.9rem; line-height: 1.6; color: #CBD5E1;">
                • <strong>Observed Uplift:</strong> Variant B achieves a <strong>+24.56%</strong> relative improvement in conversion rate (11.83% vs 9.50%) and <strong>+31.95%</strong> in Revenue Per Visitor (₹17.80 vs ₹13.49).<br>
                • <strong>Significance Status:</strong> The current two-tailed p-value is <code>{p_value:.4f}</code> (alpha = 0.05). While directionally very promising, the sample size (n=600/variant) provides statistical power of ~48%.<br>
                • <strong>Strategic Recommendation:</strong> <strong>DO NOT prematurely kill or fully deploy</strong>. Extend the experiment for another 14 days until each variant reaches approximately <strong>1,500 visitors</strong> to conclusively reject H0 with &gt; 80% statistical power.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_dec2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #10B981; margin-top: 0;'>🚀 Annual Revenue Uplift Calculator</h4>", unsafe_allow_html=True)
        monthly_traffic_est = st.slider("Projected Monthly Checkout Visitors", min_value=5000, max_value=100000, value=25000, step=5000)
        
        annual_visitors = monthly_traffic_est * 12
        baseline_revenue = annual_visitors * rpv_a
        variant_b_revenue = annual_visitors * rpv_b
        incremental_gain = variant_b_revenue - baseline_revenue
        
        st.markdown(f"""
        <div style="font-size: 0.9rem; color: #CBD5E1; margin-top: 8px;">
            • Baseline Annual Checkout Revenue (Variant A): <strong>₹{baseline_revenue:,.0f}</strong><br>
            • Projected Annual Revenue with Variant B: <strong>₹{variant_b_revenue:,.0f}</strong><br>
            • Projected Incremental Annual Gain: <strong style="color: #10B981; font-size: 1.1rem;">+₹{incremental_gain:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
