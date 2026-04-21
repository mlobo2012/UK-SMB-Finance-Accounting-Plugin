from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_tool(script_name: str, args: list[str]) -> dict:
    proc = subprocess.run(
        [sys.executable, str(TOOLS / script_name), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    payload = json.loads(proc.stdout)
    payload["_returncode"] = proc.returncode
    return payload


def load_fixture(name: str) -> list[dict]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class RateLookupTests(unittest.TestCase):
    def test_rate_lookup_fixtures(self) -> None:
        for case in load_fixture("rate_lookup_cases.json"):
            with self.subTest(args=case["args"]):
                payload = run_tool("lookup_rate.py", case["args"])
                self.assertEqual(payload["ok"], case["expected"]["ok"])
                self.assertEqual(payload["_returncode"], 0)
                if isinstance(case["expected"]["value"], dict):
                    for key, value in case["expected"]["value"].items():
                        self.assertEqual(payload["value"][key], value)
                else:
                    self.assertEqual(payload["value"], case["expected"]["value"])
                if "status" in case["expected"]:
                    self.assertEqual(payload["status"], case["expected"]["status"])

    def test_missing_rate_refuses(self) -> None:
        payload = run_tool(
            "lookup_rate.py",
            ["--regime", "payroll", "--parameter", "lower_earnings_limit_year", "--event-date", "2025-03-01"],
        )
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["_returncode"], 2)
        self.assertEqual(payload["error"], "RateNotFoundError")


class DeadlineTests(unittest.TestCase):
    def test_deadline_fixtures(self) -> None:
        for case in load_fixture("deadline_cases.json"):
            with self.subTest(args=case["args"]):
                payload = run_tool("find_deadline.py", case["args"])
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["_returncode"], 0)
                self.assertEqual(payload["deadline"], case["expected"]["deadline"])


class FormTests(unittest.TestCase):
    def test_form_fixtures(self) -> None:
        for case in load_fixture("form_cases.json"):
            with self.subTest(args=case["args"]):
                payload = run_tool("list_forms.py", case["args"])
                self.assertTrue(payload["ok"])
                codes = {form["code"] for form in payload["forms"]}
                for expected_code in case["expected_contains"]:
                    self.assertIn(expected_code, codes)


class ComputeTests(unittest.TestCase):
    def test_compute_fixtures(self) -> None:
        for case in load_fixture("compute_cases.json"):
            with self.subTest(args=case["args"]):
                payload = run_tool("compute_tax.py", case["args"])
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["_returncode"], 0)
                for key, value in case["expected"]["result"].items():
                    self.assertEqual(payload["result"][key], value)


if __name__ == "__main__":
    unittest.main()
