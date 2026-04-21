---
name: payroll-uk
description: Use this skill when the user discusses UK payroll, PAYE, National Insurance, employer NIC, auto-enrolment pensions, RTI, statutory payments, student loans, P11D, payrolling of benefits, or payroll journal entries. Use the local deterministic lookup tools before stating date-sensitive figures.
---

# UK Payroll Reference

> This skill provides payroll reference information for accounting purposes. It does not constitute payroll processing advice. Use HMRC-recognised payroll software for RTI submissions.

## Deterministic Guardrail

Before stating any payroll rate, threshold, filing date, or benefits-in-kind effective date:

1. Run the local lookup tool from the plugin root.
2. Use the returned value and source in the answer.
3. If the tool returns `ok: false`, say there is no verified local record and do not guess.

Examples:

```bash
python3 finance-uk/tools/lookup_rate.py --regime payroll --parameter employer_nic_rate --event-date 2026-04-06
python3 finance-uk/tools/lookup_rate.py --regime payroll --parameter mandatory_payrolling_bik_from --event-date 2026-07-01
python3 finance-uk/tools/find_deadline.py --regime p11d --facts '{"tax_year_end":"2026-04-05"}'
```

## High-Risk Snapshot

Use the tool outputs as the source of truth. The table below is only a quick orientation for the current hardening scope.

| Item | 2025/26 | 2026/27 |
|------|---------|---------|
| Employer NIC rate | 15% | 15% |
| Employer secondary threshold | £5,000/year | £5,000/year |
| Lower Earnings Limit | £6,500/year | £6,708/year |
| Employment Allowance | £10,500/year | £10,500/year |
| SSP | £118.75/week | £123.25/week |
| Mandatory payrolling of most BiKs | Not live | Not live |

**Important:** Mandatory payrolling of most benefits in kind starts on **6 April 2027**, not 6 April 2026. For 2026/27, voluntary payrolling remains the position and the legacy registration deadline was **5 April 2026**.

## PAYE and NIC Workflow

When the user asks a payroll question:

1. Identify the tax date or pay period first.
2. Look up the relevant rate or threshold locally.
3. Distinguish between:
   - employee deductions;
   - employer costs;
   - annual reporting items such as P11D and Class 1A NIC.
4. If the question is about a live payroll run, recommend payroll software as the execution system and use this skill as an explanation and review layer.

## RTI (Real Time Information)

| Submission | Timing | Notes |
|-----------|--------|-------|
| **FPS** | On or before each pay date | Includes pay, tax, NIC, student loans, starter/leaver data |
| **EPS** | By the 19th of the following month | Used for statutory recoveries, Employment Allowance, Apprenticeship Levy, nil periods |
| **P60** | By 31 May after tax year end | Use deadline tool for the exact filing year context |
| **P11D / P11D(b)** | By 6 July after tax year end | Benefits reporting still required where benefits are not being payrolled |
| **Class 1A NIC payment** | By 22 July electronically | Due after the tax year on P11D benefits |

## Benefits in Kind

- 2026/27 remains a **voluntary payrolling** year for most benefits.
- Mandatory reporting and payment of Income Tax and Class 1A NIC through payroll starts **6 April 2027** for most BiKs.
- Employment-related loans and living accommodation remain special cases and should not be assumed to follow the general rule without checking current guidance.
- If the user asks whether a business must payroll benefits now, answer from the tool-backed date first, then explain the transitional position.

## Auto-Enrolment

Auto-enrolment remains a minimum-contribution regime:

- minimum employer contribution: 3% of qualifying earnings
- minimum employee contribution: 5% including tax relief
- minimum total: 8%

Treat these as minimum compliance numbers, not scheme design advice.

## Student Loans and Statutory Payments

Student loan thresholds and statutory payment rates change over time. Do not quote them from memory. Use the local data layer when the answer depends on the tax year.

## IR35 / Off-Payroll Working

Handle IR35 conservatively:

- **Chapter 8** applies where the client is small or the worker is dealing with the old intermediary rules.
- **Chapter 10** applies where the end client is medium or large, or in the public sector.
- From **6 April 2025**, the small-company thresholds moved to **£15m turnover / £7.5m balance sheet / 50 employees**. HMRC guidance says this usually does **not** affect off-payroll status in practice until **6 April 2027 at the earliest**, because the size test looks back.
- HMRC says it will stand by a CEST result where the information is accurate and the arrangements are not contrived.
- Do **not** make a definitive IR35 determination inside this skill. Explain the framework, status determination statement process, and where specialist review is needed.
- Do **not** present the 5% admin allowance as a universal rule. It is relevant to the Chapter 8 deemed payment calculation, not the Chapter 10 fee-payer regime generally.

## Journal Entry Reminder

For payroll journals, include:

- gross wages
- PAYE and employee NIC deductions
- employer NIC
- employer pension contributions
- Apprenticeship Levy where applicable
- holiday pay accrual adjustments
- statutory payment recoveries where relevant

If the entry depends on a tax-year threshold or rate, look it up first and cite the result.

## Holiday Pay Accrual

UK statutory leave remains 5.6 weeks for a full-time worker under the Working Time Regulations 1998. Holiday pay accrual is an accounting estimate question, not a lookup-rate question, so explain the basis and assumptions clearly.
