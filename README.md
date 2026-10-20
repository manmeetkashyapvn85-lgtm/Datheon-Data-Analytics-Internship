# Datheon Data Analytics Internship – Task 3: Customer Cohort & Churn Analytics

## Objective
Analyse customer retention behaviour on the IBM Telco Churn dataset. Segment customers by tenure cohort, contract type, payment method and monthly charges to compute retention curves and churn probability.

## Dataset
IBM Telco Customer Churn (7,043 customers, 21 columns).

## Approach
1. Loaded and cleaned the data (`TotalCharges` blanks → 0, churn flag encoded).
2. Calculated baseline churn rate = Churned Customers / Total Customers × 100.
3. Grouped customers into tenure cohorts (0-12, 13-24, ... months) and contract types.
4. Built a cohort retention matrix and retention curves by contract.
5. Compared churn across payment methods, monthly charge bands and service tiers.
6. Identified high-risk segments (e.g. Fiber optic users without tech support).
7. Wrote strategic retention recommendations (see `outputs/churn_report.md`).

## Tools
Python (Pandas, Plotly)

## How to Run
```bash
pip install pandas plotly tabulate
python churn_analysis.py
```
Place `WA_Fn-UseC_-Telco-Customer-Churn.csv` in the same folder first.

## Outputs (`/outputs`)
- `1_cohort_retention_matrix.html`
- `2_retention_curves.html`
- `3_churn_by_payment_method.html`
- `4_churn_by_monthly_charge_band.html`
- `5_churn_by_contract.html`
- `6_churn_heatmap_service_tier.html`
- `churn_report.md` – full churn analysis report + recommendations

## Key Findings
_Run the script and paste the top 3-4 numbers from `churn_report.md` here (baseline churn %, highest-risk segment, month-to-month vs long-contract churn)._
