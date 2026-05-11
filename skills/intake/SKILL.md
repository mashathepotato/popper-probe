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

Hedge explicitly: *"My knowledge has a cutoff date — anything since then I won't reliably know. For recent work, see piece 2 or 3 below."* If you do not know the field well, say so directly rather than fabricating consensus.

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
