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
