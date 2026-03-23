---
name: companies-house
description: Prepare Companies House filings, track deadlines, and classify company size under Companies Act 2006. Covers annual accounts, confirmation statements, audit exemption, abridged/filleted accounts, and iXBRL tagging. Also covers sole trader and partnership filing obligations.
user-invocable: true
argument-hint: "<action> <period> — actions: annual-accounts, confirmation-statement, deadlines"
allowed-tools: [Read, Glob, Grep]
---

# Companies House Command — /companies-house

> This skill assists with Companies House filing preparation but does not constitute professional legal or accounting advice.

## Arguments

The user invoked this with: $ARGUMENTS

Parse:
- **Action:** One of `annual-accounts`, `confirmation-statement`, `deadlines`
- **Period:** e.g., `2025`, `2024-25`

## Company Size Classification

Per Companies Act 2006, SI 2024/1303 (FY beginning on or after 6 April 2025):

| Category | Turnover | Balance Sheet | Employees | Meet |
|----------|----------|---------------|-----------|------|
| **Micro-entity** | ≤ £1,000,000 | ≤ £500,000 | ≤ 10 | 2 of 3 |
| **Small** | ≤ £15,000,000 | ≤ £7,500,000 | ≤ 50 | 2 of 3 |
| **Medium** | ≤ £54,000,000 | ≤ £27,000,000 | ≤ 250 | 2 of 3 |

Two-consecutive-year rule applies for changes (transitional provisions allow immediate benefit from new thresholds).

## For `annual-accounts`:

### Filing Deadlines

| Company Type | Deadline |
|-------------|----------|
| **Private / LLP** | **9 months** from accounting reference date |
| **Public** | **6 months** from accounting reference date |
| **First accounts (private, >12m)** | 21 months from incorporation or 3 months from ARD, whichever longer |

### Late Filing Penalties

| Lateness | Private / LLP | Public |
|----------|--------------|--------|
| ≤ 1 month | £150 | £750 |
| 1–3 months | £375 | £1,500 |
| 3–6 months | £750 | £3,000 |
| > 6 months | £1,500 | £7,500 |

Penalties **double** if late in two successive financial years.

### Audit Exemption

Small company exemption (s.477): meet 2 of 3 — turnover ≤ £15M, balance sheet ≤ £7.5M, employees ≤ 50.

**Excluded regardless of size:** Public companies (unless dormant), banking companies, authorised insurance companies, e-money issuers, MiFID investment firms, UCITS management companies, regulated market companies.

**Members' right:** ≥ 10% of share capital can require an audit by written notice before year-end.

### Filing Options (Small Companies)

1. **Full accounts** — complete balance sheet, P&L, notes, directors' report
2. **Abridged accounts** — Arabic-numbered items combined (unanimous member consent required)
3. **Filleted accounts** — omit P&L and/or directors' report

**Abridged P&L (Format 1):** Items 1–3 and 6 merge into "Gross profit or loss", concealing turnover and cost of sales.

**Note:** Economic Crime and Corporate Transparency Act 2023 will eventually remove abridged option (pending secondary legislation).

### Micro-Entity Filing (FRS 105)

- Abridged balance sheet
- No P&L required to be filed
- No directors' report required
- Minimal notes only (guarantees and financial commitments)

### iXBRL Tagging

All accounts filed online must be tagged in iXBRL using the Companies House taxonomy. Most accounting software handles this automatically.

### Filing Preparation Checklist

- [ ] Confirm company size classification
- [ ] Select accounts format (full/abridged/filleted/micro)
- [ ] Prepare accounts per Companies Act statutory format (refer to the financial-statements skill for annual format guidance)
- [ ] Directors approve accounts; balance sheet signed
- [ ] Include all required notes
- [ ] Directors' report (required for medium and large; optional for small)
- [ ] Strategic report (required for medium and large)
- [ ] Auditor's report (if required)
- [ ] Tag in iXBRL
- [ ] File via Companies House WebFiling or software filing
- [ ] Record filing date and confirmation

## For `confirmation-statement`:

Annual confirmation that company information at Companies House is up to date.

- **Due:** Within 14 days of review date (anniversary of incorporation or previous confirmation)
- **Confirms:** Registered office, directors, secretary, share capital, PSC register, SIC codes
- **Fee:** £13 (online) / £40 (paper)
- **Penalty:** Criminal offence for persistent default (up to £5,000 and/or striking off)

## For `deadlines`:

Present all upcoming filing deadlines for the entity:

| Filing | Deadline | Status |
|--------|----------|--------|
| Companies House annual accounts | [date] | [pending/filed] |
| Corporation Tax return (CT600) | [date] | [pending/filed] |
| Corporation Tax payment | [date] | [pending/paid] |
| Confirmation statement | [date] | [pending/filed] |
| VAT return (current quarter) | [date] | [pending/filed] |
| PAYE/NIC (current month) | [date] | [pending/paid] |

## Sole Traders and Partnerships

Sole traders and ordinary partnerships are **not registered at Companies House** and have **no Companies House filing obligations**.

Their obligations are to HMRC:
- Self Assessment (SA100) by 31 January
- MTD ITSA quarterly updates (from April 2026 if qualifying income > £50,000)
- Partnership return (SA800) if applicable

**LLPs** are registered at Companies House with obligations similar to limited companies.
