---
name: controls-testing
description: Use this skill when the user discusses internal controls, audit preparation, control testing, deficiency classification, governance compliance, or risk assessment for a UK company. Provides comprehensive methodology aligned with UK Corporate Governance Code (2024), ISA (UK) 315/330/265, and Companies Act 2006.
---

# Internal Controls Testing — UK Framework

> This skill assists with internal controls assessment but does not constitute professional audit or legal advice. Statutory audits must be conducted by registered auditors.

## Regulatory Landscape

### UK Corporate Governance Code 2024 — Provision 29

**Effective:** Financial years beginning on or after 1 January 2026.

Provision 29 requires boards to:
1. **Monitor** risk management and internal controls throughout the year
2. Conduct at least an **annual review** covering all **material controls** (financial, operational, reporting, and compliance)
3. Provide a **declaration of effectiveness** in the annual report

The Code operates on a **comply-or-explain** basis — not a legal mandate. External assurance is not required.

**Important:** The UK has no SOX equivalent. The audit reform bill (ARGA/CRA) has been effectively shelved. Provision 29 is the only operative internal controls requirement — and only for premium-listed companies on a comply-or-explain basis. However, best practice extends these principles to all companies seeking robust governance.

### ISA (UK) Standards

| Standard | Purpose |
|----------|---------|
| **ISA (UK) 315** | Identifying and Assessing the Risks of Material Misstatement |
| **ISA (UK) 330** | The Auditor's Responses to Assessed Risks |
| **ISA (UK) 265** | Communicating Deficiencies in Internal Control |

### Companies Act 2006

- **s.393** — Directors must not approve accounts unless they give a true and fair view
- **s.414C** — Strategic report must include principal risks and uncertainties
- **s.172** — Directors' duty to promote the success of the company

## Deficiency Classification

ISA (UK) 265 uses two tiers (the US term "Material Weakness" was deliberately removed from international standards):

| Classification | Definition | Communication Required |
|---------------|------------|----------------------|
| **Deficiency in internal control** | A control unable to prevent, detect, or correct misstatements; or a missing control | Communicate to management |
| **Significant deficiency** | Of sufficient importance to merit the attention of those charged with governance | **In writing** to governance and management |

For internal assessment purposes, this plugin uses a three-tier system:

| Tier | Description | Action Required |
|------|-------------|-----------------|
| **High** | Could result in material misstatement or significant financial loss | Immediate remediation; escalate to board |
| **Medium** | Increases risk but has compensating controls or limited exposure | Remediation within 3 months; report to FD |
| **Low** | Minor improvement opportunity | Include in next review cycle |

## Control Categories

### 1. Entity-Level Controls

| Control Area | UK-Specific Considerations |
|-------------|---------------------------|
| Tone at the top / governance | UK Corporate Governance Code; board composition; independent NEDs |
| Risk management | Principal risks per s.414C; board risk appetite statement |
| Code of conduct / ethics | Whistleblowing (PIDA 1998); Bribery Act 2010 |
| Internal audit | Not mandatory for all; Provision 25 (premium listed only) |
| IT general controls | UK GDPR / Data Protection Act 2018; Cyber Essentials |
| Anti-fraud | Bribery Act 2010; Corporate Criminal Offence (failure to prevent tax evasion) |

### 2. Financial Reporting Controls

| Process | Key Controls | Testing Approach |
|---------|-------------|-----------------|
| **Revenue / Turnover** | Contract review, performance obligation ID (post-2026), cut-off | Inspect contracts; test cut-off; recalculate |
| **Purchases / AP** | PO authorisation, GRN matching, invoice approval, payment approval | Three-way match; verify approval limits |
| **Payroll** | Starters/leavers, pay rate changes, RTI accuracy, pension compliance | Recalculate PAYE/NIC; verify RTI |
| **Cash / Banking** | Bank rec review, payment dual-authorisation, bank mandate control | Review recs; test authorisation levels |
| **Fixed Assets** | Capex authorisation, physical verification, depreciation review | Inspect approvals; verify existence |
| **VAT** | Output VAT, input VAT, partial exemption, MTD submission | Reconcile VAT control; test invoice treatment |
| **Financial Close** | Checklist completion, JE review, management review | Verify procedures; test JE approvals |

### 3. IT General Controls

| Domain | Key Controls |
|--------|-------------|
| Access management | Starters/leavers for system access; SoD; admin access review |
| Change management | Change approval; test-to-prod separation; rollback |
| Operations | Backup/recovery; BCP; incident management |
| Data protection | UK GDPR compliance; DPAs; breach procedures; DPIAs |

## Sample Size Guidance

| Control Frequency | Population | Suggested Sample |
|-------------------|-----------|-----------------|
| Daily | ~250/year | 25–30 |
| Weekly | ~52/year | 10–15 |
| Monthly | 12/year | 5–6 |
| Quarterly | 4/year | All 4 |
| Annual | 1/year | Test the single occurrence |

## Workpaper Template

```
INTERNAL CONTROLS TEST WORKPAPER

Entity:          [Company name]
Period:          [Testing period]
Process:         [e.g., Revenue, Payroll, Cash]
Control:         [Description of the control being tested]
Control owner:   [Name and role]
Control type:    [Manual / Automated / IT-dependent manual]
Frequency:       [Daily / Weekly / Monthly / Quarterly / Annual]

Test objective:  [What the test aims to confirm]
Test approach:   [Inspection / Observation / Enquiry / Re-performance]
Sample:          [Sample size and selection method]

Findings:
[Detailed description of results — exceptions identified, root causes]

Classification:  [High / Medium / Low]
Recommendation:  [Remediation action]

Tested by:       [Name]          Date: DD/MM/YYYY
Reviewed by:     [Name]          Date: DD/MM/YYYY
```

## Applicability by Company Type

| Company Type | Framework | Controls Depth |
|-------------|-----------|---------------|
| **Sole trader / Freelancer** | Best practice only | Basic: bank rec, expense tracking, tax records |
| **Micro-entity** | Companies Act; no audit required | Basic financial controls; VAT, PAYE accuracy |
| **Small company** | Companies Act; audit exempt | Moderate: key financial controls, segregation where possible |
| **Medium company** | Companies Act; statutory audit | Comprehensive: all financial reporting and ITGC |
| **Large / Listed** | UK Corporate Governance Code; ISA (UK) | Full Provision 29 declaration |
