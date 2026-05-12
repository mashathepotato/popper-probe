# popper-probe Architecture

Three views: runtime workflow, static structure, data flow.

---

## 1. Runtime workflow — the intake dialogue

The skill runs an optional preamble followed by four probes, terminating
either in a `passed` gate (well-formed falsifiable hypothesis) or a
`failed` gate (unfalsifiable as stated, with diagnostic).

```mermaid
flowchart TD
    Start([User invokes intake<br/>slash command OR hypothesis-shaped text]) --> Q0{Uncertainty<br/>signals?}

    Q0 -->|yes| P0
    Q0 -->|no| P1

    subgraph SoTA[Probe 0 — SoTA orientation, optional preamble]
        P0[Offer orientation<br/>user accepts] --> P0a[Foundations from<br/>training knowledge]
        P0a --> P0b[Recent activity:<br/>user-supplied papers]
        P0b --> P0c{Want web<br/>search?}
        P0c -->|yes, opt-in| P0d[Targeted WebFetch/Search<br/>user picks references<br/>before any citation]
        P0c -->|no| P1
        P0d --> P1
    end

    P1[Probe 1 — Restate operationally<br/>force measurable terms] -->|operational| P2
    P1 -.->|cannot operationalize| FAIL

    P2[Probe 2 — Name the falsifier<br/>what observation refutes?] -->|named| P3
    P2 -.->|none nameable| Choice{Reformulate<br/>or record?}
    Choice -->|reformulate| P1
    Choice -.->|record| FAIL

    P3[Probe 3 — Test design 'the how'<br/>methods, study design, auxiliaries<br/>literature pass on user papers] --> P4

    P4[Probe 4 — Distinctiveness<br/>light, optional<br/>what does it forbid?] --> PASS

    PASS[PASSED gate<br/>status: active<br/>falsifiability_gate: passed]
    FAIL[FAILED gate<br/>status: unfalsifiable<br/>falsifiability_gate: failed<br/>## Diagnostic section]

    PASS --> Write
    FAIL --> Write

    Write[File-writing protocol:<br/>1. Generate slug<br/>2. Check collision append -2,-3<br/>3. Draft inline to user<br/>4. User approves edits<br/>5. Write popper-corpus/&lt;slug&gt;/hypothesis.md<br/>6. Suggest validator]

    Write --> Validate([validate_hypothesis.py<br/>optional offline schema check])
```

### Load-bearing properties

- **Termination is content-gated, not turn-count gated.** The skill
  writes a `passed` file only when probes 1–3 produce their required
  substance; it writes a `failed` file with a diagnostic when sharpening
  genuinely couldn't happen.
- **Network access is gated twice.** Once at the probe level (only
  Probe 0 can search) and once per turn (user must explicitly confirm).
  Probe 3's literature pass is offline by design.
- **No partial files appear mid-conversation.** The draft is shown
  inline; only after user approval does it land on disk.

---

## 2. Static structure — repo, install path, runtime layout

```
github.com/mashathepotato/popper-probe
├── .claude-plugin/
│   ├── plugin.json          ← manifest (name, version, license, ...)
│   └── marketplace.json     ← catalog (lists popper-probe under 'popper')
├── skills/intake/
│   └── SKILL.md             ← THE prompt body
│                              (Probes 0–4, termination, file-writing)
├── scripts/
│   └── validate_hypothesis.py    ← offline schema validator
├── tests/
│   ├── test_validate_hypothesis.py
│   ├── fixtures/            ← 7 eval scenarios + synthetic ref paper
│   ├── rubric.md            ← human review checklist
│   └── README.md            ← how to run an eval
├── docs/
│   ├── examples/popper-corpus/  ← canonical hypothesis file
│   ├── superpowers/specs/   ← design specs
│   ├── superpowers/plans/   ← implementation plans
│   └── ARCHITECTURE.md      ← this file
├── context/
│   └── overview.md          ← cross-session project memory
├── README.md
├── PRIVACY.md
└── LICENSE
```

### Distribution paths

```mermaid
flowchart LR
    Repo[(GitHub repo<br/>mashathepotato/<br/>popper-probe)]

    Repo -->|/plugin marketplace add<br/>mashathepotato/popper-probe| User1[User Claude Code<br/>~/.claude/plugins/<br/>cache/popper/<br/>popper-probe/&lt;ver&gt;/]

    Repo -->|listed via curated<br/>catalog at submission| Anthropic[(Anthropic Official<br/>Marketplace<br/>anthropics/<br/>claude-plugins-official)]

    Anthropic -->|/plugin browse<br/>or marketplace add| User2[User Claude Code<br/>~/.claude/plugins/<br/>cache/&lt;official&gt;/...]
```

Plugins are pinned to a git commit SHA at install time. Updates require
the user to run `/plugin marketplace update <name>` and reinstall.

---

## 3. Data flow — what reads what, what writes what

```mermaid
flowchart LR
    User[User claim<br/>text typed in session] --> Skill
    Papers[User-supplied papers<br/>.pdf / .md / .txt<br/>local filesystem] -.->|Read tool| Skill
    Web[Web search results<br/>opt-in, Probe 0 only<br/>user confirms per turn] -.->|WebFetch/Search| Skill

    Skill[INTAKE SKILL<br/>SKILL.md loaded by Claude Code<br/>conducts Probes 0–4<br/>drafts hypothesis content]

    Skill -->|draft shown inline<br/>user approves| Output[popper-corpus/&lt;slug&gt;/<br/>hypothesis.md<br/>+ refs/ if applicable]

    Output -.->|optional check| Validator[validate_hypothesis.py<br/>exit 0 = OK<br/>exit 1 = schema errors]
```

### What lives on disk after a session

```
popper-corpus/
└── <slug>/
    ├── hypothesis.md     ← YAML frontmatter + structured sections
    └── refs/             ← only if the user staged papers here
        ├── chen-2021.pdf
        └── ...
```

All artifacts are local. The plugin has no backend, telemetry, or
external data store of its own. See [`PRIVACY.md`](../PRIVACY.md) for
the full data-handling statement.

---

## 4. Where each piece is enforced

| Property | Enforced by |
|---|---|
| Schema structure of hypothesis.md | `scripts/validate_hypothesis.py` (objective, runnable) |
| Conversation behavior (probes asked in order, tone, no hallucinated citations) | `tests/rubric.md` (human review) |
| Probes 1–3 must produce non-empty content | validator + SKILL.md termination gate |
| Mandatory `contribution:` field on references | validator |
| No paper cited without being read | SKILL.md instruction + rubric anti-hallucination check |
| File never overwrites; collisions get `-2`, `-3` | SKILL.md file-writing protocol |
