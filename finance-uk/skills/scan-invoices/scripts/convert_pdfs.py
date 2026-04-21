#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert scanned invoice PDFs into per-page PNGs and emit a manifest."
    )
    parser.add_argument("--input-folder", required=True, help="Folder containing PDF files.")
    parser.add_argument(
        "--output-root",
        help="Run output directory. Defaults to <input-folder>/.scan-invoices/latest.",
    )
    parser.add_argument(
        "--manifest-path",
        help="Explicit manifest path. Defaults to <output-root>/manifest.json.",
    )
    parser.add_argument(
        "--summary-path",
        help="Explicit summary path. Defaults to <output-root>/conversion_summary.json.",
    )
    parser.add_argument("--dpi", type=int, default=200, help="PNG render DPI. Default: 200.")
    parser.add_argument(
        "--sample-pages",
        type=int,
        default=0,
        help="Optional random sample size for QA runs. Default: render all pages.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used when --sample-pages is set. Default: 42.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return cleaned or "document"


def find_pdfs(folder: Path) -> list[Path]:
    pdfs = []
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        if path.name.startswith(".") or path.name.startswith("~$") or path.name.startswith(".~lock"):
            continue
        if path.suffix.lower() == ".pdf":
            pdfs.append(path)
    return pdfs


def get_page_count(pdf_path: Path) -> tuple[int | None, str | None]:
    command = ["pdfinfo", str(pdf_path)]
    try:
        proc = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None, "pdfinfo is not installed"

    if proc.returncode != 0:
        error = (proc.stderr or proc.stdout or "unknown pdfinfo failure").strip()
        return None, error

    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            raw_value = line.split(":", 1)[1].strip()
            try:
                return int(raw_value), None
            except ValueError:
                return None, f"unable to parse page count from '{raw_value}'"
    return None, "pdfinfo output did not include a Pages field"


def contiguous_ranges(page_numbers: list[int]) -> list[tuple[int, int]]:
    if not page_numbers:
        return []
    page_numbers = sorted(page_numbers)
    ranges: list[tuple[int, int]] = []
    start = end = page_numbers[0]
    for page in page_numbers[1:]:
        if page == end + 1:
            end = page
            continue
        ranges.append((start, end))
        start = end = page
    ranges.append((start, end))
    return ranges


def select_pages(
    all_pages: list[dict[str, object]],
    sample_pages: int,
    seed: int,
) -> list[dict[str, object]]:
    if sample_pages <= 0 or sample_pages >= len(all_pages):
        return sorted(all_pages, key=lambda item: (str(item["pdf_name"]), int(item["page_num"])))

    rng = random.Random(seed)
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in all_pages:
        grouped[str(item["pdf_name"])].append(item)

    if sample_pages >= len(grouped):
        chosen: list[dict[str, object]] = []
        leftovers: list[dict[str, object]] = []
        for entries in grouped.values():
            picked = rng.choice(entries)
            chosen.append(picked)
            leftovers.extend(
                candidate for candidate in entries if candidate["page_ref"] != picked["page_ref"]
            )
        remaining = sample_pages - len(chosen)
        if remaining > 0:
            chosen.extend(rng.sample(leftovers, remaining))
    else:
        chosen = rng.sample(all_pages, sample_pages)

    return sorted(chosen, key=lambda item: (str(item["pdf_name"]), int(item["page_num"])))


def render_pages(selected_pages: list[dict[str, object]], images_root: Path, dpi: int) -> None:
    grouped: dict[Path, list[dict[str, object]]] = defaultdict(list)
    for item in selected_pages:
        grouped[Path(str(item["pdf_path"]))].append(item)

    for pdf_path, entries in grouped.items():
        pdf_slug = slugify(pdf_path.stem)
        pdf_output_dir = images_root / pdf_slug
        pdf_output_dir.mkdir(parents=True, exist_ok=True)

        pages = [int(entry["page_num"]) for entry in entries]
        for range_start, range_end in contiguous_ranges(pages):
            prefix = pdf_output_dir / f"{pdf_slug}-{range_start:04d}-{range_end:04d}"
            command = [
                "pdftoppm",
                "-r",
                str(dpi),
                "-png",
                "-f",
                str(range_start),
                "-l",
                str(range_end),
                str(pdf_path),
                str(prefix),
            ]
            proc = subprocess.run(command, check=False, capture_output=True, text=True)
            if proc.returncode != 0:
                message = (proc.stderr or proc.stdout or "pdftoppm failed").strip()
                raise RuntimeError(f"Failed to render {pdf_path.name} pages {range_start}-{range_end}: {message}")

            rendered_by_page: dict[int, Path] = {}
            pattern = re.compile(rf"^{re.escape(prefix.name)}-(\d+)\.png$")
            for candidate in pdf_output_dir.iterdir():
                if not candidate.is_file():
                    continue
                match = pattern.match(candidate.name)
                if not match:
                    continue
                rendered_by_page[int(match.group(1))] = candidate

            for page_num in range(range_start, range_end + 1):
                temp_path = rendered_by_page.get(page_num)
                final_path = pdf_output_dir / f"{pdf_slug}-page-{page_num:04d}.png"
                if temp_path is None or not temp_path.exists():
                    raise RuntimeError(
                        f"Expected rendered page not found for {pdf_path.name} page {page_num}"
                    )
                temp_path.rename(final_path)
                create_focus_crops(final_path)


def create_focus_crops(image_path: Path) -> None:
    with Image.open(image_path) as image:
        width, height = image.size
        header_bottom = max(1, int(height * 0.42))
        footer_top = min(height - 1, int(height * 0.78))

        header_crop = image.crop((0, 0, width, header_bottom))
        footer_crop = image.crop((0, footer_top, width, height))

        header_crop.save(image_path.with_name(f"{image_path.stem}-header.png"))
        footer_crop.save(image_path.with_name(f"{image_path.stem}-footer.png"))


def attach_image_paths(selected_pages: list[dict[str, object]], images_root: Path) -> list[dict[str, object]]:
    enriched: list[dict[str, object]] = []
    for item in selected_pages:
        pdf_slug = slugify(Path(str(item["pdf_name"])).stem)
        image_base = images_root / pdf_slug / f"{pdf_slug}-page-{int(item['page_num']):04d}"
        enriched_item = dict(item)
        enriched_item["image_path"] = str(image_base.with_suffix(".png").resolve())
        enriched_item["header_crop_path"] = str(image_base.with_name(f"{image_base.name}-header.png").resolve())
        enriched_item["footer_crop_path"] = str(image_base.with_name(f"{image_base.name}-footer.png").resolve())
        enriched.append(enriched_item)
    return enriched


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_folder = Path(args.input_folder).expanduser().resolve()
    if not input_folder.exists() or not input_folder.is_dir():
        print(f"Input folder does not exist: {input_folder}", file=sys.stderr)
        return 1

    output_root = (
        Path(args.output_root).expanduser().resolve()
        if args.output_root
        else (input_folder / ".scan-invoices" / "latest").resolve()
    )
    images_root = output_root / "images"
    manifest_path = (
        Path(args.manifest_path).expanduser().resolve()
        if args.manifest_path
        else output_root / "manifest.json"
    )
    summary_path = (
        Path(args.summary_path).expanduser().resolve()
        if args.summary_path
        else output_root / "conversion_summary.json"
    )

    pdfs = find_pdfs(input_folder)
    if not pdfs:
        print(f"No PDF files found in {input_folder}", file=sys.stderr)
        return 1

    page_inventory: list[dict[str, object]] = []
    skipped_pdfs: list[dict[str, str]] = []
    for pdf_path in pdfs:
        page_count, error = get_page_count(pdf_path)
        if page_count is None:
            skipped_pdfs.append(
                {
                    "pdf_name": pdf_path.name,
                    "pdf_path": str(pdf_path),
                    "reason": error or "unable to determine page count",
                }
            )
            continue

        for page_num in range(1, page_count + 1):
            page_inventory.append(
                {
                    "pdf_name": pdf_path.name,
                    "pdf_path": str(pdf_path),
                    "page_num": page_num,
                    "page_ref": f"{pdf_path.name}:page_{page_num}",
                }
            )

    if not page_inventory:
        print("No readable PDF pages were found after integrity checks.", file=sys.stderr)
        return 1

    selected_pages = select_pages(page_inventory, args.sample_pages, args.seed)
    render_pages(selected_pages, images_root, args.dpi)
    manifest = attach_image_paths(selected_pages, images_root)

    summary = {
        "input_folder": str(input_folder),
        "output_root": str(output_root),
        "dpi": args.dpi,
        "seed": args.seed,
        "pdf_count": len(pdfs),
        "readable_pdf_count": len(pdfs) - len(skipped_pdfs),
        "skipped_pdf_count": len(skipped_pdfs),
        "total_pages_seen": len(page_inventory),
        "pages_rendered": len(manifest),
        "sample_mode": bool(args.sample_pages),
        "sample_pages_requested": args.sample_pages,
        "skipped_pdfs": skipped_pdfs,
    }

    write_json(manifest_path, manifest)
    write_json(summary_path, summary)

    skipped_note = ""
    if skipped_pdfs:
        skipped_note = f" ({len(skipped_pdfs)} skipped: {', '.join(item['pdf_name'] for item in skipped_pdfs)})"

    print(
        f"Rendered {len(manifest)} page(s) from {len(pdfs) - len(skipped_pdfs)} readable PDF(s){skipped_note}. "
        f"Manifest: {manifest_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
