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
