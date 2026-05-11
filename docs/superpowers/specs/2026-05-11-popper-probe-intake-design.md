# popper-probe Intake (v1) — Design

**Status:** Approved, ready for implementation planning
**Date:** 2026-05-11
**Scope:** v1 only — the Intake skill. Phases B (corpus schema beyond intake's needs), C (observation logging), and D (audit & surfacing) are out of scope and will each get their own spec.

---

## 1. Vision (full companion)

`popper-probe` is a Claude Code skill (or set of skills) that gives a researcher a Popperian companion for the life of a project. It maintains a markdown corpus of:

- **Hypotheses** the researcher holds, each phrased as a falsifiable claim with explicit risky predictions and a sketch of how to test them.
- **Observations** logged against those hypotheses (supporting, contradicting, inconclusive), with citations to papers or experiments.
- **Audits** that surface stale, vague, ad-hoc-rescued, or contradicted claims over time.

The discipline is adversarial but constructive: interactions ask *"what would prove this wrong?"* and *"how would you actually test it?"* — not *"how do we make this work?"* Literature is treated as a source of potential falsifiers and methods reference, not authority.

**Form factor.** A Claude Code skill in the standard `SKILL.md` format, distributed as part of this repo (later: as a Claude Code plugin). The full companion may grow into a set of skills (intake, observation-logger, auditor); v1 is one skill. State lives in a local markdown corpus in the user's working directory. No runtime infrastructure beyond what Claude Code already provides (file reading, including PDFs).

**Target user.** Researchers and scientists. Vocabulary leans on philosophy of science (falsifiability, risky predictions, auxiliary hypotheses, ad-hoc rescue) — the tool assumes the user knows or wants to learn these terms.

**Relationship to superpowers' `brainstorming`.** Complementary, not redundant. `brainstorming` refines *software designs* through supportive clarification. `popper-probe` interrogates *empirical claims* through attempted refutation. A researcher building an ML experiment could use `brainstorming` for the code and `popper-probe` for the scientific hypothesis.

---

## 2. Intake skill — scope and conversation shape

### Invocation

The user invokes the skill in one of two ways:

- **Explicit:** the slash form `/popper-probe:intake` (or whatever Claude Code's plugin-qualified skill invocation is).
- **Implicit:** the skill auto-activates when the user describes something hypothesis-shaped — a claim about the world they expect to be testable. This follows the `using-superpowers` convention of invoking a skill whenever it might apply.

In both cases, the user may include initial papers / lit-review paths in the same message (e.g., *"I think X. Papers: refs/chen-2021.pdf, refs/smith-2019.pdf"*). The skill picks them up automatically if present.

### What it does

Adversarial-but-constructive Popperian dialogue. One probe at a time, aimed at sharpening a fuzzy claim into one that is (a) operationally stated, (b) falsifiable with a named refuter, and (c) testable — the user leaves with a sketch of how they would actually test it.

### What it does not do

Observation logging, audits, multi-hypothesis comparison, web search (user supplies papers).

### Conversation shape — four probes, in order

1. **Restate operationally.** Force the claim into terms a third party could measure. *"Plants grow better with music"* → *"Pea plants exposed to 60–80 dB classical music for 12 hr/day will gain X% more biomass than silent controls over Y days."* Skill keeps probing until the restated form is unambiguous.

2. **Name the falsifier.** *What observation would make you abandon this?* If the user cannot name one, the claim is unfalsifiable as stated — the skill says so and offers to either reformulate or write a `status: unfalsifiable` file with a diagnostic.

3. **Design the test (the "how" — emphasis here).** Constructive, not adversarial. Walks the user through:
   - **Methods & instruments** — how would the relevant variables actually be measured?
   - **Study design** — controls, sample size intuition, what counts as a clean run.
   - **Auxiliary assumptions** — what else has to be true for the test to be meaningful? (Instrument accuracy, no confound X, population assumption Y.) These get logged because they are the rescue surface: future ad-hoc patches will attack these.
   - **Literature pass happens here.** If the user supplied papers, the skill reads them against the proposed test: *has this design been tried? what did they find? what methods or hedges did the field use when results were inconvenient?* Mechanics in section 3.

4. **Distinctiveness check (light, optional).** One question: *what does this hypothesis predict that competing accounts don't?* If the answer is "nothing in particular," that is recorded as a flag in the file (not a block) — the user may still want to test it, but they will know it is low-information.

### Termination gate

The hypothesis is written to the corpus when probes 1–3 produce: operational restatement, ≥1 falsifier, named auxiliaries, and a test sketch. Probe 4 is recorded but not gating.

### Tone

Sparring partner, not judge. Probes 1–2 are sharpening, probe 3 is collaborative design, probe 4 is curiosity. The skill says *"can you sharpen this?"* not *"this is bad."*

---

## 3. Literature pass mechanics

### Input

The user points the skill at papers explicitly: a list of file paths (absolute or relative), or a folder path containing them. Convention: if the user has pre-staged papers under `<corpus>/<hypothesis-slug>/refs/`, the skill picks those up automatically. Supported formats: PDF, markdown, plaintext.

### Reading strategy

Papers are big; the skill triages instead of dumping:

1. **First pass:** abstract → intro → conclusion (cheap, gives the field's framing and the paper's claim).
2. **Targeted pass:** the section relevant to the current probe (methods if probe 3 is mid-design discussion; results if checking for prior refutation).
3. **Deep pass only on user request:** *"I read the abstract and methods of Smith 2019. Want me to dig into the results section?"*

For PDFs longer than ten pages, the skill reads in page ranges and tells the user what range it pulled, so it is honest about coverage.

### What it looks for

Four targeted lenses, not a generic summary:

- **Prior tests.** Has this hypothesis (or a near-equivalent) already been tested? With what result?
- **Standard methods in the field.** What study designs are used for this kind of claim, and what are their known weaknesses?
- **Reported refutations.** Papers reporting the hypothesis failing — flagged as critical.
- **Common hedges / rescues.** Recurring phrases the field uses when results disappoint (*"under certain conditions," "in this subpopulation only"*). These often map directly to ad-hoc rescues the user might be tempted to make.

### How findings enter the dialogue

One at a time, brief, with a citation:

> *"Chen 2021 (p. 7) ran a comparable design with N=40 and found no effect. They attributed it to dB level rather than musical content. Does that change how you'd specify the music exposure?"*

Not lectures. Each finding asks the user to do something with it — update the test, narrow the claim, abandon it, or note it as known prior art.

### What gets recorded

A `references:` section in the hypothesis markdown file (schema in section 4).

### No papers? Skip cleanly

Hypothesis file gets `literature_pass: none` and the skill moves on. Literature pass is value-add, not a gate.

### Token budget honesty

The skill says what it actually read and what it skipped, so the user knows when a deeper pass is worth requesting. **No hallucinated citations — if the skill did not open the file, it does not cite it.**

---

## 4. Corpus layout and hypothesis file schema

### Corpus location

Default: `popper-corpus/` in the researcher's current working directory. No `.config` file in v1 — convention over configuration. (Configurable in a later phase if needed.)

### Per-hypothesis layout

```
popper-corpus/
  pea-plants-music-biomass/
    hypothesis.md       ← the structured intake artifact
    refs/               ← user-supplied papers (optional)
      chen-2021.pdf
      zhao-2018.md
```

One directory per hypothesis. Slug is generated from a short summary of the claim; collisions get `-2`, `-3`, etc. — never overwrite. Future phases (observations, audits) add sibling files (`observations.md`, `audits.md`) — no restructure needed.

### `hypothesis.md` schema

YAML frontmatter for machine-readable fields, markdown body for the substance:

```markdown
---
slug: pea-plants-music-biomass
created: 2026-05-11
status: active            # active | unfalsifiable | retired
falsifiability_gate: passed   # passed | failed
literature_pass: completed     # completed | partial | none
---

# Pea plants exposed to 60–80 dB classical music gain more biomass than silent controls

## Original framing
> Plants grow better with music.

## Operational restatement
Pea plants (variety X) exposed to 60–80 dB classical music for 12 hr/day
will gain at least Y% more dry biomass than silent controls over Z days,
under controlled light/temp/humidity.

## Falsifier(s)
- Biomass gain in music group ≤ silent controls (within measurement error) at Z days.
- Effect disappears when dB level is held constant but music replaced with white noise → would refute *music* as the active factor.

## Test design
- Methods: dry biomass by oven-dry at 60°C to constant weight; growth chamber controls for light/temp/humidity.
- Design: N=… per group, randomized seedling assignment, blinded measurement.
- Standard reference for biomass method: Zhao 2018.

## Auxiliary assumptions
- Music is the active variable, not vibration / dB level alone.
- Growth chamber isolates acoustic exposure (no cross-contamination).
- Pea variety X is not unusually noise-sensitive vs. other varieties.

## Distinctiveness
Predicts a *music-specific* effect that pure-dB or vibration hypotheses don't.
Forbids: equal effect from white noise at same dB.

## References
- path: refs/chen-2021.pdf
  pages: 5-9
  contribution: prior null result on comparable design; attributed null to dB level rather than music
- path: refs/zhao-2018.md
  contribution: standard method source for dry biomass measurement

## Intake log
2026-05-11 — Sharpened from "plants grow better with music." Falsifier added
after probe 2. Chen 2021 surfaced during literature pass, prompted the
white-noise control in falsifiers.
```

### When the file gets written

At the end of intake, the skill drafts the full file and shows it to the user inline before writing. User approves (or asks for edits) — then the file lands on disk. No partial files appear mid-conversation.

### Unfalsifiable outcome

Same schema, `falsifiability_gate: failed`, `status: unfalsifiable`. Test design and distinctiveness sections are replaced by a single `## Diagnostic` section explaining what was unfalsifiable about the claim and what reformulation might rescue it. The user still gets a file — it documents the dead end.

### No corpus index in v1

The file listing *is* the index. An `INDEX.md` or audit roll-up is a Phase D concern.

---

## 5. Testing approach

A Claude Code skill is a prompt body driving a conversation — not a unit-testable function. "Testing" here means evaluation against fixed scenarios, not pytest. Three layers, scaled to v1's actual scope:

### Layer 1 — Schema validator (automatable)

A small script (`scripts/validate-hypothesis.sh` or `.py`) that checks any `hypothesis.md`:

- YAML frontmatter has all required keys with valid values.
- If `falsifiability_gate: passed`: required sections (operational restatement, ≥1 falsifier, test design, auxiliaries) are present and non-empty.
- If `falsifiability_gate: failed`: a `## Diagnostic` section exists.
- `references:` entries point to files that actually exist.

Runs locally on demand. Catches structural regressions when SKILL.md is edited.

### Layer 2 — Fixture-based evals (manual for v1)

A `tests/fixtures/` directory with 5–6 canonical input scenarios. Each fixture is a folder containing an `input.md` (the fuzzy claim + any setup notes) and `refs/` (sample papers — small public-domain or synthetic content to keep the repo light):

| Fixture | Input | Expected behavior |
|---|---|---|
| `vague-claim` | "AI will make programmers obsolete" | Force operational restatement; user likely cannot name a falsifier → flag as unfalsifiable-as-stated |
| `already-operational` | A claim already in measurable terms | Skip probe 1 quickly; not force redundant restatement |
| `with-refutation` | Claim + a paper that refutes it | Literature pass surfaces the refutation in probe 3 |
| `hedged-claim` | Claim full of "may," "could," "in some cases" | Call out the hedges, force user to commit |
| `bold-distinct` | A claim that clearly forbids competing predictions | Probe 4 (distinctiveness) passes cleanly, file marked high-info |
| `unfalsifiable` | "Consciousness emerges from complexity" | `falsifiability_gate: failed`, diagnostic written |

For v1, evals are run manually: pick a fixture, run the skill, compare the resulting `hypothesis.md` against the expected shape using the validator and a human rubric (Layer 3). Document failures, iterate on SKILL.md. Automating the conversation loop is a Phase B+ concern.

### Layer 3 — Human rubric (`tests/rubric.md`)

A reviewer checklist for things the validator cannot check:

- All four probes were asked, in order.
- Tone stayed constructive (no hostile or judgy phrasings).
- Probe 3 (the "how") got real airtime, not skipped.
- Literature pass cited only what was actually read (anti-hallucination).
- Skill did not lecture — every finding was tied to a question for the user.
- Termination happened at the gate, not arbitrarily.

Pass/fail per item. Run after each fixture eval.

### Anti-hallucination spot check

For fixtures that include papers, the fixture metadata records "this paper actually says X on page Y." The reviewer confirms any citation in the output matches. If the skill cites something not in the paper, that is a critical failure — fix the SKILL.md to be more conservative about citation.

### Not in v1

Automated conversation drivers, regression suites, scored evals, statistical comparison across SKILL.md versions. All Phase B+ if the project matures.

---

## 6. Out of scope for v1

- **Phase B — Corpus schema beyond intake's needs.** Cross-hypothesis linking, project-level metadata, audit roll-ups.
- **Phase C — Observation logging.** A separate skill/flow for adding observed evidence (supports / contradicts / inconclusive) against a hypothesis, with citations.
- **Phase D — Audit & surfacing.** Re-review of the corpus: stale claims, accumulated counter-evidence, ad-hoc rescues, unfalsifiable retrofits.

Each is its own spec → plan → build cycle, informed by what we learn from v1 in use.
