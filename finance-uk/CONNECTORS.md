# Connectors — UK Finance & Accounting Plugin

This plugin uses tool category placeholders (~~category) in skill files to remain
tool-agnostic. When a skill references ~~accounting software, it means whichever
accounting platform is connected via MCP.

## Tool Categories

| Category | Placeholder | Recommended UK Platforms |
|----------|-------------|------------------------|
| **Accounting Software** | ~~accounting software | Sage 50, Sage 200, Sage Business Cloud, Xero UK, FreeAgent, QuickBooks UK, Kashflow |
| **Data Warehouse** | ~~data warehouse | Snowflake, BigQuery, Amazon Redshift |
| **Email** | ~~email | Microsoft 365 (Outlook), Gmail |
| **Office Suite** | ~~office suite | Microsoft 365 (Excel, Word), Google Workspace |
| **Chat** | ~~chat | Slack, Microsoft Teams |
| **Payroll** | ~~payroll | Sage Payroll, BrightPay, Moorepay, IRIS, Moneysoft |
| **Tax Filing** | ~~tax filing | HMRC MTD API (VAT), HMRC Corporation Tax Online, HMRC ITSA |
| **Statutory Filing** | ~~statutory filing | Companies House API, iXBRL tagging software |
| **Banking** | ~~banking | Open Banking API (via TrueLayer/Yapily/Plaid), Wise API, Starling Bank API |
| **Analytics / BI** | ~~analytics | Power BI, Sage Intelligence, Tableau |

## Connection Notes

- **Sage** dominates UK SMB accounting. Sage 50 (desktop) and Sage Business Cloud (online)
  have different APIs. Sage 200 serves larger SMBs.
- **Xero UK** has built-in MTD VAT filing and Open Banking bank feeds.
- **FreeAgent** is purpose-built for UK freelancers and sole traders, with Self Assessment
  and simplified VAT.
- **HMRC MTD API** requires OAuth 2.0 via Government Gateway, mandatory fraud prevention
  headers, and developer registration at developer.service.hmrc.gov.uk.
- **Companies House API** uses a simple API key and provides free access to public company data.
- **Open Banking** provides real-time bank feeds — replaces manual CSV imports for
  bank reconciliation. UK has 327+ regulated providers and 16M+ user connections.
- **Wise API** is essential for freelancers and SMBs with international income streams,
  providing multi-currency balance and transaction data.
