#!/usr/bin/env python3

from __future__ import annotations

import calendar
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


class LookupErrorWithContext(Exception):
    def __init__(self, error: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.error = error
        self.message = message
        self.context = context or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": False,
            "error": self.error,
            "message": self.message,
            "context": self.context,
        }


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def iso_date(value: date) -> str:
    return value.isoformat()


def add_months(base: date, months: int) -> date:
    year = base.year + ((base.month - 1 + months) // 12)
    month = ((base.month - 1 + months) % 12) + 1
    day = min(base.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def fixed_day_second_following_month(base: date, day: int) -> date:
    second_following = add_months(date(base.year, base.month, 1), 2)
    return date(second_following.year, second_following.month, day)


def find_rate_file(regime: str) -> Path:
    path = DATA_DIR / "rates" / f"{regime}.json"
    if not path.exists():
        raise LookupErrorWithContext(
            "UnknownRegimeError",
            f"No rate file found for regime '{regime}'.",
            {"regime": regime},
        )
    return path


def get_parameter_definition(regime: str, parameter: str) -> Dict[str, Any]:
    data = load_json(find_rate_file(regime))
    parameters = data.get("parameters", {})
    if parameter not in parameters:
        raise LookupErrorWithContext(
            "UnknownParameterError",
            f"Parameter '{parameter}' is not defined for regime '{regime}'.",
            {"regime": regime, "parameter": parameter},
        )
    return parameters[parameter]


def find_forms_file(regime: str) -> Path:
    mapping = {
      "ct600": "ct600_supplementary.json",
      "self_assessment": "sa_supplementary.json",
      "companies_house": "companies_house_forms.json",
    }
    filename = mapping.get(regime)
    if not filename:
        raise LookupErrorWithContext(
            "UnknownRegimeError",
            f"No forms file found for regime '{regime}'.",
            {"regime": regime},
        )
    return DATA_DIR / "forms" / filename


def match_effective_window(values: Iterable[Dict[str, Any]], event_date: date) -> Dict[str, Any]:
    for entry in sorted(values, key=lambda item: item["effective_from"], reverse=True):
        start = parse_date(entry["effective_from"])
        end = parse_date(entry["effective_to"]) if entry.get("effective_to") else None
        if start <= event_date and (end is None or event_date <= end):
            return entry
    raise LookupErrorWithContext(
        "RateNotFoundError",
        f"No verified record covers {iso_date(event_date)}.",
        {"event_date": iso_date(event_date)},
    )


def lookup_parameter(regime: str, parameter: str, event_date: date) -> Dict[str, Any]:
    definition = get_parameter_definition(regime, parameter)
    entry = match_effective_window(definition.get("values", []), event_date)
    return {
        "ok": True,
        "regime": regime,
        "parameter": parameter,
        "event_date": iso_date(event_date),
        "unit": definition.get("unit"),
        "jurisdiction": definition.get("jurisdiction"),
        "value": entry.get("value"),
        "status": entry.get("status"),
        "effective_from": entry.get("effective_from"),
        "effective_to": entry.get("effective_to"),
        "source": entry.get("source"),
    }


def list_forms(regime: str, event_date: date) -> List[Dict[str, Any]]:
    data = load_json(find_forms_file(regime))
    forms = []
    for entry in data.get("forms", []):
        start = parse_date(entry["effective_from"])
        end = parse_date(entry["effective_to"]) if entry.get("effective_to") else None
        if start <= event_date and (end is None or event_date <= end):
            forms.append(entry)
    return forms


def load_deadline_rules() -> List[Dict[str, Any]]:
    data = load_json(DATA_DIR / "deadlines" / "deadlines.json")
    return data.get("rules", [])


def find_deadline_rule(rule_id: str) -> Dict[str, Any]:
    for rule in load_deadline_rules():
        if rule["id"] == rule_id:
            return rule
    raise LookupErrorWithContext(
        "UnknownDeadlineRuleError",
        f"No deadline rule found for '{rule_id}'.",
        {"regime": rule_id},
    )


def parse_facts(raw: str) -> Dict[str, Any]:
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LookupErrorWithContext(
            "InvalidFactsError",
            "Facts must be valid JSON.",
            {"raw": raw, "detail": str(exc)},
        ) from exc
    if not isinstance(payload, dict):
        raise LookupErrorWithContext(
            "InvalidFactsError",
            "Facts payload must be a JSON object.",
            {"raw": raw},
        )
    return payload


def compute_deadline(rule_id: str, facts: Dict[str, Any]) -> Dict[str, Any]:
    rule = find_deadline_rule(rule_id)
    for fact in rule.get("required_facts", []):
        if fact not in facts:
            raise LookupErrorWithContext(
                "MissingFactError",
                f"Deadline rule '{rule_id}' requires fact '{fact}'.",
                {"regime": rule_id, "required_fact": fact},
            )

    logic = rule["rule"]
    kind = logic["kind"]
    if kind == "fixed_day_second_following_month":
        base = parse_date(facts[logic["base"]])
        due = fixed_day_second_following_month(base, logic["day"])
    elif kind == "months_and_days_after":
        base = parse_date(facts[logic["base"]])
        due = add_months(base, logic["months"]) + timedelta(days=logic["days"])
    elif kind == "days_after":
        base = parse_date(facts[logic["base"]])
        due = base + timedelta(days=logic["days"])
    elif kind == "fixed_annual_after_tax_year":
        tax_year_end = parse_date(facts["tax_year_end"])
        due = date(tax_year_end.year + 1, logic["month"], logic["day"])
    elif kind == "fixed_same_year":
        tax_year_end = parse_date(facts["tax_year_end"])
        due = date(tax_year_end.year, logic["month"], logic["day"])
    else:
        raise LookupErrorWithContext(
            "UnsupportedRuleError",
            f"Unsupported deadline rule kind '{kind}'.",
            {"regime": rule_id, "kind": kind},
        )

    return {
        "ok": True,
        "regime": rule_id,
        "deadline": iso_date(due),
        "description": rule["description"],
        "facts": facts,
        "source": rule["source"],
    }


def dump_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=False)
