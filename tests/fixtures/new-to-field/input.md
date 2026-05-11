# Input — new-to-field fixture

**User starting claim:**

> I want to study how gut microbiome composition affects mood, but I'm not familiar with this area. What's known?

**No papers supplied.**

**Expected skill behavior:**

- Skill detects uncertainty signals (explicit "I'm not familiar," open question rather than a claim).
- Probe 0 (SoTA orientation) triggers. Skill offers, in one message, the orientation option.
- On user acceptance, skill delivers:
  1. Foundations from training knowledge, with explicit knowledge-cutoff caveat.
  2. Notes that no papers were supplied.
  3. Offers opt-in web search ("I can do a targeted search. I'll show you 3–5 candidates before I cite anything.").
- Only after orientation does the skill proceed to Probe 1 with: "Given that, how would you phrase the claim you want to test?"
- No paper is cited unless the user explicitly chose to pull it.
