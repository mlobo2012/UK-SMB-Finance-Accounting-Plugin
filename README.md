# UK SMB Finance & Accounting Plugin

A Claude Code / Cowork plugin for UK finance and accounting workflows — journal entries, reconciliation, financial statements, VAT, MTD, payroll, Companies House, and internal controls. Built for sole traders, freelancers, and SMBs under FRS 102/IFRS, Companies Act 2006, and HMRC regulations.

> 🏗️ **Architecture:** This plugin is built on and derived from the
> official
> [Anthropic Finance & Accounting Plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance)
> (US version). All US-specific content has been replaced with verified
> UK equivalents — including FRS 102 instead of US-GAAP, HMRC VAT &
> MTD instead of US sales tax, employer NIC & auto-enrolment pension
> instead of FICA/401(k), plus new UK-specific skills (VAT
> Reconciliation, MTD Filing, Companies House, PAYE/RTI Payroll) with
> no US equivalent.

> **Getting the most out of this plugin?** If you need help with setup, want it customised to your firm's workflows, or just want to talk through what's possible — [reach out to AI Heroes](https://www.ai-heroes.co/contact). We're building these tools to be as valuable as possible and your input drives that.

## Commands

| Command | Description |
|---------|-------------|
| `/journal-entry` | Journal entry preparation — accruals, fixed assets, prepaids, payroll (employer NIC, auto-enrolment pension), revenue entries with FRS 102 treatment |
| `/financial-statements` | Financial statements — P&L (Companies Act Format 1/2), Balance Sheet, Cash Flow, with period comparison |
| `/reconciliation` | Account reconciliation — GL vs. subledger, bank (BACS/Faster Payments/Open Banking), intercompany |
| `/variance-analysis` | Variance/flux analysis — price/volume/mix decomposition with narrative and waterfall charts |
| `/internal-controls` | Internal controls testing — workpapers, sample selections, UK Corporate Governance Code 2024, ISA (UK) |
| `/vat-reconciliation` | VAT reconciliation — VAT control account, 9-box MTD return, partial exemption handling |
| `/mtd-filing` | Making Tax Digital — VAT quarterly returns and ITSA updates via HMRC API, deadlines and penalties |
| `/companies-house` | Companies House — annual accounts, confirmation statements, size classification, audit exemption, filing deadlines |

## Skills (auto-activated)

| Skill | Description |
|-------|-------------|
| journal-entry-prep | JE best practices, FRS 102 recognition, capital allowances (AIA £1M, full expensing, WDA), approval matrices |
| journal-entry | JE command workflow with UK chart of accounts reference |
| reconciliation | Reconciliation methodology including bank, subledger, and intercompany |
| financial-statements | P&L, Balance Sheet, Cash Flow under Companies Act / FRS 102 with flux analysis |
| variance-analysis | Variance decomposition with UK materiality thresholds (ISA UK 320) |
| close-management | Month-end close checklist with VAT deadlines, PAYE 22nd payment, annual close activities |
| controls-testing | UK Corporate Governance Code 2024 Provision 29, ISA (UK) 265 deficiency classification |
| internal-controls | Full ICS assessment framework for UK entities |
| vat-reconciliation | VAT control account reconciliation, 9-box return, partial exemption, reverse charge |
| mtd-filing | HMRC MTD VAT & ITSA filing workflow, API bridging, penalty regime |
| companies-house | Companies Act 2006 filing requirements, size thresholds, late penalties |
| payroll-uk | 2025/26 PAYE bands, NIC (employee 8%/2%, employer 15%), Employment Allowance, auto-enrolment, RTI, P11D |

## Configuration

### Annual Rate Updates

At each tax year start (6 April), update `config/rates-2025-26.json` with the new tax year values and adjust the reference in `plugin.json`. All skills read rates from this file.

### MCP Integration

This plugin works best with MCP servers connected to your financial data. Add the relevant servers in `.mcp.json`:

- **Accounting** (e.g. Xero, Sage, FreeAgent, QuickBooks) — trial balances, journal entries, invoices
- **Payroll** (e.g. Sage Payroll, BrightPay, Gusto UK) — PAYE, NIC, pension data
- **Banking** (e.g. Open Banking, Plaid, TrueLayer) — bank feeds, BACS/FPS matching
- **HMRC** (e.g. MTD API, Government Gateway) — VAT returns, ITSA submissions
- **Data Warehouse** (e.g. Snowflake, BigQuery) — analysis, historical comparisons

Without MCP servers, you can paste data or upload files for analysis.

## Example Workflows

### Month-End Close April 2026

```
/journal-entry payroll 2026-04
```

Claude books PAYE, employer NIC (15%), auto-enrolment pension (3% employer / 5% employee), and statutory payments with correct GL coding.

### VAT Return Q1 2026

```
/vat-reconciliation 2026-Q1
```

Claude reconciles output/input VAT, prepares the 9-box MTD return, handles partial exemption and reverse charge, and walks through the HMRC submission.

### Annual Accounts 2025-26

```
/financial-statements annual 2025-26 --format companies-act
```

Claude generates P&L (Format 1), Balance Sheet, and notes under Companies Act / FRS 102 with prior year comparison and size classification.

## Repository Structure

```
├── finance-uk/                          # The plugin (canonical source)
│   ├── .claude-plugin/plugin.json       # Plugin manifest
│   ├── skills/                          # 12 skill files (8 invocable + 4 background)
│   ├── README.md                        # Full plugin documentation
│   ├── [CONNECTORS.md](finance-uk/CONNECTORS.md) # MCP connector categories
│   ├── .mcp.json                        # MCP server configuration
│   └── LICENSE                          # Apache 2.0 + Commons Clause
│
└── .gitignore                           # Git ignore rules
```

## Installation

### Option 1: Claude Desktop — Drag & Drop (recommended)

1. Download the latest `.zip` from the [Releases page](https://github.com/mlobo2012/UK-SMB-Finance-Accounting-Plugin/releases)
2. In the Claude Desktop app, go to **Plugins** → **Upload plugin**
3. Drag and drop the zip file — the plugin installs automatically

> **Note:** The zip is a snapshot. When updates are available, download the latest release and reinstall.

### Option 2: Claude Code CLI

```bash
# Clear any previous cache first
rm -rf ~/.claude/plugins/marketplaces/*UK*
rm -rf ~/.claude/plugins/cache/*UK*

# Step 1: Add this repo as a plugin marketplace
claude plugins marketplace add mlobo2012/UK-SMB-Finance-Accounting-Plugin

# Step 2: Install the plugin
claude plugins install finance-uk@UK-SMB-Finance-Accounting-Plugin
```

> **Troubleshooting:** If you get "not found" errors, clear the cache directories above and try again. The marketplace name in the install command is `UK-SMB-Finance-Accounting-Plugin` (not the GitHub path).

### Option 3: Clone and point

```bash
git clone https://github.com/mlobo2012/UK-SMB-Finance-Accounting-Plugin.git
claude --plugin-dir ./UK-SMB-Finance-Accounting-Plugin/finance-uk
```

After installation, use `/journal-entry`, `/reconciliation`, `/vat-reconciliation`, etc.

## Documentation

See [finance-uk/README.md](finance-uk/README.md) for full plugin documentation including commands, skills, example workflows, and tax rates.

See [finance-uk/CONNECTORS.md](finance-uk/CONNECTORS.md) for MCP connector categories and recommended UK platforms.

## Author

Built by [AI Heroes](https://www.ai-heroes.co).

## License

[Apache 2.0 + Commons Clause](finance-uk/LICENSE) — free for private and internal business use. Commercial resale is not permitted.
