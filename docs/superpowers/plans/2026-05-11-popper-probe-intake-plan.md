# popper-probe Intake (v1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v1 of the popper-probe Intake skill — a Claude Code skill that runs an adversarial-but-constructive Popperian dialogue to convert a fuzzy research claim into a falsifiable hypothesis file in a local markdown corpus.

**Architecture:** A single Claude Code skill (`skills/intake/SKILL.md`) drives the conversation; a Python schema validator (`scripts/validate_hypothesis.py`) checks the output file structure; a fixture set (`tests/fixtures/`) plus a human rubric (`tests/rubric.md`) is the eval harness. The skill is packaged as a Claude Code plugin (existing `.claude-plugin/` directory is repurposed).

**Tech Stack:** Markdown (skill body, hypothesis files, fixtures, rubric); Python 3 stdlib only (validator + its self-test); Claude Code plugin/skill format; shell.

**Source of truth for behavior:** `docs/superpowers/specs/2026-05-11-popper-probe-intake-design.md`. Read it before starting Tasks 9–12 — the SKILL.md is a faithful expression of that spec.

---

### Task 1: Remove old direction artifacts

The repo previously housed a Socratic design-phase plugin (`commands/probe.md`). The new direction is a skill, not a slash command. Old artifacts come out cleanly before anything new lands.

**Files:**
- Delete: `commands/probe.md`
- Delete: `commands/` (after `probe.md` is gone, if empty)

- [ ] **Step 1: Verify what's in `commands/`**

Run: `ls /Users/masha/Documents/popper-probe/commands/`
Expected: a single file `probe.md`. If there are more files, stop and check with the user before deleting.

- [ ] **Step 2: Delete `commands/probe.md`**

Run: `rm /Users/masha/Documents/popper-probe/commands/probe.md`
Expected: silent success.

- [ ] **Step 3: Remove the now-empty `commands/` directory**

Run: `rmdir /Users/masha/Documents/popper-probe/commands`
Expected: silent success. If `rmdir` fails (not empty), investigate before deleting forcefully.

- [ ] **Step 4: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add -A commands
git commit -m "Remove commands/probe.md from earlier direction"
```

---

### Task 2: Update plugin manifest to reflect new direction

The existing `plugin.json` and `marketplace.json` describe the old Socratic-design plugin. Both need updating so install/discovery descriptions match the new intent.

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Replace `.claude-plugin/plugin.json` with the new manifest**

Write file content exactly:

```json
{
  "name": "popper-probe",
  "version": "0.1.0",
  "description": "A Popperian research companion: adversarially interrogate empirical claims, log them as falsifiable hypotheses, and keep a markdown ledger of evidence over time. v1 ships the intake skill.",
  "author": {
    "name": "masha"
  },
  "keywords": ["research", "hypothesis", "falsifiability", "popper", "science"],
  "license": "MIT"
}
```

- [ ] **Step 2: Replace `.claude-plugin/marketplace.json` with the new catalog**

Write file content exactly:

```json
{
  "name": "popper",
  "owner": {
    "name": "masha"
  },
  "description": "Marketplace for popper-probe and related Claude Code research-companion plugins.",
  "plugins": [
    {
      "name": "popper-probe",
      "source": "./",
      "description": "A Popperian research companion: adversarially interrogate empirical claims, log them as falsifiable hypotheses, and keep a markdown ledger of evidence over time. v1 ships the intake skill.",
      "version": "0.1.0",
      "license": "MIT",
      "keywords": ["research", "hypothesis", "falsifiability", "popper", "science"],
      "category": "research"
    }
  ]
}
```

- [ ] **Step 3: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "Update plugin manifest for popper-probe v1 direction"
```

---

### Task 3: Scaffold project directories

Create the directories the rest of the plan writes into. Empty `.gitkeep` files keep them tracked until real content lands.

**Files:**
- Create: `skills/intake/.gitkeep`
- Create: `scripts/.gitkeep`
- Create: `tests/fixtures/.gitkeep`

- [ ] **Step 1: Create the directories with placeholder files**

Run:
```bash
mkdir -p /Users/masha/Documents/popper-probe/skills/intake
mkdir -p /Users/masha/Documents/popper-probe/scripts
mkdir -p /Users/masha/Documents/popper-probe/tests/fixtures
touch /Users/masha/Documents/popper-probe/skills/intake/.gitkeep
touch /Users/masha/Documents/popper-probe/scripts/.gitkeep
touch /Users/masha/Documents/popper-probe/tests/fixtures/.gitkeep
```

- [ ] **Step 2: Verify structure**

Run: `find /Users/masha/Documents/popper-probe/skills /Users/masha/Documents/popper-probe/scripts /Users/masha/Documents/popper-probe/tests -type f`
Expected: three `.gitkeep` files, one per directory.

- [ ] **Step 3: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add skills scripts tests
git commit -m "Scaffold skills, scripts, and tests directories"
```

---

### Task 4: Write failing test for hypothesis validator

The validator is the only piece of v1 with real logic — drive it with TDD. First test: a known-good fixture file should validate cleanly.

**Files:**
- Create: `tests/test_validate_hypothesis.py`
- Create: `tests/fixtures/_validator_inputs/valid_passed.md` (a hand-crafted minimal valid hypothesis file used only by validator tests, not by the eval fixtures)

- [ ] **Step 1: Create the inputs directory**

Run: `mkdir -p /Users/masha/Documents/popper-probe/tests/fixtures/_validator_inputs`

- [ ] **Step 2: Create the known-good fixture file**

Write `tests/fixtures/_validator_inputs/valid_passed.md` with this exact content:

```markdown
---
slug: example-claim
created: 2026-05-11
status: active
falsifiability_gate: passed
literature_pass: none
---

# Example claim

## Original framing
> The original fuzzy version.

## Operational restatement
The third-party-measurable version.

## Falsifier(s)
- One concrete observation that would refute it.

## Test design
- Methods and design notes.

## Auxiliary assumptions
- One assumption that has to be true.

## Distinctiveness
What this claim predicts that competing accounts don't.

## References

## Intake log
2026-05-11 — Created for validator tests.
```

- [ ] **Step 3: Write the failing test file**

Write `tests/test_validate_hypothesis.py` with this exact content:

```python
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
```

- [ ] **Step 4: Run the test — expect it to fail because the validator doesn't exist yet**

Run: `python3 /Users/masha/Documents/popper-probe/tests/test_validate_hypothesis.py`
Expected: exit code 1; output contains `FAIL test_valid_passed_hypothesis_returns_zero`. The failure mode is that the validator script does not exist, so the subprocess returns a non-zero exit code (likely 2 from the system) and no "OK" in stdout.

- [ ] **Step 5: Remove the `_validator_inputs` `.gitkeep` if present, commit the test infrastructure**

```bash
cd /Users/masha/Documents/popper-probe
rm -f tests/fixtures/.gitkeep
git add tests/test_validate_hypothesis.py tests/fixtures/_validator_inputs
git commit -m "Add failing test for hypothesis validator"
```

(The `.gitkeep` in `tests/fixtures/` is no longer needed because the directory has real content now.)

---

### Task 5: Implement the validator

Make the failing test pass. Write the validator with just enough to satisfy the test, no more.

**Files:**
- Create: `scripts/validate_hypothesis.py`

- [ ] **Step 1: Write the validator**

Write `scripts/validate_hypothesis.py` with this exact content:

```python
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

    hyp_dir = file.parent
    in_refs = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_refs = (line.strip() == "## References")
            continue
        if in_refs and line.strip().startswith("- path:"):
            ref_path = line.split(":", 1)[1].strip()
            full = hyp_dir / ref_path
            if not full.exists():
                errors.append(f"reference not found: {ref_path}")

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
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x /Users/masha/Documents/popper-probe/scripts/validate_hypothesis.py`

- [ ] **Step 3: Run the test — expect it to pass now**

Run: `python3 /Users/masha/Documents/popper-probe/tests/test_validate_hypothesis.py`
Expected: exit code 0; output `PASS test_valid_passed_hypothesis_returns_zero` and `All 1 test(s) passed`.

- [ ] **Step 4: Commit**

```bash
cd /Users/masha/Documents/popper-probe
rm -f scripts/.gitkeep
git add scripts/validate_hypothesis.py
git commit -m "Implement hypothesis validator (passing first test)"
```

---

### Task 6: Add validator test cases for failure modes

Now drive out the remaining validator behavior with more failing tests, each covered by the existing implementation.

**Files:**
- Modify: `tests/test_validate_hypothesis.py`
- Create: `tests/fixtures/_validator_inputs/valid_failed_gate.md`
- Create: `tests/fixtures/_validator_inputs/missing_sections.md`
- Create: `tests/fixtures/_validator_inputs/bad_status.md`
- Create: `tests/fixtures/_validator_inputs/bad_reference.md`

- [ ] **Step 1: Create a known-good "unfalsifiable" fixture**

Write `tests/fixtures/_validator_inputs/valid_failed_gate.md`:

```markdown
---
slug: example-unfalsifiable
created: 2026-05-11
status: unfalsifiable
falsifiability_gate: failed
literature_pass: none
---

# Example unfalsifiable claim

## Original framing
> Vague claim text.

## Diagnostic
Why this claim is unfalsifiable as stated, and what reformulation might rescue it.

## References

## Intake log
2026-05-11 — Created for validator tests.
```

- [ ] **Step 2: Create a fixture missing required sections**

Write `tests/fixtures/_validator_inputs/missing_sections.md`:

```markdown
---
slug: missing-sections
created: 2026-05-11
status: active
falsifiability_gate: passed
literature_pass: none
---

# Example with missing sections

## Original framing
> Whatever.
```

- [ ] **Step 3: Create a fixture with invalid status**

Write `tests/fixtures/_validator_inputs/bad_status.md`:

```markdown
---
slug: bad-status
created: 2026-05-11
status: pending
falsifiability_gate: passed
literature_pass: none
---

# Example with bad status

## Original framing
> Whatever.

## Operational restatement
x.

## Falsifier(s)
- x.

## Test design
- x.

## Auxiliary assumptions
- x.

## Distinctiveness
x.

## References

## Intake log
x.
```

- [ ] **Step 4: Create a fixture with a broken reference**

Write `tests/fixtures/_validator_inputs/bad_reference.md`:

```markdown
---
slug: bad-reference
created: 2026-05-11
status: active
falsifiability_gate: passed
literature_pass: completed
---

# Example with bad reference

## Original framing
> Whatever.

## Operational restatement
x.

## Falsifier(s)
- x.

## Test design
- x.

## Auxiliary assumptions
- x.

## Distinctiveness
x.

## References
- path: refs/does-not-exist.pdf
  contribution: should fail validation

## Intake log
x.
```

- [ ] **Step 5: Extend `tests/test_validate_hypothesis.py` with the new test cases**

Replace the `TESTS = [...]` list and add the test functions above it. The full file becomes:

```python
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
```

- [ ] **Step 6: Run the tests — all five should pass**

Run: `python3 /Users/masha/Documents/popper-probe/tests/test_validate_hypothesis.py`
Expected: all five tests print `PASS`; exit code 0.

If any test fails, the validator from Task 5 needs adjustment — do not modify the test to fit a buggy validator. Fix the validator, re-run.

- [ ] **Step 7: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add tests
git commit -m "Add validator test cases for failure modes"
```

---

### Task 7: Create eval fixtures

Eval fixtures live separately from the validator inputs. They represent the *user-facing* test scenarios from the spec (section 5.2). Each fixture has an `input.md` describing the starting context a user would provide to the intake skill, plus optional `refs/` for fixtures that exercise the literature pass.

**Files:**
- Create: `tests/fixtures/vague-claim/input.md`
- Create: `tests/fixtures/already-operational/input.md`
- Create: `tests/fixtures/with-refutation/input.md`
- Create: `tests/fixtures/with-refutation/refs/synthetic-null-result.md`
- Create: `tests/fixtures/hedged-claim/input.md`
- Create: `tests/fixtures/bold-distinct/input.md`
- Create: `tests/fixtures/unfalsifiable/input.md`
- Create: `tests/fixtures/new-to-field/input.md`

- [ ] **Step 1: Create `vague-claim`**

Write `tests/fixtures/vague-claim/input.md`:

```markdown
# Input — vague-claim fixture

**User starting claim:**

> AI will make programmers obsolete.

**No papers supplied.**

**Expected skill behavior:**

- Probe 1 forces operational restatement. The user is likely unable to phrase this in falsifiable form.
- Probe 2 asks for a falsifier; the user can't name one that isn't trivially evadable.
- Skill writes a `falsifiability_gate: failed`, `status: unfalsifiable` hypothesis file with a diagnostic.
```

- [ ] **Step 2: Create `already-operational`**

Write `tests/fixtures/already-operational/input.md`:

```markdown
# Input — already-operational fixture

**User starting claim:**

> In adult human subjects (N≥30 per arm), 30 minutes of moderate-intensity cycling on stationary bikes performed 2 hours before a recall test will increase the number of correctly recalled words from a 50-word list by at least 10% compared to a seated rest control.

**No papers supplied.**

**Expected skill behavior:**

- Probe 1 is brief — the claim is already operational. Skill confirms and moves on, does not force redundant restatement.
- Probe 2 elicits a clear falsifier (no measurable gain at the stated threshold).
- Probe 3 runs the test-design discussion; no literature pass needed (no papers).
- Probe 4 records distinctiveness.
- Hypothesis file written with `falsifiability_gate: passed`.
```

- [ ] **Step 3: Create `with-refutation` (input + a synthetic refutation paper)**

Write `tests/fixtures/with-refutation/input.md`:

```markdown
# Input — with-refutation fixture

**User starting claim:**

> Listening to Mozart immediately before a spatial reasoning task improves performance compared to silence ("the Mozart effect").

**Paper supplied:** `refs/synthetic-null-result.md`

**Expected skill behavior:**

- Probe 3's literature pass reads the supplied paper, surfaces the null result, and prompts the user with a citation-anchored question (e.g., "Smith et al. found no effect at N=120 — does this change your falsifier?").
- The resulting hypothesis file's `## References` section includes the supplied paper with a `contribution:` line that mentions prior null result.
- The user may decide to abandon, narrow, or proceed; any outcome is acceptable as long as the literature pass surfaced the refutation.

**Anti-hallucination ground truth:** the paper at `refs/synthetic-null-result.md` reports N=120 and a null result; the abstract specifically uses the phrase "no statistically significant difference."
```

Write `tests/fixtures/with-refutation/refs/synthetic-null-result.md`:

```markdown
# A pre-registered replication of the Mozart effect: no support for short-term spatial cognition gains

**Authors:** Synthetic, A.; Test, B.

## Abstract
We conducted a pre-registered replication of the proposed "Mozart effect" with
N=120 adult participants (60 per arm) using a within-subjects design. Participants
completed a paper-folding spatial reasoning task after either ten minutes of Mozart's
Sonata for Two Pianos in D Major (K. 448) or ten minutes of silence. Across the
full sample, we observed **no statistically significant difference** in task
performance between the music and silence conditions (mean difference 0.4 items
correct, 95% CI [-0.9, 1.7], p = 0.55). Bayes factor analysis (BF01 = 7.3)
indicates moderate evidence for the null.

## Method
Participants were recruited from an undergraduate subject pool. Each completed
both conditions in counterbalanced order separated by a 24-hour washout. The
spatial reasoning measure was the 20-item paper-folding subscale of the
Educational Testing Service Kit.

## Results
Group means were near-identical (music M = 12.3, SD = 3.1; silence M = 11.9,
SD = 3.4). Pre-registered analyses showed no significant effect of condition.

## Discussion
Our results add to a growing literature failing to replicate the original
Mozart-effect findings. We suggest the original results may reflect arousal
differences from the unfamiliar listening environment rather than a music-specific
cognitive effect.
```

- [ ] **Step 4: Create `hedged-claim`**

Write `tests/fixtures/hedged-claim/input.md`:

```markdown
# Input — hedged-claim fixture

**User starting claim:**

> Mindfulness meditation may, under certain conditions, in some individuals, somewhat reduce symptoms of anxiety, though effects can vary substantially.

**No papers supplied.**

**Expected skill behavior:**

- Probe 1 calls out the hedges ("may," "under certain conditions," "in some individuals," "somewhat," "can vary") and refuses to advance until the user commits to specific quantities (which population, which symptoms, what magnitude, measured how).
- If the user resists committing, the skill explicitly names the problem: a hedged-enough claim cannot be falsified because every outcome is consistent with it.
- Outcome depends on whether the user commits or doubles down on hedges. Both branches are acceptable as long as the skill surfaced the issue.
```

- [ ] **Step 5: Create `bold-distinct`**

Write `tests/fixtures/bold-distinct/input.md`:

```markdown
# Input — bold-distinct fixture

**User starting claim:**

> A high-fat ketogenic diet (≥70% calories from fat, ≤10% from carbohydrate) sustained for 12 weeks will reduce HbA1c in type-2 diabetic patients by at least 0.5 percentage points more than an isocaloric standard low-fat diet (Mediterranean profile), measured by the same lab using the same assay.

**No papers supplied.**

**Expected skill behavior:**

- All four probes pass cleanly. Probe 4 (distinctiveness) is notably strong: the claim *forbids* outcomes that competing accounts (calorie-restriction-is-all-that-matters, low-carb-but-not-keto-specific) predict.
- Hypothesis file marked `falsifiability_gate: passed`. Distinctiveness section captures the specific forbids.
```

- [ ] **Step 6: Create `unfalsifiable`**

Write `tests/fixtures/unfalsifiable/input.md`:

```markdown
# Input — unfalsifiable fixture

**User starting claim:**

> Consciousness emerges from sufficiently complex information processing.

**No papers supplied.**

**Expected skill behavior:**

- Probe 1 forces operational restatement: how is "consciousness" measured, how is "sufficient complexity" measured? The user likely cannot answer in falsifier-friendly terms.
- Probe 2 confirms no falsifier is namable.
- Skill writes `falsifiability_gate: failed`, `status: unfalsifiable`, with a `## Diagnostic` section explaining why and offering reformulation suggestions (e.g., restrict to behaviorally measurable proxies, name a specific complexity threshold).
```

- [ ] **Step 7: Create `new-to-field`**

Write `tests/fixtures/new-to-field/input.md`:

```markdown
# Input — new-to-field fixture

**User starting claim:**

> I want to study how gut microbiome composition affects mood, but I'm not familiar with this area. What's known?

**No papers supplied.**

**Expected skill behavior:**

- Skill detects uncertainty signals (explicit "I'm not familiar," open question rather than a claim).
- Probe 0 (SoTA orientation) triggers. Skill offers, in one message, the orientation option.
- On user acceptance, skill delivers:
  1. Foundations from training knowledge, with explicit knowledge-cutoff caveat.
  2. Notes that no papers were supplied.
  3. Offers opt-in web search ("I can do a targeted search. I'll show you 3–5 candidates before I cite anything.").
- Only after orientation does the skill proceed to Probe 1 with: "Given that, how would you phrase the claim you want to test?"
- No paper is cited unless the user explicitly chose to pull it.
```

- [ ] **Step 8: Verify all eval fixtures exist**

Run: `find /Users/masha/Documents/popper-probe/tests/fixtures -name input.md -type f | sort`
Expected: seven `input.md` files (one per fixture directory), plus one `synthetic-null-result.md` under `with-refutation/refs/`.

- [ ] **Step 9: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add tests/fixtures
git commit -m "Add seven eval fixtures covering intake scenarios"
```

---

### Task 8: Write the human rubric

The rubric is what a human (or future agent) checks after running the skill against a fixture. It captures the behavioral expectations the validator cannot.

**Files:**
- Create: `tests/rubric.md`
- Create: `tests/README.md` (documents how to run an eval)

- [ ] **Step 1: Write the rubric**

Write `tests/rubric.md`:

```markdown
# popper-probe Intake — Manual Eval Rubric

Run after each fixture eval. Mark each item Pass / Fail / N/A.

## Probe coverage

- [ ] **Probe 0 — SoTA orientation.** Triggered only when uncertainty signals
      were present (user said "new to field," asked open question, etc.). Did
      not trigger gratuitously when the user already had a clear claim.
- [ ] **Probe 0 — opt-in web search.** If web search was offered, the skill
      showed candidate references and asked the user to pick before citing.
      No paper was cited without the user's explicit pick.
- [ ] **Probe 1 — operational restatement.** Skill forced or confirmed an
      operationally measurable form of the claim.
- [ ] **Probe 2 — named falsifier.** Skill asked what observation would refute
      the claim. If the user could not name one, the skill flagged the claim
      as unfalsifiable rather than smoothing it over.
- [ ] **Probe 3 — test design (the "how").** Skill walked through methods,
      study design, and auxiliary assumptions constructively. Did not skip
      this probe.
- [ ] **Probe 3 — literature pass.** If papers were supplied, skill triaged
      (abstract/intro/conclusion first), reported what it read and skipped,
      and surfaced findings one at a time with citation-anchored questions.
- [ ] **Probe 4 — distinctiveness.** Skill asked what the hypothesis predicts
      that competing accounts do not. Recorded answer in file (may be flagged
      as low-information but not gated).

## Tone

- [ ] **Constructive, not hostile.** Sparring partner, not judge.
- [ ] **No lecturing.** Each finding was tied to a question for the user, not
      a monologue.

## Output file

- [ ] **Schema validator passes.** Run
      `python3 scripts/validate_hypothesis.py <path/to/hypothesis.md>` and confirm
      `OK`.
- [ ] **Termination at the gate, not arbitrarily.** File was written only when
      probes 1–3 produced their required content (or the unfalsifiable diagnostic
      was triggered).

## Anti-hallucination

- [ ] **No citations to papers the skill did not open.** Cross-check any
      `## References` entries against papers the skill explicitly said it read.
- [ ] **Citation content matches paper content.** For fixtures with ground-truth
      paper claims (see fixture's `input.md`), verify citations match the actual
      content of the paper.

## Comments

(Free text: anything notable, surprising, or worth changing in the SKILL.md.)
```

- [ ] **Step 2: Write the eval procedure README**

Write `tests/README.md`:

```markdown
# popper-probe — Eval Procedure

## Run the validator self-tests

```bash
python3 tests/test_validate_hypothesis.py
```

Expected: `All N test(s) passed`.

## Run an eval against a single fixture

1. Pick a fixture under `tests/fixtures/<name>/`.
2. Read its `input.md` — that is the user's starting context. (For
   `with-refutation`, also note the `refs/` directory; the skill should
   pick these up.)
3. Start a fresh Claude Code session in the repo. Invoke the intake skill
   with the fixture's user claim — verbatim.
4. Conduct the conversation as the user would: answer the skill's probes
   honestly given the fixture's framing. (For the `vague-claim`,
   `hedged-claim`, and `unfalsifiable` fixtures, do not artificially supply
   answers the user would not have; the point is to see whether the skill
   handles the difficulty.)
5. When the skill writes a `hypothesis.md`, run the validator:
   ```bash
   python3 scripts/validate_hypothesis.py popper-corpus/<slug>/hypothesis.md
   ```
6. Open a fresh copy of `tests/rubric.md` and tick each item.
7. Save the completed rubric alongside the produced hypothesis (e.g.,
   `popper-corpus/<slug>/rubric.md`) and any notes.

## Aggregate

After running multiple fixtures, summarize: which rubric items fail most
often? That points to specific SKILL.md changes.
```

- [ ] **Step 3: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add tests/rubric.md tests/README.md
git commit -m "Add manual eval rubric and procedure"
```

---

### Task 9: Write SKILL.md — frontmatter, scope, invocation

The SKILL.md is the heart of v1. Build it in four passes (Tasks 9–12) so each commit is reviewable. Read `docs/superpowers/specs/2026-05-11-popper-probe-intake-design.md` before this task — section 2 is the source of truth for what the skill must do.

**Files:**
- Modify (replace): `skills/intake/SKILL.md` (currently empty placeholder)

- [ ] **Step 1: Remove the `.gitkeep` from `skills/intake/`**

Run: `rm -f /Users/masha/Documents/popper-probe/skills/intake/.gitkeep`

- [ ] **Step 2: Write the SKILL.md frontmatter and opening sections**

Write `skills/intake/SKILL.md`:

```markdown
---
name: intake
description: Use when a researcher describes a research hypothesis, fuzzy claim, or empirical conjecture they want to test — runs an adversarial-but-constructive Popperian dialogue and writes a falsifiable-hypothesis file to a local markdown corpus. Triggers on phrases like "I think X causes Y", "my hypothesis is", "I want to test whether", or any hypothesis-shaped claim about the world.
---

# popper-probe Intake

Convert a fuzzy research claim into a sharp, falsifiable hypothesis through one optional preamble (SoTA orientation) and four probes (operational restatement, named falsifier, test design, distinctiveness). At the end, write a `hypothesis.md` file to the local markdown corpus.

**Source of truth for behavior:** `docs/superpowers/specs/2026-05-11-popper-probe-intake-design.md`. Read it if anything below seems ambiguous.

## Invocation

This skill is invoked in two ways:

- **Explicit:** the user calls `/popper-probe:intake` (or its plugin-qualified equivalent).
- **Implicit:** the user describes something hypothesis-shaped — a claim about the world they expect to be testable — without explicitly invoking the skill. Follow the `using-superpowers` convention: if there's any reasonable chance this skill applies, invoke it.

If the user supplied papers or a `refs/` folder path in their first message, pick them up automatically — they belong in Probe 0 (orientation) or Probe 3 (literature pass).

## Scope (v1)

This skill does **intake only**:

- Convert a fuzzy claim into a well-formed hypothesis file in the local corpus.
- Optionally orient the user to the field's state of the art before sharpening.

It does **not**:

- Log observations against existing hypotheses (future Phase C).
- Audit the corpus for stale/contradicted claims (future Phase D).
- Compare or link hypotheses to each other.
- Search the web *except* in Probe 0's opt-in SoTA fallback. Probe 3's literature pass uses only user-supplied papers, never the web.

## Tone

Sparring partner, not judge. The skill says *"can you sharpen this?"* not *"this is bad."* Probes 1–2 are sharpening. Probe 3 is collaborative design. Probe 4 is curiosity. Adversarial but not hostile.

## Output

The skill terminates by writing a single file:

- `popper-corpus/<slug>/hypothesis.md` in the user's working directory.
- Plus, optionally, papers under `popper-corpus/<slug>/refs/` (only if the user explicitly placed them there or asked the skill to copy them).

Schema is enforced by `scripts/validate_hypothesis.py` (run it on the output to confirm).
```

- [ ] **Step 3: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add skills/intake/SKILL.md
git commit -m "Begin intake SKILL.md: frontmatter, scope, invocation, tone"
```

---

### Task 10: Write SKILL.md — Probe 0 (SoTA orientation)

**Files:**
- Modify: `skills/intake/SKILL.md` (append Probe 0 section)

- [ ] **Step 1: Append the Probe 0 section to `skills/intake/SKILL.md`**

Add this content to the end of the file:

```markdown

## Conversation shape

The skill runs an optional preamble (Probe 0) followed by four core probes. Probes are not boxes to tick — they are stages of a dialogue. Stay in each stage until its outcome is genuine, not performed.

### Probe 0 — SoTA orientation (optional preamble)

**Trigger this probe when ANY of the following are true:**

- The user says they are new to the field, unfamiliar with the area, or "not up to date."
- The user asks open questions instead of stating a claim — e.g., *"I want to study X — what's known?"* or *"how do people usually think about Y?"*
- Probe 1 stalls because the user cannot restate the initial claim operationally even after a sharpening attempt, suggesting they lack field context.
- The user explicitly asks for SoTA, background, or orientation.

**If none of these apply, skip Probe 0 entirely and go to Probe 1.** Do not gratuitously offer orientation to a user who has a clear claim.

**Offer (exact phrasing — adapt the field-specific word as needed):**

> *"Want me to walk through what's established and what's actively being debated in this area before we sharpen your claim? I'll combine foundations I know with any papers you have. Optional."*

This offer is a single message, no other content. Wait for the user's response.

**If the user declines, proceed to Probe 1.**

**If the user accepts, deliver the orientation in three pieces, in order:**

#### Piece 1: Foundations from training knowledge

A short briefing on the established framing of the area:

- What's the consensus position?
- What's the standard ontology of variables (what dimensions does the field typically vary)?
- What classical experiments or findings anchor the field?

Hedge explicitly: *"My knowledge cuts off in <date>; anything since then I won't reliably know. For recent work, see piece 2 or 3 below."* If you do not know the field well, say so directly rather than fabricating consensus.

#### Piece 2: Recent activity — user-supplied papers first

If the user has supplied papers (in their first message, or in a `refs/` folder they pointed at), read them now under the same triage rules as Probe 3:

- First pass: abstract → intro → conclusion (cheap).
- Targeted pass: the section relevant to orientation (typically intro and discussion).
- Be honest about what you read and what you skipped.

Surface relevant findings one at a time, citation-anchored. Do not lecture.

#### Piece 3: Web search fallback — opt-in only

If the user has no recent papers and wants the latest, offer:

> *"I can do a targeted search for recent work. I'll show you 3–5 candidate references — title, authors, year, one-line relevance — and you pick which ones to pull fully before I cite anything."*

Wait for explicit user confirmation. **Never cite a paper you have not pulled.** If the user confirms, run a targeted WebFetch/WebSearch on search terms you surface (state the terms before searching). Present results. The user picks. Only then read the picked papers fully and only then cite them.

If the user declines all three pieces or has exhausted orientation, transition to Probe 1:

> *"Given that, how would you phrase the claim you want to test?"*

**No SoTA-briefing artifact is written in v1.** Anything from orientation that meaningfully shapes the eventual hypothesis lands in that hypothesis's `## References` and `## Intake log` sections — not a separate file.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add skills/intake/SKILL.md
git commit -m "Add Probe 0 (SoTA orientation) to intake skill"
```

---

### Task 11: Write SKILL.md — Probes 1–4

**Files:**
- Modify: `skills/intake/SKILL.md` (append Probes 1–4 section)

- [ ] **Step 1: Append the four core probes**

Add this content to the end of `skills/intake/SKILL.md`:

```markdown

### Probe 1 — Restate operationally

Force the claim into a form a third party could measure.

Example transformation:

> *"Plants grow better with music."* → *"Pea plants (variety X) exposed to 60–80 dB classical music for 12 hr/day will gain at least Y% more dry biomass than silent controls over Z days, under controlled light/temp/humidity."*

Ask one question at a time. Iterate until the restated form is unambiguous: every noun resolves to something measurable, every comparison has a referent, every quantity has units or at least a magnitude.

If the user resists committing to specifics ("it depends," "in some cases"), name the problem directly: *"A claim that doesn't commit to a magnitude can't be falsified by any measurement, because every result is consistent with it. Can you commit to a number or a direction?"*

**If the user cannot operationalize the claim even with sharpening attempts, do not proceed to Probe 2 as if you had a working hypothesis.** Move directly to the unfalsifiable termination path (see "Termination" below).

### Probe 2 — Name the falsifier

Ask: *"What observation would make you abandon this claim?"*

A good answer is concrete and specific: *"If the biomass gain in the music group is within measurement error of silent controls at Z days, the claim fails."*

A bad answer is evasive: *"Well, it depends on what we mean by 'better,'" "I'd want to consider why,"* or *"I'd refine the hypothesis."* These are red flags for ad-hoc rescue thinking. Surface them.

If the user cannot name any falsifier, even after prompting, the claim is unfalsifiable as stated. Offer the user a choice:

> *"I can either (a) help you reformulate the claim into something with a falsifier, or (b) record this as a `status: unfalsifiable` file with a diagnostic about what makes it unfalsifiable. Which?"*

Then act accordingly.

### Probe 3 — Design the test (the "how")

This probe is constructive, not adversarial. Walk the user through:

**Methods and instruments.** How will the variables in the operational restatement actually be measured? What instruments, protocols, scales? Push for specifics. If the user names a standard method, that's a citation opportunity (note for the References section).

**Study design.** Controls (positive, negative, placebo, sham?); randomization; blinding; sample size intuition (not a power calculation — just enough to gut-check feasibility); what a "clean run" looks like.

**Auxiliary assumptions.** What else has to be true for the test to be meaningful?

- *"The instrument is accurate at the relevant precision."*
- *"There's no confound X."*
- *"The sample is drawn from the population we mean to generalize about."*

Auxiliaries are not embarrassing — they are honest. Log every one named. These are the rescue surface for future ad-hoc patches; an explicit list now is a defense against later rationalization.

**Literature pass — runs here if the user supplied papers** (otherwise skip cleanly).

For each user-supplied paper:

1. First pass: abstract, intro, conclusion. State what you read and what you skipped.
2. Look for four lenses:
   - **Prior tests:** has this hypothesis (or near-equivalent) been tested?
   - **Standard methods:** what designs does the field use, and what are their known weaknesses?
   - **Reported refutations:** papers reporting the hypothesis failing — flag as critical.
   - **Common hedges / rescues:** recurring phrases the field uses when results disappoint.
3. Surface findings one at a time, with citation:

   > *"Chen 2021 (p. 7) ran a comparable design with N=40 and found no effect. They attributed it to dB level rather than musical content. Does that change how you'd specify the music exposure?"*

Never cite a section you did not read. If you skipped the results section but the user wants results, ask permission to do a deeper pass.

### Probe 4 — Distinctiveness (light, optional)

One question: *"What does this hypothesis predict that competing accounts don't?"*

A strong answer names a competing account and a prediction the user's claim makes that the competitor doesn't (or vice versa). Record it.

A weak answer is *"nothing in particular"* or *"I'm not sure."* That's fine — record it as a flag in the file (`distinctiveness: low-information`), not a block. The user may still want to test the claim; they just know it's not a sharp wedge against alternatives.

Probe 4 is recorded but does **not** gate writing the hypothesis file.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add skills/intake/SKILL.md
git commit -m "Add Probes 1-4 (operational, falsifier, test design, distinctiveness)"
```

---

### Task 12: Write SKILL.md — termination, file-writing protocol, schema

**Files:**
- Modify: `skills/intake/SKILL.md` (append termination + file-writing sections)

- [ ] **Step 1: Append the termination, file-writing, and schema sections**

Add this content to the end of `skills/intake/SKILL.md`:

```markdown

## Termination

There are exactly two termination outcomes:

### Falsifiability gate passed

When probes 1–3 have produced:

- An unambiguous operational restatement.
- At least one explicit, concrete falsifier.
- A test design sketch (methods, design notes, ≥1 auxiliary assumption).

Probe 4 is also recorded, but its outcome (`low-information` or substantive) does not gate.

Write the hypothesis file with `falsifiability_gate: passed`, `status: active`.

### Falsifiability gate failed

When Probe 1 or Probe 2 cannot be satisfied even after the user has had a real chance to sharpen the claim, and the user has chosen the "record as unfalsifiable" branch over the "reformulate" branch.

Write the hypothesis file with `falsifiability_gate: failed`, `status: unfalsifiable`, and a `## Diagnostic` section explaining what specifically was unfalsifiable and what reformulation might rescue it.

**Do not terminate arbitrarily.** If the conversation feels stuck mid-probe, surface that directly to the user ("we've circled this twice — should we set it aside, narrow it, or record it as unfalsifiable?") rather than silently writing a half-formed file.

## File-writing protocol

When termination conditions are met:

1. **Generate a slug** from a short summary of the operational restatement. Lowercase, hyphen-separated, no special characters. Example: *"Pea plants exposed to 60–80 dB classical music gain more biomass than silent controls"* → `pea-plants-music-biomass`.

2. **Check for collision.** Look at `popper-corpus/<slug>/`. If a hypothesis with the same slug already exists, append `-2`, `-3`, etc. **Never overwrite.**

3. **Draft the file content** following the schema below. Show the entire draft to the user inline (in the chat) — *do not write to disk yet.*

4. **Ask for approval.** *"Here's the draft. Want any changes before I write it to `popper-corpus/<slug>/hypothesis.md`?"*

5. **Apply edits** the user requests. Re-show if substantial.

6. **Write the file** to disk after explicit approval. Create the directory if it does not exist.

7. **Confirm** with the user, showing the path: *"Written to popper-corpus/<slug>/hypothesis.md."*

8. **Suggest validation:** *"You can verify the schema with: `python3 scripts/validate_hypothesis.py popper-corpus/<slug>/hypothesis.md`."*

## Schema (hypothesis.md)

YAML frontmatter followed by markdown sections.

**Frontmatter (required keys):**

- `slug` — the directory slug, matches `popper-corpus/<slug>/`.
- `created` — ISO date, e.g. `2026-05-11`.
- `status` — one of `active`, `unfalsifiable`, `retired`.
- `falsifiability_gate` — one of `passed`, `failed`.
- `literature_pass` — one of `completed`, `partial`, `none`.

**Body sections — `falsifiability_gate: passed`:**

- `# <one-line claim>` (the operational restatement, as the title)
- `## Original framing` — the user's first fuzzy version, preserved verbatim in a blockquote.
- `## Operational restatement` — the third-party-measurable form.
- `## Falsifier(s)` — bullet list, ≥1 entry, each concrete.
- `## Test design` — methods, study design, references to standard methods if any.
- `## Auxiliary assumptions` — bullet list, each assumption named.
- `## Distinctiveness` — what the claim forbids that competing accounts don't. May be flagged as `low-information`.
- `## References` — empty if no literature pass, otherwise structured per below.
- `## Intake log` — one or more dated lines summarizing how the conversation went.

**Body sections — `falsifiability_gate: failed`:**

- `# <one-line claim>` (the user's claim, lightly normalized)
- `## Original framing` — same as above.
- `## Diagnostic` — what specifically made the claim unfalsifiable, plus suggestions for reformulation. **Replaces** Operational restatement, Falsifier(s), Test design, Auxiliary assumptions, Distinctiveness.
- `## References` — empty unless a literature pass happened.
- `## Intake log` — dated summary.

**References format:**

Each entry is a YAML-like block:

```
- path: refs/chen-2021.pdf
  pages: 5-9
  contribution: prior null result on comparable design; attributed null to dB level
```

`pages:` is optional (omit for non-paginated files like markdown). `contribution:` is mandatory and should be one specific line — what *this paper specifically contributed* to the hypothesis (not a generic summary).

**Reference paths are relative to the hypothesis file's directory.** Papers live under `popper-corpus/<slug>/refs/`.

## Final reminders

- One probe at a time. Do not bundle questions across probes.
- Prefer multiple-choice or specific questions over open-ended where possible.
- Never invent citations. If you did not open a file, do not cite it. If you opened it but only read part, say which part.
- The user owns the corpus. Show drafts before writing; never write without approval.
- The discipline is constructive. Sharpening, not shaming.
```

- [ ] **Step 2: Run the validator on the existing validator-input fixture as a smoke test**

This confirms the validator still works after all changes (which haven't touched it, but worth confirming before declaring SKILL.md done).

Run: `python3 /Users/masha/Documents/popper-probe/tests/test_validate_hypothesis.py`
Expected: all five validator tests pass.

- [ ] **Step 3: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add skills/intake/SKILL.md
git commit -m "Add termination, file-writing protocol, and schema to intake skill"
```

---

### Task 13: Author one canonical example hypothesis output

Create a hand-authored "golden" output file that demonstrates the schema and is itself validator-passing. Useful both as documentation and as something the eval reviewer can compare new outputs against.

**Files:**
- Create: `docs/examples/popper-corpus/pea-plants-music-biomass/hypothesis.md`
- Create: `docs/examples/popper-corpus/pea-plants-music-biomass/refs/chen-2021-synthetic.md`

- [ ] **Step 1: Create the example directory**

Run: `mkdir -p /Users/masha/Documents/popper-probe/docs/examples/popper-corpus/pea-plants-music-biomass/refs`

- [ ] **Step 2: Write the synthetic reference paper**

Write `docs/examples/popper-corpus/pea-plants-music-biomass/refs/chen-2021-synthetic.md`:

```markdown
# Effects of acoustic exposure on Pisum sativum biomass: a controlled growth-chamber study

**Authors:** Chen, L.; (synthetic example for documentation only)

## Abstract
We exposed Pisum sativum seedlings (N=40) to a 60–80 dB classical music regimen
or silent controls over 21 days under controlled light, temperature, and humidity.
No significant difference in dry biomass was observed between groups (mean
difference 0.03 g, 95% CI [-0.08, 0.14], p = 0.61). When we substituted white
noise at the same dB level in a follow-up arm, results were indistinguishable
from music, suggesting any effect — if present — was driven by dB exposure
rather than musical content.
```

- [ ] **Step 3: Write the example hypothesis file**

Write `docs/examples/popper-corpus/pea-plants-music-biomass/hypothesis.md`:

```markdown
---
slug: pea-plants-music-biomass
created: 2026-05-11
status: active
falsifiability_gate: passed
literature_pass: completed
---

# Pea plants exposed to 60–80 dB classical music gain more biomass than silent controls

## Original framing
> Plants grow better with music.

## Operational restatement
Pea plants (Pisum sativum, variety X) exposed to 60–80 dB classical music for
12 hr/day will gain at least 10% more dry biomass than silent controls over
21 days, under controlled light (16/8 photoperiod), temperature (22 ± 1°C),
and humidity (60% RH).

## Falsifier(s)
- Biomass gain in the music group is ≤ silent controls (within measurement
  error) at 21 days.
- Effect disappears when dB level is held constant but music replaced with
  white noise → would refute *music content* (rather than dB exposure) as
  the active factor.

## Test design
- Methods: dry biomass measured by oven-dry at 60°C to constant weight.
- Design: N=30 per group; randomized seedling assignment; blinded measurement;
  growth chamber controls for light/temp/humidity.
- A second arm with matched-dB white noise tests the auxiliary that music
  content (not dB) is the active factor.

## Auxiliary assumptions
- Music content (not vibration or dB level alone) is the active variable.
- The growth chamber acoustically isolates exposure (no cross-contamination
  between music and silent arms).
- Variety X is not unusually noise-sensitive compared to other pea cultivars.

## Distinctiveness
Predicts a *music-specific* effect that pure-dB or vibration hypotheses don't.
Forbids: equal biomass gain from white noise at the same dB level.

## References
- path: refs/chen-2021-synthetic.md
  contribution: prior null result on comparable design; attributed observed
                null to dB level rather than music content; prompted addition
                of the white-noise control arm in the falsifier list

## Intake log
2026-05-11 — Sharpened from "plants grow better with music." Operational
restatement landed quickly. Probe 2 produced two falsifiers, the second
prompted by Chen 2021's null result during Probe 3's literature pass. Probe 4
distinctiveness clear: predicts music-specific effect.
```

- [ ] **Step 4: Run the validator on the example**

Run: `python3 /Users/masha/Documents/popper-probe/scripts/validate_hypothesis.py /Users/masha/Documents/popper-probe/docs/examples/popper-corpus/pea-plants-music-biomass/hypothesis.md`
Expected: `OK`. If validator fails, the example is wrong — fix it (do not adjust the validator to fit a bad example).

- [ ] **Step 5: Commit**

```bash
cd /Users/masha/Documents/popper-probe
git add docs/examples
git commit -m "Add canonical hypothesis example that passes validator"
```

---

### Task 14: Final pass — README and validator-passes-on-example acceptance

Make sure the README links to the example and the spec/plan files; run the validator suite once more end-to-end; push.

**Files:**
- Modify: `README.md` (add a section pointing to the example + the spec/plan)

- [ ] **Step 1: Read the current README**

Read: `/Users/masha/Documents/popper-probe/README.md`

It currently ends with a link to `context/overview.md`. Add a "Reference" section after the status section that points to the example and the design docs.

- [ ] **Step 2: Replace the README with this updated version**

Use Edit to add a Reference section. The full final README is:

```markdown
# popper-probe

**A research companion that tries to prove your hypotheses wrong.**

Most thinking tools help you build a case. This one helps you break it.

Inspired by Karl Popper, `popper-probe` is a Claude Code skill for
researchers. Bring a fuzzy idea or a half-formed claim, point it at the
papers you've been reading, and it will:

- sharpen the claim into something *risky* enough to be wrong,
- name the observations that would refute it,
- flag the hedges and ad-hoc rescues you didn't notice you were making.

Over time it keeps a markdown ledger of your hypotheses, the evidence
for and against, and the moments you should have changed your mind.

## Status

V1 in implementation: the intake skill (refining ideas into falsifiable
hypotheses). Corpus, observation logging, and audits follow.

## Reference

- Canonical example output:
  [`docs/examples/popper-corpus/pea-plants-music-biomass/`](docs/examples/popper-corpus/pea-plants-music-biomass/)
- Design spec:
  [`docs/superpowers/specs/2026-05-11-popper-probe-intake-design.md`](docs/superpowers/specs/2026-05-11-popper-probe-intake-design.md)
- Implementation plan:
  [`docs/superpowers/plans/2026-05-11-popper-probe-intake-plan.md`](docs/superpowers/plans/2026-05-11-popper-probe-intake-plan.md)
- Vision for the full companion:
  [`context/overview.md`](context/overview.md)

## How this differs from superpowers' `brainstorming` skill

`brainstorming` refines *software designs* through supportive clarification.
`popper-probe` interrogates *empirical claims* through attempted refutation.
They are complementary — use both on a research project: `brainstorming`
for the code, `popper-probe` for the scientific hypothesis.
```

- [ ] **Step 3: Run the full validator test suite once more**

Run: `python3 /Users/masha/Documents/popper-probe/tests/test_validate_hypothesis.py`
Expected: `All 5 test(s) passed`.

- [ ] **Step 4: Run the validator on the canonical example**

Run: `python3 /Users/masha/Documents/popper-probe/scripts/validate_hypothesis.py /Users/masha/Documents/popper-probe/docs/examples/popper-corpus/pea-plants-music-biomass/hypothesis.md`
Expected: `OK`.

- [ ] **Step 5: Commit and push**

```bash
cd /Users/masha/Documents/popper-probe
git add README.md
git commit -m "Update README with references to example and design docs"
git push
```

---

### Task 15: First manual eval pass (acceptance gate)

V1 isn't really "done" until the skill produces validator-passing, rubric-passing output for at least one fixture in a real Claude Code session. This task is **manual** — there is no code to write — but it is the acceptance gate for v1.

**Files:**
- Create: `tests/eval-runs/2026-05-11-bold-distinct/` (output of the first eval run)

- [ ] **Step 1: Start a fresh Claude Code session in this repo**

Open a new terminal session. From `/Users/masha/Documents/popper-probe`, start Claude Code.

- [ ] **Step 2: Run the `bold-distinct` fixture**

Read `tests/fixtures/bold-distinct/input.md`. Copy the user starting claim verbatim into Claude Code as the opening message. Conduct the conversation honestly — answer probes as the user described in the fixture would.

`bold-distinct` is chosen as the first acceptance run because it exercises all four core probes cleanly (no Probe 0, no unfalsifiable diagnostic) and produces a `falsifiability_gate: passed` file. If this works, the path is exercised end-to-end.

- [ ] **Step 3: After the skill writes the hypothesis file, run the validator**

Run: `python3 scripts/validate_hypothesis.py popper-corpus/<slug>/hypothesis.md`
(Replace `<slug>` with whatever slug the skill generated.)
Expected: `OK`.

If the validator fails, the SKILL.md is producing schema-violating output. Read the error, look at the offending section of `skills/intake/SKILL.md`, fix it, commit, and re-run from Step 1.

- [ ] **Step 4: Score the rubric**

Open `tests/rubric.md` and tick each item against what happened in the conversation. Save the completed rubric and the hypothesis file under `tests/eval-runs/2026-05-11-bold-distinct/`:

```bash
mkdir -p /Users/masha/Documents/popper-probe/tests/eval-runs/2026-05-11-bold-distinct
cp popper-corpus/<slug>/hypothesis.md tests/eval-runs/2026-05-11-bold-distinct/hypothesis.md
# create tests/eval-runs/2026-05-11-bold-distinct/rubric.md with the ticked rubric and any notes
```

- [ ] **Step 5: Acceptance decision**

If *all* rubric items pass: v1 is **accepted**. Commit the eval run:

```bash
cd /Users/masha/Documents/popper-probe
git add tests/eval-runs
git commit -m "First eval run: bold-distinct fixture passes acceptance gate"
git push
```

If any rubric items fail: identify the smallest change to `skills/intake/SKILL.md` that addresses the failure. Implement, commit, push, restart from Step 1. Do not relax the rubric to fit imperfect behavior.

**This is the v1 acceptance gate. After this, Phase B (corpus schema) can be brainstormed.**

---

## Plan self-review (run after writing, fix issues inline)

**Spec coverage** — every spec section maps to at least one task:

- Vision (spec §1) — captured in README + context/overview.md (already committed pre-plan).
- Invocation (spec §2 "Invocation") — Task 9.
- Conversation shape, Probes 0–4 (spec §2) — Tasks 10, 11.
- Literature pass (spec §3) — embedded in Task 11 (Probe 3).
- Corpus layout + hypothesis schema (spec §4) — Task 12 (schema section) + validator (Tasks 5, 6) + canonical example (Task 13).
- Termination + file-writing (spec §2 "Termination gate" + §4 "When the file gets written") — Task 12.
- Testing layers 1–3 (spec §5) — Layer 1 validator: Tasks 4–6. Layer 2 fixtures: Task 7. Layer 3 rubric + procedure: Task 8. Anti-hallucination spot check: rubric items in Task 8 + fixture ground-truth in Task 7. Manual eval: Task 15.

**Placeholder scan** — no TBD/TODO/"implement later" anywhere. Each SKILL.md task gives full content. Validator code is complete. Fixture content is complete. Rubric is complete.

**Type consistency** — frontmatter keys and section headers are used identically across the validator (Task 5), the example (Task 13), and the SKILL.md schema section (Task 12). The slug `pea-plants-music-biomass` is consistent in the example. Validator's required-section sets match the schema documented in SKILL.md.

**Out-of-scope confirmation** — observation logging, audits, multi-hypothesis linking, web search outside Probe 0 are all explicitly excluded in SKILL.md (Task 9 scope section) and tested for absence implicitly by the v1 rubric.

Plan is internally consistent and spec-complete. Ready for execution.
