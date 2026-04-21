# Deterministic Data Layer

This directory holds the time-bound source-of-truth records for the highest-risk
parts of the plugin:

- `rates/` for effective-dated rates, thresholds, fees, and policy flags
- `forms/` for authoritative form/page enumerations
- `deadlines/` for filing and payment deadline rules

Every record is intentionally local-file based so the plugin can stay
self-contained in Claude Code / Cowork without a backend service.

## Conventions

- `effective_from` and `effective_to` use ISO `YYYY-MM-DD`
- `status` is `enacted` or `announced`
- `source` should point to an official GOV.UK, HMRC, or Companies House source
- Missing records are treated as a refusal condition by the local tools

The local CLI tools in `../tools/` are the supported way to query this data.
