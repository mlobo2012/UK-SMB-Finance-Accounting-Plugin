#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path


MONEY_TOLERANCE_VAT = Decimal("0.02")
MONEY_TOLERANCE_GROSS = Decimal("0.01")
MONEY_TOLERANCE_LINES = Decimal("0.05")
CONFIDENCE_RANK = {"low": 1, "medium": 2, "high": 3}
DATE_FORMATS = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d %b %Y",
    "%d %B %Y",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge invoice extraction batches, validate them, and build clean JSON outputs."
    )
    parser.add_argument("--manifest-path", required=True, help="Path to manifest.json")
    parser.add_argument("--batch-dir", required=True, help="Directory containing batch_*.json files")
    parser.add_argument("--output-dir", required=True, help="Directory for merged outputs")
    parser.add_argument("--expected-vat-rate", type=float, default=20.0)
    parser.add_argument(
        "--quarter",
        help="Optional UK VAT quarter filter in YYYY-QX format. Example: 2025-Q3 for Oct-Dec 2025.",
    )
    return parser.parse_args()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    text = str(value).strip()
    if not text or text.lower() in {"null", "none", "nan"}:
        return None
    cleaned = (
        text.replace("£", "")
        .replace(",", "")
        .replace("(", "-")
        .replace(")", "")
        .replace("%", "")
        .strip()
    )
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def money_to_float(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value.quantize(Decimal("0.01")))


def parse_date(value: object) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()

    text = str(value).strip()
    if not text:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def normalise_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalise_key(value: object) -> str:
    return re.sub(r"[^A-Z0-9]+", "", normalise_text(value).upper())


def quarter_bounds(spec: str) -> tuple[date, date]:
    match = re.fullmatch(r"(\d{4})-Q([1-4])", spec.strip())
    if not match:
        raise ValueError(f"Invalid quarter format: {spec}")
    start_year = int(match.group(1))
    quarter = int(match.group(2))
    if quarter == 1:
        return date(start_year, 4, 1), date(start_year, 6, 30)
    if quarter == 2:
        return date(start_year, 7, 1), date(start_year, 9, 30)
    if quarter == 3:
        return date(start_year, 10, 1), date(start_year, 12, 31)
    return date(start_year + 1, 1, 1), date(start_year + 1, 3, 31)


def quarter_label(day: date | None) -> str:
    if day is None:
        return ""
    if 4 <= day.month <= 6:
        quarter = 1
        start_year = day.year
    elif 7 <= day.month <= 9:
        quarter = 2
        start_year = day.year
    elif 10 <= day.month <= 12:
        quarter = 3
        start_year = day.year
    else:
        quarter = 4
        start_year = day.year - 1
    end_year_short = str(start_year + 1)[-2:]
    return f"Q{quarter} {start_year}/{end_year_short}"


def is_valid_uk_vat_reg(value: str) -> bool:
    cleaned = re.sub(r"\s+", "", value.upper())
    return bool(re.fullmatch(r"(GB)?\d{9}", cleaned))


def make_flag(
    record: dict[str, object],
    flag_type: str,
    description: str,
    expected_value: object = "",
    actual_value: object = "",
) -> dict[str, str]:
    page_ref = normalise_text(record.get("page_ref"))
    suffix = f" ({page_ref})" if page_ref else ""
    return {
        "invoice_number": normalise_text(record.get("invoice_number")),
        "supplier": normalise_text(record.get("supplier_name")),
        "flag_type": flag_type,
        "description": f"{description}{suffix}",
        "expected_value": normalise_text(expected_value),
        "actual_value": normalise_text(actual_value),
    }


def extract_records(batch_path: Path) -> list[dict[str, object]]:
    payload = load_json(batch_path)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("records", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    raise ValueError(f"Batch file must contain a JSON array or records/results/items list: {batch_path}")


def classify_skip_reason(reason: str) -> str:
    lowered = reason.lower()
    if "blank" in lowered:
        return "Blank"
    if "delivery" in lowered:
        return "Delivery Note"
    if "statement" in lowered:
        return "Statement"
    if "credit" in lowered:
        return "Credit Note"
    if "packing" in lowered:
        return "Packing Slip"
    if "waste" in lowered:
        return "Waste Transfer Note"
    return reason.strip().title() or "Other"


def line_items_total(record: dict[str, object]) -> Decimal | None:
    line_items = record.get("line_items")
    if not isinstance(line_items, list) or not line_items:
        return None
    total = Decimal("0")
    found_any = False
    for item in line_items:
        if not isinstance(item, dict):
            continue
        line_total = parse_decimal(item.get("line_total"))
        if line_total is None:
            continue
        total += line_total
        found_any = True
    return total if found_any else None


def record_score(record: dict[str, object]) -> tuple[int, int, str]:
    confidence = normalise_text(record.get("confidence")).lower()
    score = CONFIDENCE_RANK.get(confidence, 2)
    essential_fields = (
        record.get("invoice_number"),
        record.get("supplier_name"),
        record.get("tax_point_date"),
        record.get("net_total"),
        record.get("vat_amount"),
        record.get("gross_total"),
    )
    completeness = sum(1 for field in essential_fields if normalise_text(field))
    return (score, completeness, normalise_text(record.get("page_ref")))


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest_path).expanduser().resolve()
    batch_dir = Path(args.batch_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_json(manifest_path)
    if not isinstance(manifest, list):
        print(f"Manifest must be a JSON array: {manifest_path}", file=sys.stderr)
        return 1

    quarter_start: date | None = None
    quarter_end: date | None = None
    if args.quarter:
        try:
            quarter_start, quarter_end = quarter_bounds(args.quarter)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    batch_files = sorted(
        path
        for path in batch_dir.iterdir()
        if path.is_file() and path.name.startswith("batch_") and path.suffix == ".json" and "_manifest" not in path.name
    )
    if not batch_files:
        print(f"No batch_*.json result files found in {batch_dir}", file=sys.stderr)
        return 1

    extraction_errors: list[dict[str, str]] = []
    page_records: dict[str, dict[str, object]] = {}
    duplicate_page_refs: set[str] = set()
    for batch_path in batch_files:
        try:
            records = extract_records(batch_path)
        except Exception as exc:  # noqa: BLE001
            extraction_errors.append({"batch_file": batch_path.name, "error": str(exc)})
            continue

        for record in records:
            page_ref = normalise_text(record.get("page_ref"))
            if not page_ref:
                extraction_errors.append(
                    {"batch_file": batch_path.name, "error": "record missing page_ref"}
                )
                continue
            if page_ref in page_records:
                duplicate_page_refs.add(page_ref)
                continue
            page_records[page_ref] = record

    flags: list[dict[str, str]] = []
    invoices: list[dict[str, object]] = []
    duplicate_invoice_refs: set[str] = set()
    today = date.today()
    older_than_cutoff = today - timedelta(days=365)

    for page_ref in sorted(duplicate_page_refs):
        record = page_records[page_ref]
        flags.append(make_flag(record, "ERROR", "Duplicate extraction result for the same page"))

    for record in page_records.values():
        if not record.get("is_invoice"):
            continue

        raw_confidence = normalise_text(record.get("confidence")).lower() or "medium"
        supplier_name = normalise_text(record.get("supplier_name"))
        invoice_number = normalise_text(record.get("invoice_number"))
        supplier_vat_reg = normalise_text(record.get("supplier_vat_reg"))
        record_date = parse_date(record.get("tax_point_date"))
        net_total = parse_decimal(record.get("net_total"))
        vat_amount = parse_decimal(record.get("vat_amount"))
        gross_total = parse_decimal(record.get("gross_total"))
        vat_rate_percent = parse_decimal(record.get("vat_rate_percent"))
        line_total_sum = line_items_total(record)

        record_flags: list[dict[str, str]] = []

        if not supplier_name:
            record_flags.append(make_flag(record, "ERROR", "Supplier name is missing"))
        if not invoice_number:
            record_flags.append(make_flag(record, "ERROR", "Invoice number is missing"))
        if record_date is None:
            record_flags.append(make_flag(record, "ERROR", "Tax point date is missing or unreadable"))
        if net_total is None:
            record_flags.append(make_flag(record, "ERROR", "Net total is missing or unreadable"))
        if vat_amount is None:
            record_flags.append(make_flag(record, "ERROR", "VAT amount is missing or unreadable"))
        if gross_total is None:
            record_flags.append(make_flag(record, "ERROR", "Gross total is missing or unreadable"))

        if net_total is not None and vat_amount is not None and vat_rate_percent is not None:
            expected_vat = (net_total * (vat_rate_percent / Decimal("100"))).quantize(Decimal("0.01"))
            if abs(vat_amount - expected_vat) > MONEY_TOLERANCE_VAT:
                record_flags.append(
                    make_flag(record, "ERROR", "VAT amount does not match net x VAT rate", expected_vat, vat_amount)
                )

        if net_total is not None and vat_amount is not None and gross_total is not None:
            expected_gross = (net_total + vat_amount).quantize(Decimal("0.01"))
            if abs(gross_total - expected_gross) > MONEY_TOLERANCE_GROSS:
                record_flags.append(
                    make_flag(record, "ERROR", "Gross total does not equal net + VAT", expected_gross, gross_total)
                )

        if line_total_sum is not None and net_total is not None and abs(line_total_sum - net_total) > MONEY_TOLERANCE_LINES:
            record_flags.append(
                make_flag(
                    record,
                    "ERROR",
                    "Line item totals do not add up to net total",
                    line_total_sum.quantize(Decimal("0.01")),
                    net_total,
                )
            )

        if record_date is not None:
            if record_date > today:
                record_flags.append(make_flag(record, "ERROR", "Tax point date is in the future", "", record_date.isoformat()))
            if record_date < older_than_cutoff:
                record_flags.append(
                    make_flag(record, "WARNING", "Tax point date is more than 12 months old", "", record_date.isoformat())
                )
            if quarter_start and quarter_end and not (quarter_start <= record_date <= quarter_end):
                record_flags.append(
                    make_flag(
                        record,
                        "WARNING",
                        f"Invoice date falls outside {args.quarter}",
                        f"{quarter_start.isoformat()} to {quarter_end.isoformat()}",
                        record_date.isoformat(),
                    )
                )

        if supplier_vat_reg:
            if not is_valid_uk_vat_reg(supplier_vat_reg):
                record_flags.append(make_flag(record, "WARNING", "Supplier VAT registration format looks invalid", "GB123456789", supplier_vat_reg))
        else:
            record_flags.append(
                make_flag(
                    record,
                    "WARNING",
                    "Supplier VAT registration missing. Input VAT cannot be reclaimed without a valid tax invoice.",
                )
            )

        error_count = sum(1 for flag in record_flags if flag["flag_type"] == "ERROR")
        warning_count = sum(1 for flag in record_flags if flag["flag_type"] == "WARNING")
        final_confidence = "high"
        if error_count > 0 or raw_confidence == "low":
            final_confidence = "low"
        elif warning_count > 0 or raw_confidence == "medium":
            final_confidence = "medium"

        cleaned_line_items = []
        for item in record.get("line_items") or []:
            if not isinstance(item, dict):
                continue
            cleaned_line_items.append(
                {
                    "description": normalise_text(item.get("description")),
                    "qty": money_to_float(parse_decimal(item.get("qty"))),
                    "unit_price": money_to_float(parse_decimal(item.get("unit_price"))),
                    "line_total": money_to_float(parse_decimal(item.get("line_total"))),
                }
            )

        notes = normalise_text(record.get("notes"))
        if error_count > 0:
            notes = " ".join(filter(None, [notes, "Validation errors detected."]))

        cleaned_record = {
            "page_ref": normalise_text(record.get("page_ref")),
            "invoice_number": invoice_number,
            "supplier_name": supplier_name,
            "supplier_vat_reg": supplier_vat_reg,
            "tax_point_date": record_date.strftime("%d/%m/%Y") if record_date else normalise_text(record.get("tax_point_date")),
            "tax_point_iso": record_date.isoformat() if record_date else "",
            "line_items": cleaned_line_items,
            "net_total": money_to_float(net_total),
            "vat_amount": money_to_float(vat_amount),
            "vat_rate_percent": money_to_float(vat_rate_percent),
            "gross_total": money_to_float(gross_total),
            "is_credit_note": bool(record.get("is_credit_note")),
            "confidence": final_confidence,
            "quarter_label": quarter_label(record_date),
            "notes": notes,
        }

        invoices.append(cleaned_record)
        flags.extend(record_flags)

    deduped_invoices: list[dict[str, object]] = []
    grouped_invoices: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for invoice in invoices:
        key = (
            normalise_key(invoice.get("invoice_number")),
            normalise_key(invoice.get("supplier_name")),
        )
        grouped_invoices[key].append(invoice)

    for key, group in grouped_invoices.items():
        if not key[0] or not key[1]:
            deduped_invoices.extend(group)
            continue
        group_sorted = sorted(group, key=record_score, reverse=True)
        winner = group_sorted[0]
        deduped_invoices.append(winner)
        for duplicate in group_sorted[1:]:
            duplicate_invoice_refs.add(normalise_text(duplicate.get("page_ref")))
            flags.append(
                make_flag(
                    duplicate,
                    "ERROR",
                    "Duplicate invoice number for the same supplier",
                    winner.get("page_ref"),
                    duplicate.get("page_ref"),
                )
            )

    deduped_invoices.sort(
        key=lambda item: (
            item.get("tax_point_iso") or "9999-12-31",
            normalise_text(item.get("supplier_name")),
            normalise_text(item.get("invoice_number")),
        )
    )

    processing_log = []
    invoice_count = 0
    credit_note_count = 0
    skipped_count = 0
    error_count = 0

    for entry in manifest:
        if not isinstance(entry, dict):
            continue
        page_ref = normalise_text(entry.get("page_ref"))
        record = page_records.get(page_ref)
        classification = "Other"
        invoice_number = ""
        status = "Error"

        if page_ref in duplicate_invoice_refs:
            classification = "Credit Note" if bool(record and record.get("is_credit_note")) else "Invoice"
            invoice_number = normalise_text(record.get("invoice_number") if record else "")
            status = "Skipped"
            skipped_count += 1
        elif record is None:
            classification = "Other"
            status = "Error"
            error_count += 1
        elif not record.get("is_invoice"):
            classification = classify_skip_reason(normalise_text(record.get("skip_reason")) or "Other")
            status = "Skipped"
            skipped_count += 1
        else:
            invoice_number = normalise_text(record.get("invoice_number"))
            if bool(record.get("is_credit_note")):
                classification = "Credit Note"
                credit_note_count += 1
            else:
                classification = "Invoice"
                invoice_count += 1
            status = "OK"

        processing_log.append(
            {
                "pdf_filename": normalise_text(entry.get("pdf_name")),
                "page_number": int(entry.get("page_num") or 0),
                "classification": classification,
                "invoice_number": invoice_number,
                "extraction_status": status,
                "page_ref": page_ref,
            }
        )

    validation_flags = sorted(
        flags,
        key=lambda item: (
            {"ERROR": 0, "WARNING": 1, "INFO": 2}.get(item["flag_type"], 3),
            item["supplier"],
            item["invoice_number"],
            item["description"],
        ),
    )

    summary = {
        "expected_vat_rate": args.expected_vat_rate,
        "quarter_filter": args.quarter or "",
        "invoices_kept": len(deduped_invoices),
        "invoice_pages": invoice_count,
        "credit_note_pages": credit_note_count,
        "skipped_pages": skipped_count,
        "errored_pages": error_count,
        "flag_count": len(validation_flags),
        "extraction_errors": extraction_errors,
        "total_net": round(sum(item.get("net_total") or 0 for item in deduped_invoices), 2),
        "total_vat": round(sum(item.get("vat_amount") or 0 for item in deduped_invoices), 2),
        "total_gross": round(sum(item.get("gross_total") or 0 for item in deduped_invoices), 2),
    }

    write_json(output_dir / "validated_invoices.json", deduped_invoices)
    write_json(output_dir / "validation_flags.json", validation_flags)
    write_json(output_dir / "processing_log.json", processing_log)
    write_json(output_dir / "merge_summary.json", summary)

    print(
        f"Merged {len(batch_files)} batch file(s): {len(deduped_invoices)} invoice(s), "
        f"{len(validation_flags)} flag(s). Output dir: {output_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
