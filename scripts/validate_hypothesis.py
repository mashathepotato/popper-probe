#!/usr/bin/env python3
"""Validate a hypothesis.md file against the popper-probe v1 schema.

Usage:
    python3 scripts/validate_hypothesis.py <path/to/hypothesis.md>

Exit codes:
    0 — valid
    1 — schema errors (printed to stderr)
    2 — usage error
"""
import sys
from pathlib import Path

REQUIRED_FRONTMATTER = {
    "slug", "created", "status", "falsifiability_gate", "literature_pass"
}
REQUIRED_SECTIONS_PASSED = {
    "Original framing",
    "Operational restatement",
    "Falsifier(s)",
    "Test design",
    "Auxiliary assumptions",
    "Distinctiveness",
    "References",
    "Intake log",
}
REQUIRED_SECTIONS_FAILED = {
    "Original framing",
    "Diagnostic",
    "References",
    "Intake log",
}
# Sections that must have at least one non-whitespace content line
NON_EMPTY_SECTIONS_PASSED = {
    "Operational restatement",
    "Falsifier(s)",
    "Test design",
    "Auxiliary assumptions",
    "Distinctiveness",
}
NON_EMPTY_SECTIONS_FAILED = {
    "Diagnostic",
    "Intake log",
}
VALID_STATUS = {"active", "unfalsifiable", "retired"}
VALID_GATE = {"passed", "failed"}
VALID_LIT_PASS = {"completed", "partial", "none"}


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing opening '---'"
    fm = {}
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    if end_idx is None:
        return None, "missing closing '---'"
    return fm, None


def section_headers(text):
    return {line[3:].strip() for line in text.splitlines() if line.startswith("## ")}


def section_bodies(text):
    """Return a dict mapping section header name -> list of content lines."""
    sections = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def validate(path):
    errors = []
    file = Path(path)
    if not file.exists():
        return [f"file not found: {path}"]
    text = file.read_text()

    fm, fm_err = parse_frontmatter(text)
    if fm_err:
        return [f"frontmatter: {fm_err}"]

    missing_fm = REQUIRED_FRONTMATTER - set(fm.keys())
    if missing_fm:
        errors.append(f"frontmatter missing keys: {sorted(missing_fm)}")

    if fm.get("status") not in VALID_STATUS:
        errors.append(
            f"status must be one of {sorted(VALID_STATUS)}, got {fm.get('status')!r}"
        )
    gate = fm.get("falsifiability_gate")
    if gate not in VALID_GATE:
        errors.append(
            f"falsifiability_gate must be one of {sorted(VALID_GATE)}, got {gate!r}"
        )
    if fm.get("literature_pass") not in VALID_LIT_PASS:
        errors.append(
            f"literature_pass must be one of {sorted(VALID_LIT_PASS)}, "
            f"got {fm.get('literature_pass')!r}"
        )

    headers = section_headers(text)
    expected = REQUIRED_SECTIONS_PASSED if gate == "passed" else REQUIRED_SECTIONS_FAILED
    missing_sec = expected - headers
    if missing_sec:
        errors.append(
            f"missing required sections (for gate={gate}): {sorted(missing_sec)}"
        )

    # Check that load-bearing sections have non-empty body content
    non_empty_required = (
        NON_EMPTY_SECTIONS_PASSED if gate == "passed" else NON_EMPTY_SECTIONS_FAILED
    )
    bodies = section_bodies(text)
    for sec in sorted(non_empty_required):
        if sec not in bodies:
            continue  # Already caught by missing_sec check above
        content_lines = [l for l in bodies[sec] if l.strip()]
        if not content_lines:
            errors.append(
                f"section '{sec}' is empty (non-empty body required for gate={gate})"
            )

    # Check references: path resolution and mandatory contribution field
    hyp_dir = file.parent
    in_refs = False
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## "):
            in_refs = (line.strip() == "## References")
            continue
        if in_refs and line.strip().startswith("- path:"):
            ref_path = line.split(":", 1)[1].strip()
            full = hyp_dir / ref_path
            if not full.exists():
                errors.append(f"reference not found: {ref_path}")
            # Check that contribution: appears before the next entry or section
            has_contribution = False
            for j in range(i + 1, len(lines)):
                next_line = lines[j]
                if next_line.strip().startswith("- path:") or next_line.startswith("## "):
                    break
                if next_line.strip().startswith("contribution:"):
                    has_contribution = True
                    break
            if not has_contribution:
                errors.append(
                    f"reference '{ref_path}' is missing mandatory 'contribution:' field"
                )

    return errors


def main():
    if len(sys.argv) != 2:
        print(
            "usage: validate_hypothesis.py <path/to/hypothesis.md>",
            file=sys.stderr,
        )
        sys.exit(2)
    errors = validate(sys.argv[1])
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
