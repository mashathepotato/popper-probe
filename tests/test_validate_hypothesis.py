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


TESTS = [
    test_valid_passed_hypothesis_returns_zero,
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
