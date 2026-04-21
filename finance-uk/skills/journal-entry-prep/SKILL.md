---
name: journal-entry-prep
description: Use this skill when the user is preparing, reviewing, or discussing UK journal entries, accruals, prepayments, depreciation, payroll journals, or asks about UK accounting entry best practices. Provides FRS 102/IFRS guidance, UK tax treatments, approval matrices, and documentation standards for GBP-denominated entries.
---

# Journal Entry Preparation — UK Best Practices

> This skill assists with journal entry preparation but does not constitute professional accounting advice. Consult a qualified accountant for decisions affecting your business.

## Deterministic Guardrail

If a journal entry explanation depends on a tax-year-sensitive rate, threshold, filing fee, or corporation-tax parameter, look it up first:

```bash
python3 finance-uk/tools/lookup_rate.py --regime payroll --parameter employer_nic_rate --event-date 2026-04-06
python3 finance-uk/tools/lookup_rate.py --regime corporation_tax --parameter main_pool_wda_rate --event-date 2026-04-01
```

If no verified local record exists, say so and avoid inventing the figure.

## Standard Accrual Types

### 1. Accounts Payable Accruals

Record goods/services received but not yet invoiced at period end.

**Recognition criteria (FRS 102 Section 2.42):**
- Obligation exists at the reporting date
- Amount can be measured reliably
- Probable outflow of economic benefits

**Standard entry:**
```
Dr  Cost of sales / Operating expenses     £X,XXX
  Cr  Accruals (creditors due within one year)  £X,XXX
```

**Documentation required:**
- Supplier name and purchase order reference
- Goods received note (GRN) or delivery confirmation
- Estimated amount and basis of estimation
- Reversal date (first day of following period)

### 2. Revenue Accruals

**[FRS 102 VERSION TOGGLE — ask the user which version applies]**

**Pre-January 2026 (current FRS 102 Section 23 — risks-and-rewards model):**
Recognise revenue from goods when risks and rewards of ownership transfer, the entity retains no managerial involvement, revenue is reliably measurable, and economic benefits are probable. Services use percentage-of-completion.

**Post-January 2026 (revised FRS 102 Section 23 — IFRS 15 five-step model):**
1. Identify the contract with a customer
2. Identify the performance obligations
3. Determine the transaction price
4. Allocate the transaction price to performance obligations
5. Recognise revenue as/when performance obligations are satisfied

Variable consideration is constrained to amounts "highly probable" of not reversing.

**Standard entry:**
```
Dr  Trade debtors                          £X,XXX
  Cr  Turnover                               £X,XXX
```

### 3. Payroll Accruals

UK payroll accruals must include all employer-side costs:

| Component | Rate/Amount (verify for posting date) | Account |
|-----------|----------------------|---------|
| **Employer NIC (Class 1 secondary)** | **15%** above £5,000/year (£417/month) threshold | Employer NIC expense |
| **Employer pension (auto-enrolment)** | **Minimum 3%** of qualifying earnings (£6,240–£50,270) | Pension contributions expense |
| **Apprenticeship Levy** | **0.5%** of pay bill (only if pay bill > £3,000,000) | Apprenticeship Levy expense |
| **Holiday pay accrual** | **Mandatory** — 5.6 weeks statutory minimum | Holiday pay accrual (creditors) |
| **Employer NIC on benefits** | **15%** (Class 1A) on P11D benefit values | Employer NIC expense |

**Employment Allowance:** £10,500/year — deducted from employer NIC liability. The previous £100,000 eligibility cap has been removed. Single-director companies with no other employees paid above the secondary threshold remain excluded.

**Standard payroll accrual entry:**
```
Dr  Wages and salaries                     £X,XXX
Dr  Employer NIC                           £X,XXX
Dr  Employer pension contributions         £X,XXX
  Cr  Net wages payable                      £X,XXX
  Cr  PAYE/NIC creditor (HMRC)               £X,XXX
  Cr  Pension contributions creditor          £X,XXX
  Cr  Holiday pay accrual                    £X,XXX
```

### 4. Prepaid Expenses

**Standard entry (initial payment):**
```
Dr  Prepayments (debtors)                  £X,XXX
  Cr  Bank                                   £X,XXX
```

**Standard entry (monthly amortisation):**
```
Dr  Insurance / Rent / Subscription expense £X,XXX
  Cr  Prepayments (debtors)                  £X,XXX
```

### 5. Fixed Asset Depreciation / Capital Allowances

UK businesses must track both **accounting depreciation** (per FRS 102 Section 17) and **capital allowances** (for Corporation Tax purposes). These are separate calculations.

**Capital allowances (verify for the accounting period / chargeable period):**

| Allowance | Rate | Eligibility |
|-----------|------|-------------|
| Annual Investment Allowance (AIA) | **100%** up to **£1,000,000**/year | Qualifying plant and machinery (excl. cars) |
| Full expensing | **100%** (main rate) / **50%** (special rate) | Companies only, new and unused P&M, excl. cars/leasing |
| Writing-down allowance — main pool | **18%** reducing balance | Plant and machinery |
| Writing-down allowance — special rate | **6%** reducing balance | Long-life assets, integral features, thermal insulation |
| Small pool write-off | **100%** | Pools ≤ £1,000 |

Note: Main pool WDA rate drops to **14%** from 1 April 2026 (Autumn Budget 2025).

**Standard depreciation entry:**
```
Dr  Depreciation expense                   £X,XXX
  Cr  Accumulated depreciation               £X,XXX
```

### 6. VAT Accruals

At each period end, ensure the VAT control account reflects:
- Output VAT collected on sales
- Input VAT recoverable on purchases
- Net VAT liability (or receivable) due to HMRC

## Approval Matrix

| Entry Value | Required Approver | Supporting Documentation |
|-------------|-------------------|------------------------|
| < £5,000 | Bookkeeper / Accounts Assistant | Invoice or calculation workpaper |
| £5,000 – £40,000 | Management Accountant / Financial Controller | Invoice, workpaper, and narrative |
| £40,000 – £200,000 | Finance Director (FD) / CFO | Full workpaper pack with supporting schedules |
| > £200,000 | FD/CFO + Board approval | Full workpaper pack, board minute reference |

For sole traders and micro-entities, the approval matrix may be simplified to owner review for all entries above a self-determined threshold.

## Documentation Standards

Every journal entry must include:
1. **Preparer name and date**
2. **Period and entity** (if multi-entity)
3. **Description** — clear narrative explaining the business rationale
4. **Supporting calculation** — workpaper or schedule reference
5. **Reversing indicator** — whether the entry auto-reverses in the next period
6. **Account codes** — per the entity's chart of accounts
7. **VAT treatment** — standard rated, zero rated, exempt, or outside scope

## Entry Format Template

```
Date:        DD/MM/YYYY
Entity:      [Company name]
Period:      [Month YYYY or Quarter Q1-Q4]
Reference:   JE-YYYY-MM-NNN

Account Code | Account Name              | Dr (£)    | Cr (£)
-------------|---------------------------|-----------|----------
XXXX         | [Account name]            | X,XXX.XX  |
XXXX         | [Account name]            |           | X,XXX.XX

Description: [Clear business narrative]
Prepared by: [Name]
Approved by: [Name]
Reversal:    [Auto-reverse / Permanent]
```
