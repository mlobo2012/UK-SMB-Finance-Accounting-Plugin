---
name: payroll-uk
description: Use this skill when the user discusses UK payroll, PAYE, National Insurance, employer NIC, auto-enrolment pensions, RTI, statutory payments (SSP, SMP, SPP), student loans, P11D, or payroll journal entries. Provides 2025/26 rates and thresholds for accounting purposes.
---

# UK Payroll Reference — 2025/26

> This skill provides payroll reference information for accounting purposes. It does not constitute payroll processing advice. Use HMRC-recognised payroll software for RTI submissions.

## PAYE Income Tax Bands (England & Northern Ireland)

| Band | Taxable Income | Rate |
|------|---------------|------|
| Personal Allowance | Up to £12,570 | 0% |
| Basic rate | £12,571 – £50,270 | 20% |
| Higher rate | £50,271 – £125,140 | 40% |
| Additional rate | Over £125,140 | 45% |

Personal Allowance reduces by £1 for every £2 earned over £100,000, reaching zero at £125,140.
## PAYE Income Tax Bands (Scotland)

| Band | Taxable Income | Rate |
|------|---------------|------|
| Personal Allowance | Up to £12,570 | 0% |
| Starter rate | £12,571 – £14,876 | 19% |
| Basic rate | £14,877 – £26,561 | 20% |
| Intermediate rate | £26,562 – £43,662 | 21% |
| Higher rate | £43,663 – £75,000 | 42% |
| Advanced rate | £75,001 – £125,140 | 45% |
| Top rate | Over £125,140 | 48% |

Scottish rates are set by the Scottish Parliament and apply to Scottish taxpayers (identified by tax code prefix 'S'). Wales currently matches England & Northern Ireland rates but has devolved power to vary them (identified by tax code prefix 'C').

## National Insurance Contributions

### Employee NIC (Class 1 Primary)

| Earnings Band | Rate |
|--------------|------|
| Below Primary Threshold (£242/week, £1,048/month, £12,570/year) | 0% |
| Primary Threshold to Upper Earnings Limit (£967/week, £4,189/month, £50,270/year) | 8% |
| Above Upper Earnings Limit | 2% |

### Employer NIC (Class 1 Secondary)

| Item | 2025/26 |
|------|---------|
| **Rate** | **15%** |
| **Secondary Threshold** | £96/week, £417/month, £5,000/year |
| Upper Secondary Threshold (under-21s, apprentices under 25, veterans) | £967/week, £4,189/month, £50,270/year |
| **Employment Allowance** | **£10,500/year** |

**Employment Allowance eligibility:** All qualifying employers regardless of NIC bill (previous £100,000 cap removed). Excluded: single-director companies with no other employees paid above the secondary threshold.

### Class 1A NIC

On benefits in kind (P11D items) at **15%** — payable annually by 22 July following tax year end.
## Self-Employed NIC (Class 2 & Class 4)

For sole traders and freelancers (assessed via Self Assessment):

### Class 2 NIC

| Item | 2025/26 |
|------|---------|
| **Rate** | **£3.45/week** |
| **Small Profits Threshold** | £6,725/year |
| **Status** | Voluntary from 2024/25 — no longer mandatory but counts towards State Pension qualification |

Paying Class 2 voluntarily is advisable for sole traders wanting to build State Pension entitlement at minimal cost.

### Class 4 NIC

| Profits Band | Rate |
|-------------|------|
| Below Lower Profits Limit (£12,570) | 0% |
| £12,570 – £50,270 | **6%** |
| Above £50,270 | **2%** |

Class 4 NIC is calculated on annual profits and collected via Self Assessment. No Employment Allowance applies to self-employed NIC.

## Workplace Pension Auto-Enrolment

| Parameter | Value |
|-----------|-------|
| Earnings trigger | £10,000/year (£833/month) |
| Qualifying earnings lower limit | £6,240/year (£520/month) |
| Qualifying earnings upper limit | £50,270/year (£4,189/month) |
| **Minimum employer contribution** | **3%** of qualifying earnings |
| **Minimum employee contribution** | **5%** (incl. tax relief) |
| **Minimum total** | **8%** |

Eligible jobholders: aged 22 to State Pension age, earning above trigger. Re-enrolment every 3 years.

## Apprenticeship Levy

| Item | Value |
|------|-------|
| Levy rate | **0.5%** of total annual pay bill |
| Annual allowance | **£15,000** |
| Effective threshold | Pay bill > **£3,000,000** |

## Student Loan Deductions

| Plan | Annual Threshold | Rate |
|------|-----------------|------|
| Plan 1 | £26,065 | 9% |
| Plan 2 | £28,470 | 9% |
| Plan 4 (Scotland) | £32,745 | 9% |
| Postgraduate | £21,000 | 6% |

## Statutory Payments

| Payment | Rate (2025/26) |
|---------|---------------|
| **SSP** | £118.75/week (3 qualifying days waiting period) |
| **SMP** first 6 weeks | 90% of AWE (no cap) |
| **SMP** weeks 7–39 | £187.18/week or 90% AWE, whichever is lower |
| **SPP** | £187.18/week or 90% AWE, whichever is lower |
| SAP/ShPP/SPBP/NCP (after initial period) | £187.18/week flat rate |

**Small Employers' Relief:** Recover **108.5%** of statutory payments. Larger employers: **92%**.

## National Minimum/Living Wage (from 1 April 2025)

| Band | Hourly Rate |
|------|------------|
| **NLW (21+)** | **£12.21** |
| 18–20 | £10.00 |
| Under 18 / Apprentice | £7.55 |
| Accommodation offset | £10.66/day |

## RTI (Real Time Information)

| Submission | Timing | Content |
|-----------|--------|---------|
| **FPS** | On or before each pay date | Employee details, pay, tax, NIC, student loans, pension |
| **EPS** | By 19th of following month | Statutory recoveries, Employment Allowance, Apprenticeship Levy |
| **Year-end FPS** | After last pay run | Year-end indicator, P60 data |

## P11D Benefits in Kind

Reportable: company cars, private medical insurance, interest-free loans (>£10,000), accommodation, childcare (above exempt limit). Deadline: 6 July. Class 1A NIC due: 22 July. Many benefits can now be payrolled to avoid P11D reporting.

## Journal Entry Summary — Monthly Payroll

```
Account                              Dr (£)        Cr (£)
Wages and salaries                   XX,XXX
Employer NIC                          X,XXX
Employer pension contributions        X,XXX
Apprenticeship Levy (if applicable)     XXX
  Net wages payable                                 XX,XXX
  PAYE creditor (HMRC)                               X,XXX
  Employee NIC creditor (HMRC)                        X,XXX
  Employer NIC creditor (HMRC)                        X,XXX
  Student loan creditor (HMRC)                          XXX
  Employee pension creditor                             XXX
  Employer pension creditor                           X,XXX
  Apprenticeship Levy creditor                          XXX
```


## IR35 / Off-Payroll Working Rules

### Overview

IR35 determines whether a contractor is genuinely self-employed or should be treated as an employee for tax purposes. The rules affect PAYE, NIC, and pension obligations.

### Responsibility for Determination

| Client Size | Who Determines Status? |
|------------|----------------------|
| **Small company** (meets 2 of 3: turnover ≤ £10.2M, balance sheet ≤ £5.1M, employees ≤ 50) | **Contractor** self-assesses |
| **Medium/Large company or public sector** | **Client** determines status via Status Determination Statement (SDS) |

### If Inside IR35

- Fee-payer (client or agency) must deduct PAYE, employee NIC, and employer NIC before paying the contractor's PSC
- Apprenticeship Levy applies if fee-payer's pay bill > £3M
- Contractor's PSC receives net payment after deemed employment deductions
- 5% flat-rate expense allowance for the contractor's PSC

### HMRC CEST Tool

HMRC's Check Employment Status for Tax (CEST) tool provides a non-binding indication. Key factors: control, substitution, mutuality of obligation.

### Accounting Impact

For engagements caught by IR35, the fee-payer must account for the deemed employment payment through payroll. The contractor's PSC should track the deemed payment calculations and retain records for potential HMRC enquiry.

> **Important:** IR35 status has significant tax consequences. Seek specialist advice for borderline cases. HMRC actively investigates non-compliance.
## Holiday Pay Accrual

UK law mandates 5.6 weeks (28 days for full-time) statutory leave including bank holidays (Working Time Regulations 1998). Holiday pay accrual is **always required** under FRS 102 Section 28.

Calculation: (Unused holiday days at period end / Working days in period) x Period staff costs
