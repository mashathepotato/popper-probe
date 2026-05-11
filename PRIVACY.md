# popper-probe Privacy Policy

_Last updated: 2026-05-11_

popper-probe is a Claude Code skill that runs entirely on the user's
local machine. It has no backend, no telemetry, no analytics, and no
external data collection of its own.

## What this plugin processes

- **Text the user types in a Claude Code session** is processed by
  Claude's underlying language model. That processing is governed by
  [Anthropic's Privacy Policy](https://www.anthropic.com/legal/privacy),
  not by this plugin.
- **Papers the user supplies** (PDF, markdown, plaintext) are read from
  the user's local filesystem during a conversation. They are not
  uploaded, cached, or transmitted by this plugin.
- **Hypothesis files and references** are written to a local directory
  (`popper-corpus/` in the user's working directory). They are not
  transmitted anywhere by this plugin and remain entirely under the
  user's control.

## Web access

The plugin is offline by default. The single exception is Probe 0's
optional state-of-the-art orientation:

- If — and only if — the user explicitly confirms a web search for that
  turn, the plugin issues a targeted WebFetch / WebSearch.
- Search queries are sent to whatever search backend Claude Code uses
  and are subject to Anthropic's privacy policy and the underlying
  search provider's terms.
- The user is shown candidate results before any paper is cited; no
  paper is read without explicit user selection.
- No information about the user's hypotheses is transmitted unless the
  user has approved a search for that turn.

## Data the plugin stores

None of its own.

All artifacts produced by popper-probe (hypothesis files, references,
intake logs) exist only on the user's local machine in the
`popper-corpus/` directory. Deletion is under the user's control.

## Third parties

popper-probe does not share any data with third parties. The plugin
itself initiates no third-party connections beyond the opt-in web
search described above.

## Children

popper-probe is a tool for researchers and is not directed at children
under 13. It collects no personal information of its own.

## Changes to this policy

If this policy changes, the updated version will be committed to this
repository and the "Last updated" date above will be revised.

## Contact

For questions, issues, or concerns about this policy or the plugin's
behavior, open an issue at
[github.com/mashathepotato/popper-probe/issues](https://github.com/mashathepotato/popper-probe/issues).
