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
