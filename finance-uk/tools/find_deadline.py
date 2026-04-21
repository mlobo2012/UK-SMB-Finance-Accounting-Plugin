#!/usr/bin/env python3

from __future__ import annotations

import argparse

from common import LookupErrorWithContext, compute_deadline, dump_json, parse_facts


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute a filing or payment deadline from the local rule table.")
    parser.add_argument("--regime", required=True, help="Deadline rule id, for example vat_return or ct600.")
    parser.add_argument("--entity-type", default="any", help="Entity type label for future expansion.")
    parser.add_argument("--facts", default="{}", help="JSON object containing the required date facts.")
    args = parser.parse_args()

    try:
        facts = parse_facts(args.facts)
        result = compute_deadline(args.regime, facts)
        result["entity_type"] = args.entity_type
        print(dump_json(result))
        return 0
    except LookupErrorWithContext as exc:
        print(dump_json(exc.to_dict()))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
