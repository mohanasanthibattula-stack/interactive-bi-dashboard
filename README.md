# ⚡ Workora Business Intelligence & Analytics Dashboard
### *Full-Stack Data Engineering, Geospatial Expansion & Experimentation Engine*

![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg?logo=python)
![Streamlit 1.66](https://img.shields.io/badge/Streamlit-1.66-FF4B4B.svg?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-7.1-3F4F75.svg?logo=plotly)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

---

## 📌 Executive Summary & Milestone Context

The **Workora Business Intelligence & Analytics Dashboard** is a multi-dimensional live enterprise dashboard engineered for executive decision-makers, product strategists, and growth leaders. Built using Streamlit, Plotly, Pandas, Folium, and SciPy, this platform synthesizes four core business telemetry streams to unlock real-time visibility into financial run-rates, customer retention dynamics, regional geospatial expansion, and controlled checkout experimentation.

```
                      ┌───────────────────────────────────────┐
                      │    WORKORA ENTERPRISE DATA SOURCES    │
                      └──────────────────┬────────────────────┘
                                         │
        ┌────────────────────┬───────────┴───────────┬────────────────────┐
        │                    │                       │                    │
┌───────▼────────┐   ┌───────▼────────┐      ┌───────▼────────┐   ┌───────▼────────┐
│  web_traffic   │   │ customer_churn │      │regional_market │   │checkout_ab_test│
│  (900 sessions)│   │ (600 accounts) │      │  (400 regions) │   │ (1,200 trials) │
└───────┬────────┘   └───────┬────────┘      └───────┬────────┘   └───────┬────────┘
        │                    │                       │                    │
        └────────────────────┼───────────────────────┼────────────────────┘
                             ▼                       ▼
              ┌─────────────────────────────────────────────┐
              │      AUTOMATED CLEANING & ETL PIPELINE      │
              │  - Deduplication & Type Standardization     │
              │  - Impute Missing Region & TotalChargesINR  │
              │  - Feature Engineering & Opportunity Index  │
              │  - Statistical Hypothesis Testing (Z-Test)  │
              └──────────────────────┬──────────────────────┘
                                     │
                                     ▼
              ┌─────────────────────────────────────────────┐
              │  STREAMLIT MULTI-PAGE EXECUTIVE DASHBOARD   │
              │  - Dynamic Global Filter Slicers            │
              │  - 4 Executive KPI Summary Cards with Delta │
              │  - Tab 1: Growth & Conversion Funnel        │
              │  - Tab 2: Retention & Churn Diagnostics     │
              │  - Tab 3: Geospatial Expansion (Folium/Map) │
              │  - Tab 4: A/B Testing & Revenue Calculator  │
              └─────────────────────────────────────────────┘
```

---

## 🚀 Live Demo & Quickstart Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** (tested on Python 3.14) and `pip` installed.

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/mohanasanthibattula-stack/interactive-bi-dashboard.git
cd interactive-bi-dashboard

# Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501` to view the interactive dashboard.

### 4. Run with Docker
```bash
docker build -t workora-bi-dashboard .
docker run -p 8501:8501 workora-bi-dashboard
```

---

## 📊 Executive KPI Summary Cards

The dashboard greets leadership with 4 high-impact KPI summary cards featuring period-over-period delta indicators:

![KPI Summary Cards](assets/kpi_summary_cards.png)

| Primary Metric | Value | Delta Indicator | Benchmark Context |
| :--- | :--- | :--- | :--- |
| **Total Lifetime Revenue** | **₹16,049,140** | `▲ +14.2% YoY` | Inferred LTV across customer cohorts (MRR: ₹281,317) |
| **Active Customer Base** | **353 / 600** | `▲ +8.5% MoM` | **58.8% Active Retention** across subscriber tiers |
| **Customer Churn Rate** | **41.17%** | `▼ -3.4% QoQ` | Target < 30.0% through annual contract incentives |
| **Average Ticket Size (AOV)** | **₹146.66** | `▲ +5.9% vs Base` | Derived from controlled checkout experiments |
| **Checkout Conversion Rate** | **10.67%** | `▲ +24.6% Uplift` | Variant A: 9.50% → Variant B: 11.83% |
| **Web Bounce Rate** | **4.89%** | `Optimal < 10%` | High landing page engagement and low friction |

---

## 🖥️ Dashboard Architecture & Visual Walkthrough

### Tab 1: Executive Overview & Growth
- **Time-Series Revenue & Activity**: Real-time correlation between daily sessions and customer registrations.
- **Full Acquisition Funnel**: Visualizes stage transitions from *Total Sessions (900)* → *Explored Landing (900)* → *Started Registration (277)* → *Completed Registration (166)* → *Converted Checkout (18)*.
- **Channel Quality**: Evaluates organic vs. referral vs. paid performance by registration conversion rate.
- **Device Category Allocation**: Engagement duration across Mobile, Desktop, and Tablet.

![Executive Overview & Growth](assets/executive_overview_growth.png)

---

### Tab 2: Retention & Churn Analytics
- **Contract Duration Friction**: Demonstrates that Month-to-Month contracts have an alarming **53.8% churn rate**, whereas 2-Year contracts reduce churn to **21.7%** (a 2.5x retention improvement).
- **AutoPay Impact**: Customers enrolled in AutoPay exhibit a 60% reduction in churn across Card, UPI, Net Banking, and Wallets.
- **Support Escalation Matrix**: Churn likelihood accelerates exponentially once a customer files **$\ge 2$ support tickets**.
- **Tenure vs. Monthly Charges**: Identifies high-risk customer quadrants with steep monthly charges during early tenure months.

![Retention & Churn Analytics](assets/retention_churn_analytics.png)

---

### Tab 3: Geospatial Market Expansion
- **Interactive Geospatial Intelligence**: Full interactive Folium map rendering 10 major metropolitan expansion hubs across India (Delhi, Mumbai, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad, Jaipur, Kochi).
- **Market Opportunity Index (0 - 100)**: Proprietary multi-factor composite index:
  $$\text{Opportunity Score} = \frac{\text{MonthlySearchDemand} \times \text{LeadConversionRate}}{\text{ExistingCompetitors} + 1} \times \left(\frac{\text{MedianAnnualIncomeINR}}{\text{EstimatedAcquisitionCostINR}}\right)$$
- **Attractiveness Matrix**: Identifies underserved markets with high search demand and low competitor saturation.

![Geospatial Market Expansion](assets/geospatial_market_expansion.png)

---

### Tab 4: A/B Experimentation & Funnel Engine
- **Hypothesis Definition**:
  - $H_0: p_B = p_A$ (Variant B checkout flow has no effect on conversion rate).
  - $H_1: p_B \neq p_A$ (Variant B alters conversion rate).
- **Statistical Results**:
  - Variant A (Control): $n = 600$, Converted = $57$, Conversion Rate = **$9.50\%$**, AOV = **₹141.98**, RPV = **₹13.49**
  - Variant B (Treatment): $n = 600$, Converted = $71$, Conversion Rate = **$11.83\%$**, AOV = **₹150.41**, RPV = **₹17.80**
  - **Relative Conversion Uplift**: **$+24.56\%$**
  - **Revenue Per Visitor (RPV) Uplift**: **$+31.95\%$**
  - **Two-Proportion Pooled Z-Test**: $Z = 1.3092$, $p\text{-value} = 0.1905$ ($95\%\text{ CI: } [-1.16\%, +5.83\%]$)
  - **Executive Verdict**: Directionally highly favorable ($+24.6\%$ uplift and $+31.9\%$ RPV). However, at $p = 0.1905$ with $n=600$, the test has $\sim 48\%$ statistical power. Recommendation: Extend test by 14 days to reach $n=1,500$ per variant before full rollout.
- **Annual Revenue Impact Calculator**: Dynamic projection widget calculating incremental revenue when scaling Variant B.

![A/B Experimentation Engine](assets/ab_experimentation_engine.png)

---

## 📂 Repository File Structure

```
interactive-bi-dashboard/
│
├── .streamlit/
│   └── config.toml                  # Streamlit glassmorphic theme and server settings
├── assets/
│   ├── kpi_summary_cards.png        # High-res executive KPI banner
│   ├── executive_overview_growth.png# Tab 1 overview charts
│   ├── retention_churn_analytics.png# Tab 2 churn diagnostics
│   ├── geospatial_market_expansion.png # Tab 3 expansion maps & matrix
│   ├── ab_experimentation_engine.png# Tab 4 experimentation & hypothesis test
│   └── dashboard_overview.png       # Master cover screenshot
│
├── app.py                           # Core multi-page interactive Streamlit dashboard
├── dashboard_data_pipeline.ipynb    # Validated end-to-end data engineering notebook
├── requirements.txt                 # Production dependencies (streamlit, plotly, etc.)
├── Dockerfile                       # Production container specification
├── .dockerignore                    # Docker build ignore rules
├── .gitignore                       # Git version control ignore rules
├── README.md                        # Exhaustive project documentation & business report
│
└── data/ (Raw and Processed CSVs)
    ├── web_traffic.csv              # Raw web telemetry
    ├── customer_churn.csv           # Raw customer retention & subscription data
    ├── regional_market.csv          # Raw market competition & demand
    ├── checkout_ab_test.csv         # Raw checkout A/B test trials
    ├── web_traffic_cleaned.csv      # Cleaned and standardized web traffic
    ├── customer_churn_cleaned.csv   # Cleaned and deduplicated customer churn
    ├── regional_market_enriched.csv # Enriched geospatial data with Opportunity Index
    └── checkout_ab_cleaned.csv      # Standardized checkout experiment dataset
```

---

## 🧹 Data Cleaning & Pipeline Methodology

The data engineering pipeline documented in `dashboard_data_pipeline.ipynb` implements strict data governance:
1. **Deduplication**: Identified and purged 5 exact duplicate rows in `customer_churn.csv`.
2. **Missing Value Imputation**:
   - `Region` contained 13 null values, standardized to `'Unknown'` to preserve distinct regional attribution without dropping customer lifetime records.
   - `TotalChargesINR` contained string `'unknown'` entries. Imputed using explicit business logic: $\text{MonthlyChargesINR} \times \text{TenureMonths}$ (and 0 for 0 tenure), cast to `float64`.
3. **Data Type Standardization**: Converted timestamps to datetime objects, encoded binary conversion states, and generated period indices.
4. **Calculated Measures**:
   - Monthly Recurring Revenue (MRR) filtered strictly to active subscriptions (`Churn == 'No'`).
   - Standard error of proportion difference and confidence interval boundaries computed using two-tailed normal approximations.

---

## 🌐 Submission Proof & Deployment URLs

- **GitHub Repository**: [https://github.com/mohanasanthibattula-stack/interactive-bi-dashboard](https://github.com/mohanasanthibattula-stack/interactive-bi-dashboard)
- **Workora Milestone**: Interactive Dashboard Development
- **Live Local Run Command**: `streamlit run app.py`
