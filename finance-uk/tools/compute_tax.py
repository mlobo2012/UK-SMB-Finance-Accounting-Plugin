#!/usr/bin/env python3

from __future__ import annotations

import argparse

from common import (
    LookupErrorWithContext,
    dump_json,
    get_parameter_definition,
    lookup_parameter,
    parse_date,
    parse_facts,
)


def compute_employer_nic_secondary(event_date: str, facts: dict) -> dict:
    annual_earnings = float(facts["annual_earnings"])
    allowance_remaining = float(facts.get("employment_allowance_remaining", 0))
    rate = lookup_parameter("payroll", "employer_nic_rate", parse_date(event_date))
    threshold = lookup_parameter("payroll", "employer_secondary_threshold_year", parse_date(event_date))
    nic_due = max(annual_earnings - float(threshold["value"]), 0) * float(rate["value"])
    nic_due = max(nic_due - allowance_remaining, 0)
    return {
        "ok": True,
        "calc_type": "employer_nic_secondary",
        "event_date": event_date,
        "inputs": facts,
        "result": {
            "annual_earnings": annual_earnings,
            "rate": rate["value"],
            "secondary_threshold": threshold["value"],
            "employment_allowance_remaining": allowance_remaining,
            "employer_nic_due": round(nic_due, 2)
        },
        "sources": [rate["source"], threshold["source"]],
    }


def compute_mtd_itsa_qualifying_income(event_date: str, facts: dict) -> dict:
    event = parse_date(event_date)
    self_employment_income = float(facts.get("self_employment_income", 0))
    property_income = float(facts.get("property_income", 0))
    qualifying_income = self_employment_income + property_income

    phase_definitions = [
        ("phase_3", get_parameter_definition("self_assessment", "mtd_itsa_phase_3_threshold")),
        ("phase_2", get_parameter_definition("self_assessment", "mtd_itsa_phase_2_threshold")),
        ("phase_1", get_parameter_definition("self_assessment", "mtd_itsa_phase_1_threshold")),
    ]

    active_phase = None
    active_threshold = None
    sources = []
    for phase_name, definition in phase_definitions:
        entry = definition["values"][0]
        sources.append(entry["source"])
        if parse_date(entry["effective_from"]) <= event:
            active_phase = phase_name
            active_threshold = float(entry["value"])
            break

    mandatory = bool(active_threshold is not None and qualifying_income > active_threshold)
    return {
        "ok": True,
        "calc_type": "mtd_itsa_qualifying_income",
        "event_date": event_date,
        "inputs": facts,
        "result": {
            "qualifying_income": qualifying_income,
            "phase": active_phase,
            "threshold": active_threshold,
            "mandatory": mandatory
        },
        "sources": sources,
    }


def compute_corporation_tax_band(event_date: str, facts: dict) -> dict:
    profits = float(facts["taxable_profits"])
    company_count_for_limits = int(facts.get("company_count_for_limits", 1))
    lower = lookup_parameter("corporation_tax", "lower_profits_limit", parse_date(event_date))
    upper = lookup_parameter("corporation_tax", "upper_profits_limit", parse_date(event_date))
    small_rate = lookup_parameter("corporation_tax", "small_profits_rate", parse_date(event_date))
    main_rate = lookup_parameter("corporation_tax", "main_rate", parse_date(event_date))

    adjusted_lower = float(lower["value"]) / max(company_count_for_limits, 1)
    adjusted_upper = float(upper["value"]) / max(company_count_for_limits, 1)

    if profits <= adjusted_lower:
        band = "small_profits_rate"
        headline_rate = small_rate["value"]
    elif profits > adjusted_upper:
        band = "main_rate"
        headline_rate = main_rate["value"]
    else:
        band = "marginal_relief"
        headline_rate = None

    return {
        "ok": True,
        "calc_type": "corporation_tax_band",
        "event_date": event_date,
        "inputs": facts,
        "result": {
            "taxable_profits": profits,
            "company_count_for_limits": company_count_for_limits,
            "adjusted_lower_limit": adjusted_lower,
            "adjusted_upper_limit": adjusted_upper,
            "band": band,
            "headline_rate": headline_rate
        },
        "sources": [
            small_rate["source"],
            main_rate["source"],
            lower["source"],
            upper["source"],
        ],
    }


CALCULATORS = {
    "employer_nic_secondary": compute_employer_nic_secondary,
    "mtd_itsa_qualifying_income": compute_mtd_itsa_qualifying_income,
    "corporation_tax_band": compute_corporation_tax_band,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded tax calculation backed by local deterministic data.")
    parser.add_argument("--calc-type", required=True, choices=sorted(CALCULATORS.keys()))
    parser.add_argument("--event-date", required=True, help="Calculation date in YYYY-MM-DD format.")
    parser.add_argument("--facts", required=True, help="JSON object with calculator inputs.")
    args = parser.parse_args()

    try:
        facts = parse_facts(args.facts)
        result = CALCULATORS[args.calc_type](args.event_date, facts)
        print(dump_json(result))
        return 0
    except LookupErrorWithContext as exc:
        print(dump_json(exc.to_dict()))
        return 2
    except KeyError as exc:
        err = LookupErrorWithContext("MissingFactError", f"Missing required input '{exc.args[0]}'.", {"calc_type": args.calc_type})
        print(dump_json(err.to_dict()))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
