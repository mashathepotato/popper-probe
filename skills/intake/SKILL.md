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
