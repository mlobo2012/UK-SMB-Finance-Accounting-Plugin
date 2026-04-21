#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys

from common import LookupErrorWithContext, dump_json, lookup_parameter, parse_date


def main() -> int:
    parser = argparse.ArgumentParser(description="Look up an effective-dated rate or threshold.")
    parser.add_argument("--regime", required=True, help="Regime file name, for example payroll or vat.")
    parser.add_argument("--parameter", required=True, help="Parameter key inside the regime file.")
    parser.add_argument("--event-date", required=True, help="Lookup date in YYYY-MM-DD format.")
    parser.add_argument("--jurisdiction", help="Optional jurisdiction filter for future expansion.")
    args = parser.parse_args()

    try:
      result = lookup_parameter(args.regime, args.parameter, parse_date(args.event_date))
      print(dump_json(result))
      return 0
    except LookupErrorWithContext as exc:
      print(dump_json(exc.to_dict()))
      return 2


if __name__ == "__main__":
    raise SystemExit(main())
