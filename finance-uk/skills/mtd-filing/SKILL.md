---
name: mtd-filing
description: Prepare and file Making Tax Digital submissions for UK businesses — VAT (MTD) quarterly returns and ITSA quarterly updates. Covers HMRC API connection, fraud prevention headers, filing deadlines, and penalty regime.
user-invocable: true
argument-hint: "<type> <period> — types: vat, itsa"
allowed-tools: [Read, Glob, Grep]
---

# MTD Filing Command — /mtd-filing

> This skill assists with MTD filing preparation but does not constitute professional tax advice. Ensure your filing software is HMRC-recognised.

## Arguments

The user invoked this with: $ARGUMENTS

Parse:
- **Type:** `vat` or `itsa`
- **Period:** `YYYY-QX` for VAT quarterly, `YYYY-YY` for ITSA annual

## MTD for VAT (Fully Live)

**All VAT-registered businesses** must comply since 1 April 2022, regardless of turnover.

### Filing Workflow

#### Step 1: Pre-Filing Checks

- [ ] VAT reconciliation completed (complete the vat-reconciliation process first)
- [ ] All reconciling differences resolved
- [ ] Digital records maintained for all transactions (not just summaries)
- [ ] Digital links in place between software components (no copy-paste)
- [ ] Spreadsheets (if used) connected via API-enabled bridging software

#### Step 2: Prepare Return Data

Map reconciled figures to the 9-box return:

| Box | Description |
|-----|-------------|
| 1 | VAT due on sales and other outputs |
| 2 | VAT due on acquisitions from EC member states (post-Brexit: NI Protocol only; zero for GB-only businesses) |
| 3 | Total VAT due (Box 1 + Box 2) |
| 4 | VAT reclaimed on purchases and other inputs |
| 5 | Net VAT to pay or reclaim (Box 3 − Box 4) |
| 6 | Total value of sales excl. VAT |
| 7 | Total value of purchases excl. VAT |
| 8 | Supplies of goods to EC member states |
| 9 | Acquisitions of goods from EC member states |

#### Step 3: HMRC API Connection

Via ~~tax filing (HMRC MTD API):

- **Authentication:** OAuth 2.0 via Government Gateway credentials
- **Access tokens:** Valid 4 hours; refresh tokens 18 months
- **Core endpoints:**
  - `GET /organisations/vat/{vrn}/obligations` — retrieve filing periods
  - `POST /organisations/vat/{vrn}/returns` — submit 9-box return as JSON
- **Mandatory fraud prevention headers** on all requests

#### Step 4: Submit

- [ ] Final review of 9-box figures
- [ ] Declaration: "I confirm the information is true and complete"
- [ ] Submit via MTD-compatible software
- [ ] Save HMRC receipt / confirmation reference
- [ ] Record filing date in ~~accounting software

#### Step 5: Arrange Payment

Due by same deadline: **1 month + 7 days** after VAT period end.

Payment methods: Direct Debit (collected ~3 days after deadline), Faster Payments/CHAPS (same day), BACS (3 days).

### Penalty Regime (from January 2023)

**Late submission — points-based:**
- 1 point per late submission
- Threshold: 4 points (quarterly), 5 (monthly), 2 (annual)
- At threshold: £200 per late return
- Points expire after 12–24 months compliance

**Late payment:**
- 15 days late: no penalty
- 16–30 days: 2% of outstanding VAT
- 31+ days: 2% at day 15 + 2% at day 30 + daily rate at 4% pa

### Filing Deadlines (Quarterly)

| Quarter Ending | Deadline |
|---------------|----------|
| 31 March | 7 May |
| 30 June | 7 August |
| 30 September | 7 November |
| 31 December | 7 February |

## MTD for Income Tax Self Assessment (Launching April 2026)

| Phase | From | Threshold |
|-------|------|-----------|
| Phase 1 | **6 April 2026** | > £50,000 |
| Phase 2 | 6 April 2027 | > £30,000 |
| Phase 3 *(proposed)* | 6 April 2028 | > £20,000 |

"Qualifying income" = gross income from self-employment and/or UK property before expenses.

### ITSA Submissions

| Submission | Deadline |
|-----------|----------|
| Q1 (6 Apr – 5 Jul) | 7 August |
| Q2 (6 Jul – 5 Oct) | 7 November |
| Q3 (6 Oct – 5 Jan) | 7 February |
| Q4 (6 Jan – 5 Apr) | 7 May |
| **Final Declaration** | **31 January** following tax year |

Quarterly updates are **cumulative year-to-date figures**. Final Declaration replaces the annual Self Assessment return.

**Soft landing:** No penalty points for late quarterly updates in first year (2026/27).

### MTD for Corporation Tax

HMRC confirmed (July 2025) it **does not intend to introduce MTD for Corporation Tax**, instead developing a "modernised approach to corporation tax administration."
