---
name: scan-invoices
description: Scan folders of purchase invoice PDFs, extract UK purchase ledger data from page images, validate it, and build an Excel workbook ready for VAT review.
argument-hint: "<folder> [--quarter YYYY-QX] [--vat-rate 20] [--sample-pages N] [--seed 42]"
---

# Purchase Invoice Scanner — /scan-invoices

Use this skill to turn scanned purchase invoice PDFs into a structured purchase ledger workbook.

This workflow is designed for **purchase invoices and credit notes only**. It is not for sales invoices, bank statements, or general document OCR.

> Recommended model: **Sonnet**. This skill relies on batched vision extraction. If the current session is not using a Sonnet-class model, warn the user before continuing.

## Arguments

The user invoked this with: $ARGUMENTS

Parse:
- Required: folder path containing one or more PDFs
- Optional: `--quarter YYYY-QX`
- Optional: `--vat-rate <percent>` where the default is `20`
- Optional: `--sample-pages <N>` for QA runs where only a randomized subset should be rendered
- Optional: `--seed <N>` for reproducible sampling, default `42`

Interpret UK VAT quarters as:
- `2025-Q1` = Apr-Jun 2025
- `2025-Q2` = Jul-Sep 2025
- `2025-Q3` = Oct-Dec 2025
- `2025-Q4` = Jan-Mar 2026

## Workflow

### 1. Validate Access

1. Confirm the folder exists and contains PDFs.
2. If the folder is outside Claude Code's allowed directories, tell the user to run `/add-dir <folder>` or restart Claude with `--add-dir <folder>`, then continue.

### 2. Resolve the Installed Script Directory

Before running anything, find the plugin's script directory by searching both:
- the current working tree;
- `~/.claude/plugins`.

Use the first exact match for:
- `skills/scan-invoices/scripts/convert_pdfs.py`
- `skills/scan-invoices/scripts/ocr_focus.swift`
- `skills/scan-invoices/scripts/prepare_batches.py`
- `skills/scan-invoices/scripts/merge_results.py`
- `skills/scan-invoices/scripts/build_workbook.py`
- `skills/scan-invoices/scripts/requirements.txt`

Reuse those absolute paths for the rest of the run.

### 3. Prepare the Run Directory

Create a run folder inside the invoice directory:

```text
<input-folder>/.scan-invoices/<timestamp>/
```

Use these child paths:
- `manifest.json`
- `conversion_summary.json`
- `batches/`
- `results/`
- `logs/`
- `.venv/`
- `purchase_ledger.xlsx`

If `--sample-pages` was supplied, keep that run isolated and mention that the workbook only covers the sampled pages.

### 4. Ensure Python Dependencies

Check whether the runtime can import `openpyxl`, `pdf2image`, and `PIL`.

Prefer a run-local virtualenv:

```bash
python3 -m venv <run>/.venv
<run>/.venv/bin/python -m pip install -r <requirements.txt>
```

Use `<run>/.venv/bin/python` for all subsequent script invocations in that run.

Only if a virtualenv is not possible in the current environment, fall back to:

```bash
python3 -m pip install --break-system-packages -r <requirements.txt>
```

### 5. Convert PDFs to Page Images

Run `convert_pdfs.py` with:
- `--input-folder`
- `--output-root`
- `--dpi 200`
- optional `--sample-pages`
- optional `--seed`

Then read `conversion_summary.json` and report:
- readable PDFs;
- skipped corrupt PDFs;
- pages rendered.

### 6. Add OCR Hints for Header and Footer Fields

Run:

```bash
swift <ocr_focus.swift> --manifest-path <run>/manifest.json --output-path <run>/manifest.json
```

This enriches each manifest entry with local Vision OCR text and candidate hints for:
- invoice number;
- supplier VAT registration;
- invoice date.

### 7. Split the Manifest Into Batches

Run `prepare_batches.py` using:
- `--manifest-path <run>/manifest.json`
- `--output-dir <run>/batches`
- `--batch-size 3`

Use the generated `batch_XXX_manifest.json` files as the extraction queue.

### 8. Extract Data With Vision Subagents

Prefer **up to 5 Task subagents in parallel**. If the Task tool is unavailable, process batches sequentially in the main agent.

For each batch:
1. Read the batch manifest JSON.
2. Use the listed file references for each page:
   - the full page image;
   - the header crop;
   - the footer crop.
3. Write the result to `<run>/results/batch_XXX.json`.

Each extraction task should follow this prompt template exactly, with the batch-specific file references injected:

```text
You are a UK purchase invoice data extractor. You are processing a single batch manifest plus up to 5 invoice pages. Each page may include a full-page image plus focused header/footer crops to help verify exact digits. The batch manifest may also include local OCR hints from macOS Vision for invoice number, VAT registration, and date fields.

Batch manifest:
@<absolute path to batch manifest>

Attached page images:
- Page A full: @/absolute/path/to/page1.png
- Page A header crop: @/absolute/path/to/page1-header.png
- Page A footer crop: @/absolute/path/to/page1-footer.png
- Page B full: @/absolute/path/to/page2.png
- Page B header crop: @/absolute/path/to/page2-header.png
- Page B footer crop: @/absolute/path/to/page2-footer.png
- ...

For each page:

1. CLASSIFY: Is this a purchase invoice or credit note? If not, return:
   {"page_ref": "<ref>", "is_invoice": false, "skip_reason": "<reason>"}

2. EXTRACT: If it is a purchase invoice or credit note, return:

{
  "page_ref": "<pdf_name>:page_<number>",
  "is_invoice": true,
  "invoice_number": "<string>",
  "supplier_name": "<string>",
  "supplier_vat_reg": "<string or null>",
  "tax_point_date": "<DD/MM/YYYY>",
  "line_items": [
    {
      "description": "<string>",
      "qty": <number>,
      "unit_price": <number>,
      "line_total": <number>
    }
  ],
  "net_total": <number>,
  "vat_amount": <number>,
  "vat_rate_percent": <number>,
  "gross_total": <number>,
  "is_credit_note": <boolean>,
  "confidence": "high" | "medium" | "low",
  "notes": "<any issues>"
}

Rules:
- First transcribe the header fields before you look at line items.
- Use the header and footer crops to verify exact invoice numbers, VAT registration numbers, supplier names, and dates.
- Use the OCR hints in the batch manifest as a secondary check for exact digits. Prefer values where the OCR hint agrees with what you can see in the crop. If the OCR hint conflicts with the crop, trust the crop and explain the conflict in `notes`.
- `invoice_number`, `supplier_name`, `supplier_vat_reg`, `tax_point_date`, `net_total`, `vat_amount`, and `gross_total` are the critical fields. Re-check them against the printed header/footer boxes before finalising output.
- Preserve every digit exactly as printed, including leading zeroes and long invoice numbers.
- For `supplier_vat_reg`, inspect the seller masthead, footer, or any `VAT`, `VAT Reg No`, or `VAT #` label. If it is printed and legible, copy it exactly. Only return `null` when it is truly absent or unreadable.
- All amounts are GBP and must keep the printed invoice values.
- Do not calculate totals that are not printed.
- Use the printed totals boxes as the primary source for `net_total`, `vat_amount`, and `gross_total`.
- Do not shift prices or quantities onto the wrong product description. If a line item is partially obscured or the mapping is ambiguous, keep the description if useful but set uncertain numeric fields to `null` instead of guessing.
- It is acceptable to return fewer line items when some rows are unreadable. Accurate header fields and totals matter more than exhaustive line detail.
- If a field is unreadable, return null where appropriate, set confidence to low, and explain why in notes.
- Do not guess or invent values.
- Return a JSON array only, with one object per page.
- Write that JSON array to the designated batch output file.
```

After each round, report progress like:
- `Processed 25/80 batches`
- `Current pass: 125/400 pages`

### 9. Merge and Validate

Run `merge_results.py` with:
- `--manifest-path`
- `--batch-dir <run>/results`
- `--output-dir <run>/results`
- `--expected-vat-rate`
- optional `--quarter`

Use its outputs:
- `validated_invoices.json`
- `validation_flags.json`
- `processing_log.json`
- `merge_summary.json`

Surface:
- invoice count;
- credit note count;
- skipped pages;
- total net and VAT;
- flag count.

### 10. Build the Workbook

Run `build_workbook.py` with:
- `--validated-invoices`
- `--validation-flags`
- `--processing-log`
- `--output-path`

### 11. Final Response

Return:
- the workbook path;
- whether this was a full run or sampled QA run;
- total pages processed;
- invoices found vs skipped pages;
- total net and VAT amounts;
- number of validation flags;
- any corrupt PDFs skipped;
- if `--quarter` was supplied, remind the user of the relevant filing window.

## Operational Notes

- Corrupt PDFs should be skipped, not crash the run.
- Low-confidence invoices should stay in the register but be clearly flagged.
- Duplicate invoices are excluded from the final register and listed in the Validation Report.
- For QA or prompt-tuning work, use `--sample-pages` first before processing a full archive.
