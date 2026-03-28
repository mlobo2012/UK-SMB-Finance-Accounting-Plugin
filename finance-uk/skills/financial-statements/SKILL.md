---
name: financial-statements
description: Generate UK financial statements per FRS 102/IFRS — Profit and Loss Account (Format 1 and 2), Balance Sheet (Companies Act format), Cash Flow Statement, and Statement of Changes in Equity. Supports company size-aware presentation with configurable statutory templates.
argument-hint: "<period-type> <period> — period-types: monthly, quarterly, annual, ytd"
---

# Financial Statements Command — /financial-statements

> This skill assists with financial statement preparation but does not constitute professional accounting advice. Statutory accounts must be approved by the directors and may require professional review or audit.

## Arguments

The user invoked this with: $ARGUMENTS

Parse the arguments to determine:
- **Period type:** One of `monthly`, `quarterly`, `annual`, `ytd`
- **Period:** `YYYY-MM` for monthly, `QX-YYYY` for quarterly, `YYYY-YY` for annual

## Step 1: Determine Presentation Framework

If not already established, proactively ask:

> "Which financial reporting framework applies?
> - **FRS 102** — UK GAAP (most private companies and SMBs)
> - **FRS 105** — Micro-entity regime (companies meeting micro-entity thresholds)
> - **IFRS** — International standards (mandatory for listed companies; optional for others)
>
> And which P&L format do you prefer?
> - **Format 1** — Cost of sales method (Turnover, Cost of sales, Gross profit...)
> - **Format 2** — Nature of expenditure method (Turnover, Raw materials, Staff costs, Depreciation...)
>
> Format 1 is more common for trading businesses. Format 2 is common for service businesses."

## Step 2: Determine Company Size

Ask the user for (or retrieve from ~~accounting software): annual turnover, balance sheet total, and average number of employees.

Classify using Companies Act 2006 thresholds (SI 2024/1303, for FY beginning on or after 6 April 2025):

| Category | Turnover | Balance Sheet | Employees |
|----------|----------|---------------|-----------|
| **Micro** | ≤ £1,000,000 | ≤ £500,000 | ≤ 10 |
| **Small** | ≤ £15,000,000 | ≤ £7,500,000 | ≤ 50 |
| **Medium** | ≤ £54,000,000 | ≤ £27,000,000 | ≤ 250 |

Must meet **2 of 3** criteria. Size determines: filing deadlines, audit exemption, abridged accounts, and required disclosures.

## Step 3: Generate Financial Statements

### Profit and Loss Account — Format 1 (Cost of Sales Method)

Per Companies Act 2006, Schedule 1 (SI 2008/410):

```
[Company Name]
Profit and Loss Account
for the [period/year] ended DD/MM/YYYY

                                              Note    £'000     £'000
Turnover                                       X     X,XXX
Cost of sales                                        (X,XXX)
                                                     ------
Gross profit                                          X,XXX

Distribution costs                                   (X,XXX)
Administrative expenses                              (X,XXX)
Other operating income                                  XXX
                                                     ------
Operating profit                                      X,XXX

Income from fixed asset investments              X       XXX
Other interest receivable and similar income     X       XXX
Interest payable and similar expenses            X      (XXX)
                                                     ------
Profit on ordinary activities before taxation         X,XXX

Tax on profit on ordinary activities             X      (XXX)
                                                     ------
Profit for the financial year                         X,XXX
                                                     ======
```

### Profit and Loss Account — Format 2 (Nature of Expenditure Method)

```
[Company Name]
Profit and Loss Account
for the [period/year] ended DD/MM/YYYY

                                              Note    £'000     £'000
Turnover                                       X     X,XXX
Change in stocks of finished goods and WIP               XXX
Own work capitalised                                     XXX
Other operating income                                   XXX
                                                     ------
                                                      X,XXX

Raw materials and consumables                        (X,XXX)
Other external expenses                                (XXX)
Staff costs                                    X    (X,XXX)
  (a) Wages and salaries                  (X,XXX)
  (b) Social security costs                 (XXX)
  (c) Other pension costs                   (XXX)
Depreciation and amounts written off
  tangible and intangible fixed assets       X        (XXX)
Other operating expenses                              (XXX)
                                                     ------
Operating profit                                      X,XXX

Income from fixed asset investments              X       XXX
Other interest receivable and similar income     X       XXX
Interest payable and similar expenses            X      (XXX)
                                                     ------
Profit on ordinary activities before taxation         X,XXX

Tax on profit on ordinary activities             X      (XXX)
                                                     ------
Profit for the financial year                         X,XXX
                                                     ======
```

### Balance Sheet — Companies Act Format 1

UK convention: fixed assets first.

```
[Company Name]
Balance Sheet as at DD/MM/YYYY

                                              Note    £'000     £'000
A. Called up share capital not paid                       XXX

B. Fixed assets
  I.   Intangible assets                   X             XXX
  II.  Tangible assets                     X           X,XXX
  III. Investments                         X             XXX
                                                     ------
                                                      X,XXX
C. Current assets
  I.   Stocks                              X             XXX
  II.  Debtors                             X           X,XXX
  III. Investments                                       XXX
  IV.  Cash at bank and in hand                        X,XXX
                                                     ------
                                                      X,XXX

D. Prepayments and accrued income                        XXX

E. Creditors: amounts falling due
   within one year                         X          (X,XXX)
                                                     ------
F. Net current assets (liabilities)                   X,XXX

G. Total assets less current liabilities              X,XXX

H. Creditors: amounts falling due after
   more than one year                      X            (XXX)

I. Provisions for liabilities              X            (XXX)

J. Accruals and deferred income                         (XXX)
                                                     ------
                                                      X,XXX
                                                     ======
K. Capital and reserves
  I.   Called up share capital              X             XXX
  II.  Share premium account                             XXX
  III. Revaluation reserve                               XXX
  IV.  Other reserves                                    XXX
  V.   Profit and loss account                         X,XXX
                                                     ------
                                                      X,XXX
                                                     ======
```

**Directors' approval statement (required):**
> "These accounts were approved by the board of directors on [date] and signed on its behalf by [Director name], Director. Company registration number: [number]."

**Small company note:** For the small companies regime, include:
> "These accounts have been prepared in accordance with the provisions applicable to companies subject to the small companies regime."

### Cash Flow Statement

Per FRS 102 Section 7 (indirect method):

```
[Company Name]
Cash Flow Statement
for the [period/year] ended DD/MM/YYYY

                                                      £'000
Cash flows from operating activities
  Profit for the financial year                        X,XXX
  Adjustments for:
    Depreciation of tangible assets                      XXX
    Amortisation of intangible assets                    XXX
    Interest receivable                                 (XXX)
    Interest payable                                     XXX
    Tax expense                                          XXX
  Changes in:
    Stocks                                              (XXX)
    Trade and other debtors                             (XXX)
    Trade and other creditors                            XXX
                                                     ------
  Cash generated from operations                       X,XXX
  Interest paid                                         (XXX)
  Tax paid                                              (XXX)
                                                     ------
Net cash from operating activities                     X,XXX

Cash flows from investing activities
  Purchase of tangible fixed assets                    (XXX)
  Proceeds from sale of tangible fixed assets            XXX
  Interest received                                      XXX
                                                     ------
Net cash used in investing activities                   (XXX)

Cash flows from financing activities
  Proceeds from bank borrowings                          XXX
  Repayment of bank borrowings                         (XXX)
  Dividends paid                                       (XXX)
                                                     ------
Net cash from (used in) financing activities             XXX
                                                     ------
Net increase (decrease) in cash and cash equivalents   X,XXX
Cash and cash equivalents at beginning of period       X,XXX
                                                     ------
Cash and cash equivalents at end of period             X,XXX
                                                     ======
```

**Small company exemption:** Entities qualifying as small under s.382 are exempt from preparing a cash flow statement (FRS 102 para 1.12(e)). Proactively inform the user: "As a small company, you're exempt from preparing a cash flow statement, but you may choose to prepare one voluntarily for management purposes."

### Sole Trader / Self-Employed Presentation

For sole traders, the balance sheet is replaced by a **Statement of Assets and Liabilities** and there are no Companies Act format requirements. Equity is simply the proprietor's capital account.


## Step 3a: FX Translation Differences

For companies with foreign currency transactions (e.g., USD or EUR income):

1. **Identify FX exposure** — monetary items (debtors, creditors, bank balances) denominated in foreign currency
2. **Translate at closing rate** — re-translate all foreign currency monetary items at the period-end exchange rate (FRS 102 Section 30)
3. **Calculate translation difference** — the difference between the rate used to record the transaction and the closing rate
4. **Book the FX gain/loss** — recognise in profit or loss for the period

```
Dr/Cr  Foreign exchange gain/loss (P&L)     £X,XXX
  Cr/Dr  Trade debtors / Bank / Creditors      £X,XXX
```

**FX translation reserve:** Where the P&L is translated at average rate and the balance sheet at closing rate, a translation difference will arise. This should be posted to an FX translation reserve within equity (other reserves) and disclosed in the notes. Do not leave this difference unreconciled.

> **Prompt:** "Do you have any foreign currency balances or transactions? If so, what closing exchange rates should we use for period-end translation?"

## Step 4: Apply FRS 102 Version-Specific Treatments

**Pre-January 2026:**
- Revenue: risks-and-rewards model (FRS 102 Section 23 current)
- Leases: operating/finance distinction — operating leases off-balance-sheet, straight-line expense
- Goodwill: amortised, rebuttable presumption ≤ 5 years (max 10 years)
- Financial instruments: Sections 11/12 (basic at amortised cost, other at FVTPL)
- Deferred tax: timing difference plus approach (Section 29)

**Post-January 2026:**
- Revenue: IFRS 15 five-step model (FRS 102 Section 23 revised)
- Leases: all leases on balance sheet as right-of-use asset + lease liability (exemptions for short-term ≤12m and low-value)
- Goodwill: unchanged (still amortised)
- Financial instruments: Sections 11/12 or IFRS 9 (IAS 39 option restricted)
- Deferred tax: unchanged, with new uncertain tax treatment guidance


## Step 5a: Related-Party and Director's Loan Reconciliation

For all companies with related-party balances (especially director's loans):

1. **Build the account from scratch** — do not work backwards from prior year totals. Start with opening balance, add each transaction, arrive at closing balance.
2. **Reconcile to source documents** — match every movement to bank statements, invoices, or board minutes.
3. **Check s.455 tax** — if director's loan account is overdrawn at year end, corporation tax at 33.75% is due on the balance (repayable if loan repaid within 9 months of year end).
4. **Disclosure** — FRS 102 Section 33 requires disclosure of all related-party transactions and balances, including terms and conditions.

## Step 5b: Comparative Period Restatement

When preparing comparative figures:

1. **Use filed accounts** as the starting point for prior year comparatives.
2. **Restate if classifications changed** — if you have reclassified items (e.g., moving a balance from debtors to other debtors), apply the same reclassification to the prior year for like-for-like comparison.
3. **Disclose restatements** — note any prior period adjustments or reclassifications in the accounting policies note.
4. **Flag material differences** — if prior year figures differ from the filed accounts, explain why in the notes.

## Step 5: Customisation

All templates are configurable. The user may:
- Add or remove line items within statutory categories
- Switch between Format 1 and Format 2 for the P&L
- Prepare abridged accounts (small companies with unanimous member consent)
- Prepare filleted accounts for Companies House (omit P&L and/or directors' report)
- Add comparative period columns
- Add budget columns for management accounts
- Present in £, £'000, or £m
