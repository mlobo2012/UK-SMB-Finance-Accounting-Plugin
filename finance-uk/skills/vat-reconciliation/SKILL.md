---
name: vat-reconciliation
description: Perform VAT control account reconciliation and prepare the 9-box MTD return for UK businesses. Reconciles output VAT, input VAT, and net liability. Handles standard, reduced, zero-rated, exempt, and reverse charge transactions.
argument-hint: "<period> — format: YYYY-QX (e.g., 2025-Q2)"
---

# VAT Reconciliation Command — /vat-reconciliation

> This skill assists with VAT reconciliation and return preparation but does not constitute professional tax advice. Consult a VAT specialist for complex transactions or partial exemption calculations.

## Arguments

The user invoked this with: $ARGUMENTS

Parse the period (e.g., `2025-Q2` for April–June 2025).

## VAT Rates (2025/26)

| Rate | Percentage | Common Applications |
|------|-----------|---------------------|
| **Standard** | **20%** | Most goods and services |
| **Reduced** | **5%** | Domestic fuel/power, children's car seats, sanitary products |
| **Zero** | **0%** | Food (most), children's clothing, books/newspapers, public transport |
| **Exempt** | N/A | Financial services, insurance, education, health, land/property |
| **Outside scope** | N/A | Wages, dividends, non-business activities, statutory fees |

**Registration threshold:** £90,000 (rolling 12-month taxable turnover)
**Deregistration threshold:** £88,000

## Step 1: Extract Data

From ~~accounting software, extract:
- All sales transactions with VAT analysis
- All purchase transactions with VAT analysis
- Opening balance on VAT control account(s)
- Previous period VAT return amounts and payment
- Any EU/international transactions (reverse charge, imports, exports)

## Step 2: Reconcile Output VAT

```
Output VAT Reconciliation — [Quarter]

                                                Net (£)        VAT (£)
Standard-rated sales (20%)                     XXX,XXX         XX,XXX
Reduced-rated sales (5%)                         X,XXX            XXX
Zero-rated sales (0%)                           XX,XXX              —
Exempt sales                                     X,XXX              —
                                               --------       --------
Total turnover                                 XXX,XXX

Output VAT per sales analysis                                  XX,XXX
Output VAT per GL (VAT output control account)                 XX,XXX
                                                              --------
Difference                                                         £0
```

## Step 3: Reconcile Input VAT

```
Input VAT Reconciliation — [Quarter]

                                                Net (£)        VAT (£)
Standard-rated purchases (20%)                  XX,XXX          X,XXX
Reduced-rated purchases (5%)                     X,XXX            XXX
Zero-rated purchases (0%)                        X,XXX              —
Exempt purchases                                 X,XXX              —
Capital expenditure VAT                          X,XXX          X,XXX
                                               --------       --------
Total input VAT claimable                                       X,XXX

Input VAT per purchase analysis                                 X,XXX
Input VAT per GL (VAT input control account)                    X,XXX
                                                              --------
Difference                                                         £0
```

**Partial exemption:** If the business makes both taxable and exempt supplies, apply the standard method (or HMRC-agreed special method). De minimis: exempt input tax ≤ £625/month average AND ≤ 50% of total input tax.

## Step 4: Prepare 9-Box Return

| Box | Description | Amount (£) |
|-----|-------------|------------|
| **1** | VAT due on sales and other outputs | XX,XXX |
| **2** | VAT due on acquisitions from other EC member states (post-Brexit: NI Protocol only; zero for GB-only businesses) | XXX |
| **3** | Total VAT due (Box 1 + Box 2) | XX,XXX |
| **4** | VAT reclaimed on purchases and other inputs | X,XXX |
| **5** | Net VAT to pay HMRC or reclaim (Box 3 − Box 4) | X,XXX |
| **6** | Total value of sales excl. VAT | XXX,XXX |
| **7** | Total value of purchases excl. VAT | XX,XXX |
| **8** | Total value of supplies of goods to EC member states | X,XXX |
| **9** | Total value of acquisitions of goods from EC member states | X,XXX |

**Post-Brexit:** Boxes 8 and 9 retained for Northern Ireland Protocol transactions only. For GB-only businesses with no NI goods movements, these are zero.

## Step 5: Reconcile to GL

```
VAT Control Account Reconciliation — [Quarter]

                                                              £
Opening balance (liability to HMRC)                         X,XXX
Add: Output VAT charged in period (Box 1)                  XX,XXX
Add: Acquisition VAT in period (Box 2)                        XXX
Less: Input VAT claimed in period (Box 4)                  (X,XXX)
Less: Payment to HMRC for prior period                     (X,XXX)
                                                           --------
Closing balance (= Box 5 for current period)                X,XXX

Per GL VAT control account closing balance                  X,XXX
                                                           --------
Difference                                                      £0
```

## Step 6: Filing Checklist

- [ ] VAT return figures agree to reconciliation workpaper
- [ ] All reconciling differences investigated and resolved
- [ ] Partial exemption calculation performed (if applicable)
- [ ] Bad debt relief claimed for invoices > 6 months overdue and written off (VAT Act 1994 s.36)
- [ ] Reverse charge correctly applied on relevant supplies
- [ ] Capital goods scheme adjustments made (if applicable)
- [ ] Return reviewed and approved by Financial Controller / FD
- [ ] Filed via MTD-compatible software before deadline (1 month + 7 days after quarter end)
- [ ] Payment arranged by same deadline

## Common VAT Errors to Check

1. **Incorrect rate applied** — particularly on mixed supplies
2. **VAT on non-deductible items** — business entertainment, non-business use
3. **Missing tax invoices** — input VAT cannot be claimed without valid tax invoice
4. **Timing errors** — VAT point rules: basic tax point = date goods removed/made available or services performed; actual tax point = invoice date (if within 14 days of basic) or payment date (if before basic)
5. **Flat Rate Scheme misapplication** — output VAT = flat rate % × gross turnover (VAT-inclusive)
6. **Domestic reverse charge (construction)** — supplies between CIS-registered businesses

## Filing Deadlines (Quarterly Filers)

| Quarter Ending | Filing & Payment Deadline |
|---------------|-------------------------|
| 31 March | 7 May |
| 30 June | 7 August |
| 30 September | 7 November |
| 31 December | 7 February |
