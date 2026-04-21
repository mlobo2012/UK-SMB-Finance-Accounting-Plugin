---
name: companies-house
description: Prepare Companies House filings, track deadlines, and classify company size under Companies Act 2006. Covers annual accounts, confirmation statements, audit exemption, current filing options, identity verification, and current fee schedules.
argument-hint: "<action> <period> — actions: annual-accounts, confirmation-statement, deadlines"
---

# Companies House Command — /companies-house

> This skill assists with Companies House filing preparation but does not constitute professional legal or accounting advice.

## Arguments

The user invoked this with: $ARGUMENTS

Parse:
- **Action:** One of `annual-accounts`, `confirmation-statement`, `deadlines`
- **Period:** e.g., `2025`, `2024-25`

## Deterministic Guardrail

Before stating a filing fee, identity-verification date, deadline, or form code:

```bash
python3 finance-uk/tools/lookup_rate.py --regime companies_house --parameter cs01_digital_fee --event-date 2026-04-21
python3 finance-uk/tools/lookup_rate.py --regime companies_house --parameter accounts_filing_reforms_state --event-date 2026-04-21
python3 finance-uk/tools/list_forms.py --regime companies_house --event-date 2026-04-21
python3 finance-uk/tools/find_deadline.py --regime companies_house_accounts_private --facts '{"period_end":"2025-12-31"}'
```

If the local tool has no verified record, say that there is no verified local entry and do not guess.
If the local tool **does** return a verified record, answer from that local record even if the user asks about a date beyond the model's own knowledge cutoff. Do not add a knowledge-cutoff disclaimer when the local record covers the requested date.

### Required Parameter Mapping

Use the local data parameter that matches the filing being discussed:

| User topic | Local parameter / tool |
|------------|------------------------|
| Confirmation statement (`CS01`) digital fee | `cs01_digital_fee` |
| Confirmation statement (`CS01`) paper fee | `cs01_paper_fee` |
| Voluntary strike-off (`DS01`) digital fee | `ds01_digital_fee` |
| Incorporation (`IN01`) digital fee | `incorporation_digital_fee` |
| Wider accounts-filing reform status | `accounts_filing_reforms_state` |
| Companies House form list | `list_forms.py --regime companies_house` |
| Accounts deadline | `find_deadline.py --regime companies_house_accounts_private` |

Hard rule: if the user asks about a **confirmation statement** or **CS01**, do **not** answer from the `DS01` strike-off fee. Those are different filings.

Hard rule: if the user asks whether the wider ECCTA accounts-filing reforms are live, delayed, or introduced on a particular date, answer from `accounts_filing_reforms_state` instead of model memory.

When the user asks a date-specific fee question:

1. Infer the event date from the prompt, or use today's date only if no date is supplied.
2. Run the matching local lookup.
3. Answer from the returned JSON value and status.
4. Mention if the value is `announced` rather than `enacted`.

## High-Risk Snapshot

Use the local tool outputs as the source of truth. The table below is only a quick orientation for the hardened areas most likely to drift.

| Item | Current local record |
|------|----------------------|
| CS01 digital fee | £50 from 1 February 2026 |
| CS01 paper fee | £110 |
| DS01 digital fee | £13 |
| Identity verification rollout starts | 18 November 2025 |
| Wider ECCTA accounts-filing reforms | Delayed, not live in April 2027 |

**Do not confuse `CS01` with `DS01`.** `CS01` is the confirmation statement. `DS01` is a voluntary strike-off form with a different fee.

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

**Current position:** Abridged and filleted options are still part of the live Companies House landscape today. The wider ECCTA accounts-filing reforms were **not** introduced in April 2027 and are currently delayed pending further notice.

If the user asks, "Were the wider ECCTA accounts-filing reforms introduced in April 2027?", answer: **No.** The current local record says those changes were **not** introduced in April 2027 and companies should receive at least 21 months' notice before any change.

### Micro-Entity Filing (FRS 105)

- Abridged balance sheet
- No P&L required to be filed
- No directors' report required
- Minimal notes only (guarantees and financial commitments)

### iXBRL Tagging

Company Tax Returns filed with HMRC require iXBRL-tagged accounts and computations. Companies House filing routes remain a mix of software and existing filing services depending on filing type. Do **not** tell users that software-only accounts filing is already mandatory.

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

### Identity Verification

- **From 18 November 2025**, new directors must verify identity before incorporation or appointment.
- Existing directors confirm identity verification with their next confirmation statement during the 12-month transition.
- Existing PSCs verify in line with their appointed timetable.
- GOV.UK One Login and ACSP routes are both current options.

## For `confirmation-statement`:

Annual confirmation that company information at Companies House is up to date.

- **Due:** Within 14 days of review date (anniversary of incorporation or previous confirmation)
- **Confirms:** Registered office, directors, secretary, share capital, PSC register, SIC codes
- **Fee:** £50 (digital) / £110 (paper) from 1 February 2026
- **Penalty:** Criminal offence for persistent default (up to £5,000 and/or striking off)

If the user asks for the confirmation statement fee on a specific date, look up `cs01_digital_fee` or `cs01_paper_fee` for that date first and answer from the tool result.

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
