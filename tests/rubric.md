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
