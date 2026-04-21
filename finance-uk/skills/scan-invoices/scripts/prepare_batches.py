#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split a scan manifest into extraction batches.")
    parser.add_argument("--manifest-path", required=True, help="Path to manifest.json")
    parser.add_argument("--output-dir", required=True, help="Directory for batch manifest files")
    parser.add_argument("--batch-size", type=int, default=3, help="Pages per batch. Default: 3")
    return parser.parse_args()


def chunk(items: list[dict[str, object]], size: int) -> list[list[dict[str, object]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, list):
        raise SystemExit(f"Manifest must be a JSON array: {manifest_path}")

    batches = []
    for index, pages in enumerate(chunk(manifest, args.batch_size), start=1):
        batch_id = f"{index:03d}"
        payload = {
            "batch_id": batch_id,
            "batch_size": len(pages),
            "pages": pages,
        }
        batch_path = output_dir / f"batch_{batch_id}_manifest.json"
        batch_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        batches.append(
            {
                "batch_id": batch_id,
                "batch_path": str(batch_path),
                "page_count": len(pages),
                "page_refs": [str(page["page_ref"]) for page in pages],
            }
        )

    summary_path = output_dir / "batches.json"
    summary_path.write_text(json.dumps(batches, indent=2), encoding="utf-8")
    print(f"Prepared {len(batches)} batch file(s) in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
