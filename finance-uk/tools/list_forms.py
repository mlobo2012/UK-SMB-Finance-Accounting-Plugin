#!/usr/bin/env python3

from __future__ import annotations

import argparse

from common import LookupErrorWithContext, dump_json, list_forms, parse_date


def main() -> int:
    parser = argparse.ArgumentParser(description="List applicable form metadata for a regime.")
    parser.add_argument("--regime", required=True, choices=["ct600", "self_assessment", "companies_house"])
    parser.add_argument("--event-date", required=True, help="Filter date in YYYY-MM-DD format.")
    args = parser.parse_args()

    try:
        forms = list_forms(args.regime, parse_date(args.event_date))
        print(dump_json({
            "ok": True,
            "regime": args.regime,
            "event_date": args.event_date,
            "forms": forms,
        }))
        return 0
    except LookupErrorWithContext as exc:
        print(dump_json(exc.to_dict()))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
