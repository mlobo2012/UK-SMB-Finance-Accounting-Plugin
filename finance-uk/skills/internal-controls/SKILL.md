---
name: internal-controls
description: Run internal controls testing for UK companies — aligned with UK Corporate Governance Code, ISA (UK), and Companies Act 2006. Tests across 9 control domains.
user-invocable: true
argument-hint: "<scope> <period> — scopes: revenue-recognition, procure-to-pay, payroll, cash-management, fixed-assets, vat-compliance, financial-close, it-general-controls, entity-level"
allowed-tools: [Read, Glob, Grep]
---

# Internal Controls Testing Command — /internal-controls

> This skill assists with internal controls assessment but does not constitute a statutory audit or professional audit opinion.

## Arguments

The user invoked this with: $ARGUMENTS

Parse the arguments to determine:
- **Scope:** One of `revenue-recognition`, `procure-to-pay`, `payroll`, `cash-management`, `fixed-assets`, `vat-compliance`, `financial-close`, `it-general-controls`, `entity-level`
- **Period:** Format `YYYY-QX` or `YYYY-YY`

## Workflow

### Step 1: Scope Assessment

For the selected scope area:
1. Document the end-to-end process flow
2. Identify key controls that prevent or detect material misstatement
3. Assess design effectiveness
4. Determine testing approach: inspection, observation, enquiry, or re-performance

### Step 2: Execute Testing

Select sample per guidance (daily controls: 25–30; weekly: 10–15; monthly: 5–6; quarterly: all 4; annual: test the single occurrence). For each key control:

1. Execute the test procedure
2. Document results and exceptions
3. Classify deficiencies per ISA (UK) 265 principles (High / Medium / Low)

### Step 3: Scope-Specific Procedures

**For `vat-compliance`:**
1. Output VAT accuracy — correct rate applied (standard 20%, reduced 5%, zero 0%, exempt)
2. Input VAT validity — valid tax invoices only; partial exemption applied correctly
3. Reverse charge compliance — domestic reverse charge (CIS) and overseas services
4. VAT reconciliation — control account agrees to return before submission
5. MTD compliance — digital records, digital links, filed via MTD-compatible software
6. Filing timeliness — by deadline (1 month + 7 days after period end)

**For `payroll`:**
1. PAYE calculation accuracy — correct tax codes, cumulative vs week 1/month 1
2. NIC calculation accuracy — correct category letters, thresholds applied
3. RTI submission accuracy — FPS matches payroll records
4. Auto-enrolment compliance — eligible jobholders enrolled, correct contribution rates
5. Student loan deductions — correct plan type and threshold
6. Statutory payment calculations — SSP £118.75/week, SMP/SPP at correct rates
7. Employment Allowance — eligibility verified, £10,500 correctly offset
8. Starters and leavers — P45/P46 procedures followed

**For `revenue-recognition`:**
- Pre-2026: Test risks-and-rewards transfer per current FRS 102 Section 23
- Post-2026: Test five-step IFRS 15 model (contract identification, performance obligations, transaction price, allocation, satisfaction)

**For `entity-level`:**
- Board governance and composition
- Risk management framework and principal risks
- Whistleblowing policy (PIDA 1998)
- Bribery Act 2010 compliance programme
- UK GDPR / Data Protection Act 2018 compliance
- Corporate Criminal Offence — failure to prevent tax evasion
- Anti-money laundering procedures (if applicable)

### Step 4: Conclude and Report

```
INTERNAL CONTROLS TESTING REPORT

Entity:        [Company name]
Scope:         [Control area tested]
Period:        [Testing period]
Framework:     UK Corporate Governance Code 2024 / ISA (UK) 315/330/265

SUMMARY
Controls tested:                 [N]
Controls — effective:            [N] (X%)
Controls — deficiency noted:     [N] (X%)
  Of which:
    High:                        [N]
    Medium:                      [N]
    Low:                         [N]

DETAILED FINDINGS

[Control 1]
Control description:   [Description]
Test performed:        [Procedure]
Sample:                [Size and selection]
Result:                EFFECTIVE / DEFICIENCY NOTED
Classification:        [High / Medium / Low]
Finding:               [Description of issue]
Recommendation:        [Remediation action]
Owner:                 [Responsible person]
Target date:           DD/MM/YYYY

Prepared by:           [Name]     Date: DD/MM/YYYY
Reviewed by:           [Name]     Date: DD/MM/YYYY
```
