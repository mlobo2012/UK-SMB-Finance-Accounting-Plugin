# UK SMB Finance & Accounting Plugin

A UK finance and accounting plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Supports month-end close, journal entry preparation, purchase invoice scanning, account reconciliation, financial statement generation, variance analysis, VAT reconciliation, MTD filing, Companies House compliance, and internal controls testing — all under FRS 102/IFRS, Companies Act 2006, and HMRC regulations.

Built for **sole traders, freelancers, and SMBs** operating in the UK.

> **Recommended model**: For best results, use the latest **Claude Opus** model. The plugin's skills involve complex UK tax calculations, multi-step regulatory logic, and nuanced accounting standards (FRS 102, Companies Act, HMRC rules) that benefit significantly from Opus-level reasoning. Sonnet will work for simpler tasks but may produce less reliable outputs on edge cases like partial exemption, FX translation reserves, or director's loan s.455 calculations.

> **Important**: This plugin assists with UK finance and accounting workflows but does not provide financial, tax, or audit advice. All outputs should be reviewed by qualified financial professionals before use in financial reporting, regulatory filings, or audit documentation. Tax rates and thresholds reflect the 2025/26 tax year and should be verified against current HMRC guidance.

## Installation

```bash
claude plugins add UK-SMB-Finance-Accounting-Plugin/finance-uk
```

## Commands

| Command | Description |
|---------|-------------|
| `/journal-entry` | Journal entry preparation — generate accruals, fixed asset entries, prepaids, payroll (employer NIC, auto-enrolment pension), and revenue entries with FRS 102 treatment, GBP amounts, and DD/MM/YYYY dates |
| `/financial-statements` | Financial statement generation — produce P&L (Companies Act Format 1 or 2), Balance Sheet, Cash Flow Statement, and Statement of Changes in Equity with period-over-period comparison |
| `/reconciliation` | Account reconciliation — compare GL balances to subledger, bank (BACS/Faster Payments/Open Banking), or intercompany balances and identify reconciling items |
| `/variance-analysis` | Variance/flux analysis — decompose variances into price/volume/mix drivers with narrative explanations, waterfall analysis, and UK-specific considerations |
| `/internal-controls` | Internal controls testing — generate testing workpapers, sample selections, and control assessments aligned with UK Corporate Governance Code 2024 and ISA (UK) |
| `/scan-invoices` | Purchase invoice scanning — convert scanned PDFs into page images, extract UK purchase ledger data from invoices and credit notes, validate it, and build an `.xlsx` workbook for VAT review |
| `/vat-reconciliation` | VAT reconciliation — reconcile the VAT control account and prepare the 9-box MTD return with output/input VAT analysis and partial exemption handling |
| `/mtd-filing` | Making Tax Digital — prepare VAT quarterly returns and ITSA quarterly updates via HMRC API, with filing deadlines and penalty regime guidance |
| `/companies-house` | Companies House filings — prepare annual accounts, confirmation statements, classify company size, check audit exemption, and track filing deadlines with late penalty schedule |

## Skills

| Skill | Description |
|-------|-------------|
| `journal-entry-prep` | JE preparation best practices, standard UK accrual types, FRS 102 recognition criteria, capital allowances (AIA £1M, full expensing, WDA), approval matrices, and documentation standards |
| `close-management` | Month-end close checklist with 5-day calendar including VAT reconciliation, PAYE payment deadlines (22nd electronic), annual close activities, accelerated 3-day close option, and sole trader simplified close |
| `controls-testing` | UK Corporate Governance Code 2024 Provision 29, ISA (UK) 265 deficiency classification, sample size guidance, workpaper templates, and applicability matrix by company type (sole trader through listed) |
| `payroll-uk` | Complete 2025/26 payroll reference — PAYE bands, employee NIC (8%/2%), employer NIC (15%), Employment Allowance (£10,500), auto-enrolment pension (3%/5%/8%), student loans, statutory payments, RTI, and P11D |
| `scan-invoices` | Purchase invoice OCR orchestration with corrupt-file handling, 5-page extraction batches, arithmetic and duplicate validation, and workbook generation for purchase ledgers |

## Example Workflows

### Month-End Close

1. Run `/journal-entry ap-accrual 2025-04` to generate AP accrual entries
2. Run `/journal-entry prepaid 2025-04` to amortise prepaid expenses
3. Run `/journal-entry fixed-assets 2025-04` to book depreciation with capital allowance guidance
4. Run `/journal-entry payroll 2025-04` to book PAYE, employer NIC, and pension accruals
5. Run `/reconciliation bank 2025-04` to reconcile bank accounts via Open Banking
6. Run `/vat-reconciliation 2025-Q1` to reconcile the VAT control account
7. Run `/financial-statements monthly 2025-04` to generate the P&L with flux analysis

### VAT Return & MTD Filing

1. Run `/scan-invoices "/path/to/purchase-invoices" --quarter 2025-Q2` to build the purchase ledger workbook from scanned supplier invoices
2. Review the Invoice Register and Validation Report sheets for low-confidence items or duplicates
3. Run `/vat-reconciliation 2025-Q2` to reconcile output and input VAT
4. Review the 9-box return preparation and check for partial exemption
5. Run `/mtd-filing vat 2025-Q2` to walk through the HMRC MTD submission workflow
6. Verify filing deadline and penalty regime exposure

### Purchase Invoice Scanner

1. Run `/scan-invoices "/path/to/purchase-invoices"` to process a full invoice folder
2. Optional: add `--quarter 2025-Q3` to flag out-of-period invoices
3. Optional: add `--sample-pages 15 --seed 42` to do a reproducible QA pass before the full run
4. Review the generated workbook sheets: Invoice Register, VAT Summary, Validation Report, and Processing Log


### Variance Analysis

1. Run `/variance-analysis turnover 2025-Q1 vs 2024-Q1` to analyse revenue variances
2. Run `/variance-analysis opex 2025-04 vs budget` to investigate operating expense variances
3. Review the waterfall analysis and employer NIC / pension impact breakdown

### Companies House Filing

1. Run `/companies-house annual-accounts 2024-25` to prepare annual accounts filing
2. Review company size classification and audit exemption eligibility
3. Run `/companies-house confirmation-statement 2025` to prepare the confirmation statement
4. Check filing deadlines and late penalty exposure

### Internal Controls Testing

1. Run `/internal-controls vat-compliance 2025-Q1` to test VAT controls
2. Run `/internal-controls payroll 2025-Q1` to test PAYE, NIC, and pension controls
3. Run `/internal-controls revenue-recognition 2025-Q1` to test revenue controls with FRS 102 version awareness
4. Review deficiency classifications per ISA (UK) 265

## FRS 102 Version Toggle

This plugin supports both pre- and post-January 2026 FRS 102 rules. On first use, it will proactively ask which version applies to your accounting period.

| Area | Pre-January 2026 | Post-January 2026 |
|------|-------------------|-------------------|
| Revenue | Risks-and-rewards transfer | IFRS 15 five-step model |
| Leases | Operating / finance classification | On-balance-sheet per IFRS 16 model |
| Goodwill | Amortised over useful life | Same treatment |

## MCP Integration

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

This plugin works best when connected to your UK financial data sources via MCP servers. Add the relevant servers to your `.mcp.json`:

### Accounting Software

Connect your accounting platform (e.g., Sage, Xero UK, FreeAgent, QuickBooks UK) MCP server to pull trial balances, subledger data, and journal entries automatically.

### Tax Filing (HMRC)

Connect the HMRC MTD API server to submit VAT returns, pull filing obligations, and manage ITSA quarterly updates with OAuth 2.0 authentication and fraud prevention headers.

### Statutory Filing (Companies House)

Connect the Companies House API server to look up company details, filing history, and submission deadlines.

### Banking

Connect via Open Banking (TrueLayer, Yapily, or Plaid) for automated bank feeds and reconciliation. Connect Wise for multi-currency transaction data and FX conversion at period-end mid-market rates.

### Payroll

Connect your payroll provider (e.g., Sage Payroll, BrightPay, Moorepay, IRIS) to pull RTI data, PAYE/NIC calculations, and pension contributions for journal entry preparation.

### Data Warehouse

Connect your data warehouse (e.g., Snowflake, BigQuery) MCP server to query financial data, run variance analysis, and pull historical comparisons.

### Collaboration

Connect Slack, Microsoft 365, or Gmail for sending reports, requesting approvals, and close status updates.

> **Note:** Connect your accounting software and banking MCP servers to pull financial data automatically. Without these, you can paste data or upload files for analysis.

## Configuration

Add your data source MCP servers to the `mcpServers` section of `.mcp.json` in this plugin directory. The `recommendedCategories` field lists the types of integrations that enhance this plugin's capabilities:

- `accounting-software` — Sage, Xero UK, FreeAgent, or QuickBooks UK for GL, subledger, and JE data
- `tax-filing` — HMRC MTD API for VAT returns and ITSA quarterly updates
- `statutory-filing` — Companies House API for annual accounts and confirmation statements
- `banking` — Open Banking and Wise for bank feeds and multi-currency transactions
- `payroll` — Payroll provider for RTI data, PAYE/NIC, and pension journals
- `data-warehouse` — Data warehouse for financial queries and historical data
- `office-suite` — Microsoft 365 or Google Workspace for workpaper generation
- `analytics-bi` — Power BI, Sage Intelligence, or Tableau for dashboards and KPI data
- `email` — Email for sending reports and requesting approvals
- `chat` — Team communication for close status updates and questions

## UK Tax Rates & Thresholds (2025/26)

This plugin embeds current rates across all skills. Key figures:

| Rate | Value |
|------|-------|
| Corporation Tax (main) | 25% (profits > £250K) |
| Corporation Tax (small profits) | 19% (profits ≤ £50K) |
| VAT standard rate | 20% |
| VAT registration threshold | £90,000 |
| Employer NIC | 15% above £5,000/year |
| Employment Allowance | £10,500/year |
| Personal Allowance | £12,570 |
| AIA (Annual Investment Allowance) | £1,000,000 |

## Supported Business Types

| Type | Supported Features |
|------|-------------------|
| **Sole traders / Freelancers** | Simplified close, MTD ITSA, SA100, Statement of Assets & Liabilities |
| **Micro-entities** | FRS 105, abridged balance sheet, minimal notes |
| **Small companies** | FRS 102 Section 1A, filleted accounts, audit exemption |
| **Medium companies** | Full FRS 102/IFRS, Companies House filing, all controls testing |
| **LLPs & Partnerships** | SA800, partner capital accounts, profit allocation |
