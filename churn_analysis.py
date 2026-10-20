"""
Task 3: Customer Cohort & Churn Analytics (IBM Telco Churn dataset)

Run:
    pip install pandas plotly
    python churn_analysis.py

Put the dataset CSV in the same folder (default name below).
Outputs go to the ./outputs folder: interactive HTML charts + churn_report.md
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_FILE = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------
# 1. Load + clean
# ---------------------------------------------------------------
df = pd.read_csv(DATA_FILE)

# TotalCharges has blank strings for brand-new customers (tenure = 0)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

# Tenure cohorts (12-month buckets)
df["TenureCohort"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 36, 48, 60, 72],
    labels=["0-12", "13-24", "25-36", "37-48", "49-60", "61-72"],
)

# Monthly charge bands (quartiles)
df["ChargeBand"] = pd.qcut(
    df["MonthlyCharges"], 4, labels=["Low", "Mid-Low", "Mid-High", "High"]
)

# ---------------------------------------------------------------
# 2. Baseline churn rate = Churned / Total * 100
# ---------------------------------------------------------------
total = len(df)
churned = int(df["ChurnFlag"].sum())
baseline = churned / total * 100


def churn_by(col):
    t = (
        df.groupby(col, observed=True)["ChurnFlag"]
        .agg(customers="count", churned="sum", churn_rate="mean")
        .reset_index()
    )
    t["churn_rate"] = (t["churn_rate"] * 100).round(1)
    return t


by_cohort = churn_by("TenureCohort")
by_contract = churn_by("Contract")
by_payment = churn_by("PaymentMethod")
by_charge = churn_by("ChargeBand")
by_service = churn_by("InternetService")

# ---------------------------------------------------------------
# 3. Cohort retention matrix (tenure cohort x contract type)
# ---------------------------------------------------------------
churn_matrix = df.pivot_table(
    index="TenureCohort",
    columns="Contract",
    values="ChurnFlag",
    aggfunc="mean",
    observed=True,
) * 100
retention_matrix = (100 - churn_matrix).round(1)

fig = px.imshow(
    retention_matrix,
    text_auto=".1f",
    color_continuous_scale="RdYlGn",
    aspect="auto",
    labels=dict(x="Contract Type", y="Tenure Cohort (months)", color="Retention %"),
    title="Cohort Retention Matrix (% customers retained)",
)
fig.write_html(OUT / "1_cohort_retention_matrix.html")

# ---------------------------------------------------------------
# 4. Retention curves (Kaplan-Meier style survival by contract)
# ---------------------------------------------------------------
def survival_curve(sub):
    events = sub.groupby("tenure")["ChurnFlag"].sum()
    at_risk = sub["tenure"].value_counts().sort_index(ascending=False).cumsum()
    at_risk = at_risk.sort_index()
    s = (1 - events.reindex(at_risk.index, fill_value=0) / at_risk).cumprod()
    return s * 100


fig = go.Figure()
for contract, sub in df.groupby("Contract"):
    s = survival_curve(sub)
    fig.add_trace(go.Scatter(x=s.index, y=s.values, mode="lines", name=contract))
fig.update_layout(
    title="Customer Retention Curve by Contract Type",
    xaxis_title="Tenure (months)",
    yaxis_title="Customers retained (%)",
)
fig.write_html(OUT / "2_retention_curves.html")

# ---------------------------------------------------------------
# 5. Churn drivers: payment method, charge band, service tier
# ---------------------------------------------------------------
for name, table, col in [
    ("3_churn_by_payment_method", by_payment, "PaymentMethod"),
    ("4_churn_by_monthly_charge_band", by_charge, "ChargeBand"),
    ("5_churn_by_contract", by_contract, "Contract"),
]:
    f = px.bar(
        table, x=col, y="churn_rate", text="churn_rate",
        title=name.split("_", 1)[1].replace("_", " ").title() + " (churn %)",
    )
    f.add_hline(y=baseline, line_dash="dash",
                annotation_text=f"Baseline {baseline:.1f}%")
    f.write_html(OUT / f"{name}.html")

# Service-tier heatmap: Internet service x Tech support
tier = df.pivot_table(
    index="InternetService", columns="TechSupport",
    values="ChurnFlag", aggfunc="mean",
) * 100
fig = px.imshow(
    tier.round(1), text_auto=".1f", color_continuous_scale="Reds", aspect="auto",
    labels=dict(x="Tech Support", y="Internet Service", color="Churn %"),
    title="Churn Heatmap by Service Tier",
)
fig.write_html(OUT / "6_churn_heatmap_service_tier.html")

# ---------------------------------------------------------------
# 6. High-risk segments
# ---------------------------------------------------------------
def segment(mask, label):
    sub = df[mask]
    return {
        "segment": label,
        "customers": len(sub),
        "churn_rate": round(sub["ChurnFlag"].mean() * 100, 1),
    }


segments = pd.DataFrame([
    segment((df["InternetService"] == "Fiber optic") & (df["TechSupport"] == "No"),
            "Fiber optic, no tech support"),
    segment((df["Contract"] == "Month-to-month") & (df["tenure"] <= 12),
            "Month-to-month, first year"),
    segment((df["PaymentMethod"] == "Electronic check")
            & (df["Contract"] == "Month-to-month"),
            "Electronic check + month-to-month"),
    segment((df["ChargeBand"] == "High") & (df["Contract"] == "Month-to-month"),
            "High monthly charge + month-to-month"),
    segment((df["OnlineSecurity"] == "No") & (df["InternetService"] != "No"),
            "Internet, no online security"),
]).sort_values("churn_rate", ascending=False)

# ---------------------------------------------------------------
# 7. Auto-generated report
# ---------------------------------------------------------------
def md(table):
    return table.to_markdown(index=False)


try:
    import tabulate  # noqa: F401
except ImportError:
    def md(table):  # fallback if tabulate is not installed
        return "```\n" + table.to_string(index=False) + "\n```"

worst = segments.iloc[0]
report = f"""# Customer Cohort & Churn Analytics Report

## 1. Baseline
- Total customers: **{total:,}**
- Churned: **{churned:,}**
- Baseline churn rate: **{baseline:.1f}%**

## 2. Churn by tenure cohort
{md(by_cohort)}

## 3. Churn by contract type
{md(by_contract)}

## 4. Churn by payment method
{md(by_payment)}

## 5. Churn by monthly charge band
{md(by_charge)}

## 6. Churn by internet service
{md(by_service)}

## 7. Cohort retention matrix (retention %)
{md(retention_matrix.reset_index())}

## 8. High-risk segments
{md(segments)}

Highest-risk segment: **{worst['segment']}** ({worst['churn_rate']}% churn,
{worst['customers']:,} customers).

## 9. Strategic retention recommendations
1. **Push contract upgrades early.** Month-to-month customers churn far more
   than 1-year / 2-year customers. Offer discounts or perks to move them to
   longer contracts within the first 12 months.
2. **Fix the first year.** The 0-12 month cohort has the highest churn.
   Add onboarding calls, welcome offers and a 90-day check-in.
3. **Bundle tech support with Fiber plans.** Fiber users without tech support
   are a high-risk segment. Free or discounted support bundles can help.
4. **Move customers off electronic check.** Incentivise auto-pay (card / bank
   transfer) since electronic-check users churn more.
5. **Review pricing for high-charge customers.** Offer loyalty pricing or
   value-added services (security, backup) to customers in the High charge band.
6. **Build an early-warning list.** Flag customers who match 2+ high-risk
   segments and trigger proactive retention outreach.
"""
(OUT / "churn_report.md").write_text(report, encoding="utf-8")

print(f"Baseline churn: {baseline:.1f}%")
print("\nRetention matrix:\n", retention_matrix)
print("\nHigh-risk segments:\n", segments.to_string(index=False))
print(f"\nDone. Check the '{OUT}' folder.")
