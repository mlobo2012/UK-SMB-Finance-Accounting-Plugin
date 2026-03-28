---
name: journal-entry
description: Generate UK journal entries with correct FRS 102/IFRS treatment, GBP amounts, and UK-specific accrual types including employer NIC, auto-enrolment pension, and VAT.
argument-hint: "<type> <period> — types: ap-accrual, fixed-assets, prepaid, payroll, revenue"
---

# Journal Entry Command — /journal-entry

> This skill assists with journal entry generation but does not constitute professional accounting advice. Consult a qualified accountant for decisions affecting your business.

## Arguments

The user invoked this with: $ARGUMENTS

Parse the arguments to determine:
- **Type:** One of `ap-accrual`, `fixed-assets`, `prepaid`, `payroll`, `revenue`
- **Period:** Format `YYYY-MM` (e.g., `2025-09`)

## Workflow

### Step 1: Determine FRS 102 Version

If not already established in the conversation, proactively ask:

> "Which FRS 102 version applies to your current accounting period?
> - **Current rules** (periods beginning before 1 January 2026) — risks-and-rewards revenue model, operating/finance lease distinction
> - **Revised rules** (periods beginning on or after 1 January 2026) — IFRS 15 five-step revenue model, all leases on balance sheet (IFRS 16 model)
>
> This affects how revenue and lease entries are prepared."

### Step 2: Gather Context

Ask the user for, or query ~~accounting software for:
- Trial balance as at period end
- Outstanding purchase orders / GRNs without invoices (for AP accruals)
- Employee payroll summary (for payroll accruals)
- Revenue contracts and delivery status (for revenue accruals)
- Fixed asset register with depreciation schedules
- VAT return data for the period

### Step 3: Generate Entries by Type

**For `payroll` entries, include:**
- Gross wages and salaries
- Employee income tax (PAYE) deducted
- Employee NIC (Class 1 primary) deducted — 8% between £12,570 and £50,270, 2% above
- Student loan deductions (Plans 1/2/4/Postgraduate if applicable)
- Employee pension contributions deducted
- Employer NIC (Class 1 secondary) at **15%** above £417/month threshold
- Employer pension contributions (**minimum 3%** of qualifying earnings £520–£4,189/month)
- Apprenticeship Levy (0.5% if pay bill > £3M)
- Holiday pay accrual adjustment (5.6 weeks statutory minimum, always mandatory)
- Statutory payments (SSP at £118.75/week, SMP/SPP as applicable)
- Employment Allowance offset (£10,500/year)

**For `revenue` entries, apply the correct FRS 102 version:**
- Pre-2026: Risks-and-rewards transfer model
- Post-2026: Five-step IFRS 15 model (identify contract, identify obligations, determine price, allocate, recognise)

**For `fixed-assets` entries, show both:**
- Accounting depreciation (per entity policy, FRS 102 Section 17)
- Capital allowance position (AIA £1M, full expensing 100%/50%, WDA 18%/6%) for the tax computation

**For `ap-accrual` entries:**
- Identify goods/services received but not yet invoiced
- Accrue at best estimate of obligation
- Set up auto-reversal for the following period
- Include correct VAT treatment

**For `prepaid` entries:**
- Calculate the unexpired portion of prepaid expenses
- Release the current-period portion to the P&L
- Common items: insurance, rent, subscriptions, software licences

### Step 4: Validate

- Confirm all entries balance (total debits = total credits)
- Verify VAT treatment on each line (standard 20%, reduced 5%, zero 0%, exempt, outside scope)
- Check approval thresholds against the approval matrix:
  - < £5,000: Bookkeeper
  - £5,000–£40,000: Management Accountant / Financial Controller
  - £40,000–£200,000: Finance Director
  - > £200,000: FD + Board

### Step 5: Present

Output entries in UK format:

```
Date:        DD/MM/YYYY
Entity:      [Company name]
Period:      [Month YYYY]
Reference:   JE-YYYY-MM-NNN

Account Code | Account Name                    | Dr (£)      | Cr (£)
-------------|---------------------------------|-------------|------------
XXXX         | [Account name]                  | XX,XXX.XX   |
XXXX         | [Account name]                  |             | XX,XXX.XX

Description: [Clear business narrative]
Prepared by: [User]
Approved by: [Per approval matrix]
Reversal:    [Auto-reverse / Permanent]
VAT:         [Standard rated 20% / Zero rated / Exempt / Outside scope]
```

Always use:
- **GBP (£)** for all amounts
- **DD/MM/YYYY** for all dates
- UK terminology: "turnover" (not "revenue"), "creditors" (not "accounts payable"), "debtors" (not "accounts receivable"), "profit and loss account" (not "retained earnings")

### Key Reference: Approval Matrix

| Entry Value | Required Approver |
|-------------|-------------------|
| < £5,000 | Bookkeeper / Accounts Assistant |
| £5,000 – £40,000 | Management Accountant / Financial Controller |
| £40,000 – £200,000 | Finance Director (FD) / CFO |
| > £200,000 | FD/CFO + Board approval |

For sole traders and micro-entities, the approval matrix may be simplified to owner review for all entries above a self-determined threshold.

### Key Reference: Capital Allowances (2025/26)

| Allowance | Rate | Eligibility |
|-----------|------|-------------|
| Annual Investment Allowance (AIA) | 100% up to £1,000,000/year | Qualifying plant and machinery (excl. cars) |
| Full expensing | 100% (main rate) / 50% (special rate) | Companies only, new and unused P&M |
| Writing-down allowance — main pool | 18% reducing balance | Plant and machinery |
| Writing-down allowance — special rate | 6% reducing balance | Long-life assets, integral features |

Note: Main pool WDA rate drops to 14% from 1 April 2026.

### Key Reference: Documentation Standards

Every journal entry must include: preparer name and date, period and entity, clear description/narrative, supporting calculation reference, reversing indicator, account codes, and VAT treatment.

