---
name: variance-analysis
description: Perform variance decomposition and narrative analysis for UK businesses — price/volume/mix analysis, waterfall charts, and materiality assessment. All amounts in GBP with UK formatting.
argument-hint: "<line-item> <period> vs <comparison>"
---

# Variance Analysis Command — /variance-analysis

> This skill assists with variance analysis but does not constitute professional accounting advice.

## Arguments

The user invoked this with: $ARGUMENTS

Parse the arguments to determine:
- **Line item:** e.g., `turnover`, `administrative-expenses`, `staff-costs`, `gross-profit`
- **Period:** e.g., `2025-Q3`, `2025-09`
- **Comparison:** e.g., `2025-Q2`, `budget`, `2024-Q3`

## Decomposition Framework

### Revenue / Turnover Variances

- **Price variance:** (Actual price − Budget price) × Actual volume
- **Volume variance:** (Actual volume − Budget volume) × Budget price
- **Mix variance:** Shift in product/service mix weighted by margin

### Cost Variances

- **Rate variance:** (Actual rate − Budget rate) × Actual quantity
- **Efficiency variance:** (Actual quantity − Budget quantity) × Budget rate
- **Spend variance:** Actual total − Budget total

## Materiality Thresholds

| Metric | Investigation Threshold | Explanation Required |
|--------|------------------------|---------------------|
| % of line item | > 5% | > 10% |
| Absolute amount | > £5,000 | > £25,000 |
| % of turnover | > 1% | > 2% |

For sole traders and micro-entities, adjust proportionately. A freelancer with £80,000 turnover should investigate variances above £500–£1,000.

Materiality aligns with ISA (UK) 320: typically 1–5% of a key benchmark (profit before tax, turnover, or total assets depending on entity circumstances).

## Waterfall Chart Format

```
Turnover Variance: [Period] vs [Comparison]

Budget Turnover           £125,000
  + Price increase           £8,200  ████████
  + Volume growth           £12,400  ████████████
  - Mix shift               (£3,100) ███
  - FX impact               (£1,500) █
                           --------
Actual Turnover           £141,000
                           ========
Variance: +£16,000 (+12.8%)
```

## Narrative Template

For each material variance, provide:

1. **What:** The variance amount and percentage
2. **Why:** Root cause analysis with specific business drivers
3. **Impact:** Effect on profitability, cash flow, or KPIs
4. **Action:** Recommended management response
5. **Trend:** Whether this is a one-off or recurring pattern

**Example narrative:**
> "Administrative expenses were £8,200 (15%) above budget in September 2025, primarily driven by £5,500 in unbudgeted legal fees for the office lease renegotiation and £2,700 in recruitment agency costs for the new management accountant role. The legal fees are non-recurring; recruitment costs may continue into October if the role remains unfilled. Recommend adjusting the Q4 forecast to reflect the lease renegotiation settlement."

## UK-Specific Variance Considerations

- **Employer NIC changes:** The increase from 13.8% to 15% (April 2025) creates a year-on-year variance in staff costs that is regulatory, not operational. Flag separately from efficiency/headcount variances.
- **VAT rate changes:** Any VAT rate changes affect gross revenue comparisons. Always analyse turnover variances on a VAT-exclusive basis.
- **Seasonal patterns:** UK businesses often see Q4 (Jan–Mar) seasonal dips; retail sees Q3 (Oct–Dec) peaks. Compare to prior-year same-period rather than sequential quarter where seasonal patterns are significant.
- **Foreign currency:** For businesses with international income (common for freelancers), separately identify FX translation variances from operational variances.

Always use **GBP (£)** and **DD/MM/YYYY** dates throughout.
