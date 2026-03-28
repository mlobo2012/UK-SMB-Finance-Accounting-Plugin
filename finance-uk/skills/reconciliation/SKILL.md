---
name: reconciliation
description: Perform account reconciliations for UK businesses — bank reconciliation (Open Banking/BACS/FPS), GL-to-subledger, intercompany matching, and VAT control account. All amounts in GBP.
argument-hint: "<type> <period> — types: bank, gl-subledger, intercompany"
---

# Reconciliation Command — /reconciliation

> This skill assists with account reconciliation but does not constitute professional accounting advice.

## Arguments

The user invoked this with: $ARGUMENTS

Parse the arguments to determine:
- **Type:** One of `bank`, `gl-subledger`, `intercompany`
- **Period:** Format `YYYY-MM` (e.g., `2025-09`)

## Bank Reconciliation

### Step 1: Obtain Data

- **GL cash balance** from ~~accounting software
- **Bank statement balance** from ~~banking (Open Banking API preferred for real-time feeds; alternatively CSV/OFX import)
- For Wise multi-currency accounts, convert to GBP using the Wise mid-market rate at period end

### Step 2: Identify Reconciling Items

| Category | UK-Specific Notes |
|----------|-------------------|
| **Unpresented payments** | BACS payments follow a 3-day cycle — submitted Day 1, settle Day 3. Faster Payments settle in seconds but may show timing differences at cut-off. Cheques are rare but take 2 working days via Image Clearing System. |
| **Receipts not yet credited** | Direct Debit collections follow the same 3-day BACS cycle. Standing orders and Faster Payments may show timing differences. |
| **Bank charges and interest** | Record bank charges to administrative expenses. Interest received/paid to appropriate income/expense accounts. |
| **Direct Debit / standing order differences** | BACS Direct Debits protected by the Direct Debit Guarantee — customers can claim refunds for incorrect amounts. Check for reversed Direct Debits. |
| **Foreign currency transactions** | Translate at the exchange rate on the transaction date (FRS 102 Section 30). Re-translate monetary items at closing rate at period end. |

### Step 3: Prepare Reconciliation

Present in this format:

```
Bank Reconciliation as at DD/MM/YYYY
Entity: [Company name]

Balance per bank statement                          £XX,XXX.XX
Add: Receipts not yet credited
  [Date] [Description]                    £X,XXX.XX
                                                    £XX,XXX.XX
Less: Unpresented payments
  [Date] [Payee] [Ref]                   (£X,XXX.XX)
  [Date] [Payee] [Ref]                   (£X,XXX.XX)
                                                   (£XX,XXX.XX)

Adjusted bank balance                               £XX,XXX.XX

Balance per general ledger                           £XX,XXX.XX
Add/Less: Adjustments
  [Bank charges not yet recorded]         (£XXX.XX)
  [Interest received not yet recorded]     £XXX.XX
                                                     £XX,XXX.XX

Adjusted GL balance                                  £XX,XXX.XX

Difference                                           £0.00
```

### Step 4: Escalation Thresholds

| Unreconciled Amount | Action Required |
|---------------------|-----------------|
| < £500 | Investigate and resolve within current close cycle |
| £500 – £5,000 | Escalate to Management Accountant; resolve within 5 business days |
| £5,000 – £25,000 | Escalate to Financial Controller; investigate root cause |
| > £25,000 | Escalate to Finance Director; potential board notification |

For sole traders and micro-entities, thresholds should be proportionate to turnover.

### Step 5: Ageing Analysis

```
Ageing of Unreconciled Items as at DD/MM/YYYY

Ref  | Date       | Description              | Amount (£)  | Age (Days) | Status
-----|------------|--------------------------|-------------|------------|--------
001  | 15/09/2025 | BACS payment – Supplier A | (£2,340.00) | 15         | Under investigation
002  | 28/09/2025 | FPS receipt – Client B    |  £1,750.00  | 2          | Timing – expected to clear
```

## GL-to-Subledger Reconciliation

Match the general ledger control account balance to the subledger detail:

- **Trade debtors control** → Sales ledger aged debtors listing
- **Trade creditors control** → Purchase ledger aged creditors listing
- **VAT control** → VAT return boxes (refer to the vat-reconciliation skill for the detailed procedure)
- **PAYE/NIC creditor** → RTI submissions and P32 employer payment record
- **Pension creditor** → Pension provider statements


### VAT Position Verification

When reconciling accounts for businesses with international income, verify VAT treatment:

- **B2B exports of services** — outside scope of UK VAT (place of supply is the customer's country under VATA 1994 s.7A). Include in Box 6 value but zero in Box 1.
- **Domestic UK purchases with VAT** — input VAT reclaimable if valid tax invoice held.
- **Mixed currency income** — translate to GBP at transaction date rate for VAT purposes.

## Intercompany Reconciliation

For group companies, match intercompany balances:
- Confirm balances agree between entities
- Investigate and resolve differences before consolidation
- Eliminate intercompany transactions in consolidated accounts
- Ensure transfer pricing documentation is in place where applicable

Always use **GBP (£)** and **DD/MM/YYYY** dates throughout.
