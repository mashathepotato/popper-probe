#!/usr/bin/env python3
"""Smoke tests for scripts/validate_hypothesis.py.

Run with: python3 tests/test_validate_hypothesis.py
Exits 0 if all tests pass, 1 otherwise.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = ROOT / "scripts" / "validate_hypothesis.py"
INPUTS = ROOT / "tests" / "fixtures" / "_validator_inputs"


def run(target):
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(target)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def assert_eq(actual, expected, msg):
    if actual != expected:
        print(f"FAIL {msg}: expected {expected!r}, got {actual!r}")
        return False
    return True


def test_valid_passed_hypothesis_returns_zero():
    code, out, err = run(INPUTS / "valid_passed.md")
    ok = True
    ok &= assert_eq(code, 0, "valid_passed exit code")
    ok &= assert_eq("OK" in out, True, "valid_passed stdout contains OK")
    return ok


def test_valid_failed_gate_returns_zero():
    code, out, err = run(INPUTS / "valid_failed_gate.md")
    ok = True
    ok &= assert_eq(code, 0, "valid_failed_gate exit code")
    ok &= assert_eq("OK" in out, True, "valid_failed_gate stdout contains OK")
    return ok


def test_missing_sections_returns_one():
    code, out, err = run(INPUTS / "missing_sections.md")
    ok = True
    ok &= assert_eq(code, 1, "missing_sections exit code")
    ok &= assert_eq(
        "missing required sections" in err,
        True,
        "missing_sections stderr mentions missing sections",
    )
    return ok


def test_bad_status_returns_one():
    code, out, err = run(INPUTS / "bad_status.md")
    ok = True
    ok &= assert_eq(code, 1, "bad_status exit code")
    ok &= assert_eq(
        "status must be one of" in err,
        True,
        "bad_status stderr mentions status",
    )
    return ok


def test_bad_reference_returns_one():
    code, out, err = run(INPUTS / "bad_reference.md")
    ok = True
    ok &= assert_eq(code, 1, "bad_reference exit code")
    ok &= assert_eq(
        "reference not found" in err,
        True,
        "bad_reference stderr mentions reference not found",
    )
    return ok


TESTS = [
    test_valid_passed_hypothesis_returns_zero,
    test_valid_failed_gate_returns_zero,
    test_missing_sections_returns_one,
    test_bad_status_returns_one,
    test_bad_reference_returns_one,
]


def main():
    failures = 0
    for t in TESTS:
        if not t():
            failures += 1
        else:
            print(f"PASS {t.__name__}")
    if failures:
        print(f"\n{failures} test(s) failed")
        sys.exit(1)
    print(f"\nAll {len(TESTS)} test(s) passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
