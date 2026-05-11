# popper-probe — Project Overview

A Claude Code skill (or set of skills) that gives a researcher a **Popperian
companion** for the life of a project. It maintains a markdown corpus of
hypotheses, observations, and audits, and interrogates them adversarially
rather than supportively.

## The discipline

Every interaction asks *"what would prove this wrong?"* — not
*"how do we make this work?"* Literature is treated as a source of potential
falsifiers, not authority. Bold, risky hypotheses are preferred over safe,
hedged ones. Unfalsifiable claims are flagged, not refined.

## Subsystems (full vision)

| # | Sub-project | What it does |
|---|---|---|
| A | **Intake** | Fuzzy idea → falsifiable hypothesis with risky predictions, written to corpus. Can read papers / lit reviews the user supplies. |
| B | **Corpus** | Directory layout and schema for hypotheses, predictions, observations, audits. |
| C | **Observation logging** | Add observed evidence (supports / contradicts / inconclusive) against a hypothesis, with citations. |
| D | **Audit & surfacing** | Re-review the corpus: stale claims, accumulated counter-evidence, ad-hoc rescues, unfalsifiable retrofits. |

Each is its own spec → plan → build cycle.

## V1 scope

**Intake only.** Converts a fuzzy idea into a hypothesis file in the corpus,
using both the researcher's input and any papers / lit reviews they point
the skill at.

**Non-goals for v1:**
- No observation logging UX
- No audit pass
- No LLM-driven paper search (user supplies the papers)
- No inter-hypothesis linking

B, C, D are deliberately deferred. Each will get its own spec after v1 is in
use long enough to inform the schema.

## Form factor

Claude Code skill + local markdown corpus. No runtime infrastructure beyond
what Claude Code already provides (file reading, including PDFs).

## Target user

Researchers and scientists. Vocabulary leans on philosophy of science
(falsifiability, risky predictions, auxiliary hypotheses, ad-hoc rescue) —
the tool assumes the user knows or wants to learn these terms.

## How this differs from superpowers' `brainstorming` skill

| | superpowers `brainstorming` | popper-probe |
|---|---|---|
| Domain | Software design | Empirical claims |
| Method | Refine through clarification | Refine through attempted refutation |
| Output | Design spec to build from | Falsifiability ledger maintained over time |
| Tone | Supportive Socratic | Adversarial Socratic |

They are complementary, not redundant. A researcher building an ML
experiment could use `brainstorming` for the *code* and `popper-probe` for
the *scientific claim being tested*.
