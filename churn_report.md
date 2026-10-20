# Customer Cohort & Churn Analytics Report

## 1. Baseline
- Total customers: **7,043**
- Churned: **1,869**
- Baseline churn rate: **26.5%**

## 2. Churn by tenure cohort
| TenureCohort   |   customers |   churned |   churn_rate |
|:---------------|------------:|----------:|-------------:|
| 0-12           |        2186 |      1037 |         47.4 |
| 13-24          |        1024 |       294 |         28.7 |
| 25-36          |         832 |       180 |         21.6 |
| 37-48          |         762 |       145 |         19   |
| 49-60          |         832 |       120 |         14.4 |
| 61-72          |        1407 |        93 |          6.6 |

## 3. Churn by contract type
| Contract       |   customers |   churned |   churn_rate |
|:---------------|------------:|----------:|-------------:|
| Month-to-month |        3875 |      1655 |         42.7 |
| One year       |        1473 |       166 |         11.3 |
| Two year       |        1695 |        48 |          2.8 |

## 4. Churn by payment method
| PaymentMethod             |   customers |   churned |   churn_rate |
|:--------------------------|------------:|----------:|-------------:|
| Bank transfer (automatic) |        1544 |       258 |         16.7 |
| Credit card (automatic)   |        1522 |       232 |         15.2 |
| Electronic check          |        2365 |      1071 |         45.3 |
| Mailed check              |        1612 |       308 |         19.1 |

## 5. Churn by monthly charge band
| ChargeBand   |   customers |   churned |   churn_rate |
|:-------------|------------:|----------:|-------------:|
| Low          |        1762 |       198 |         11.2 |
| Mid-Low      |        1766 |       434 |         24.6 |
| Mid-High     |        1757 |       659 |         37.5 |
| High         |        1758 |       578 |         32.9 |

## 6. Churn by internet service
| InternetService   |   customers |   churned |   churn_rate |
|:------------------|------------:|----------:|-------------:|
| DSL               |        2421 |       459 |         19   |
| Fiber optic       |        3096 |      1297 |         41.9 |
| No                |        1526 |       113 |          7.4 |

## 7. Cohort retention matrix (retention %)
| TenureCohort   |   Month-to-month |   One year |   Two year |
|:---------------|-----------------:|-----------:|-----------:|
| 0-12           |             48.6 |       89.5 |      100   |
| 13-24          |             62.3 |       91.9 |      100   |
| 25-36          |             67.5 |       92   |       97.9 |
| 37-48          |             66.5 |       86.9 |       97.8 |
| 49-60          |             72.2 |       86.3 |       96   |
| 61-72          |             77.8 |       87.9 |       96.9 |

## 8. High-risk segments
| segment                              |   customers |   churn_rate |
|:-------------------------------------|------------:|-------------:|
| Electronic check + month-to-month    |        1850 |         53.7 |
| High monthly charge + month-to-month |         870 |         52.2 |
| Month-to-month, first year           |        1994 |         51.4 |
| Fiber optic, no tech support         |        2230 |         49.4 |
| Internet, no online security         |        3498 |         41.8 |

Highest-risk segment: **Electronic check + month-to-month** (53.7% churn,
1,850 customers).

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
