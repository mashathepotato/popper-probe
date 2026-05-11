# Input — with-refutation fixture

**User starting claim:**

> Listening to Mozart immediately before a spatial reasoning task improves performance compared to silence ("the Mozart effect").

**Paper supplied:** `refs/synthetic-null-result.md`

**Expected skill behavior:**

- Probe 3's literature pass reads the supplied paper, surfaces the null result, and prompts the user with a citation-anchored question (e.g., "Smith et al. found no effect at N=120 — does this change your falsifier?").
- The resulting hypothesis file's `## References` section includes the supplied paper with a `contribution:` line that mentions prior null result.
- The user may decide to abandon, narrow, or proceed; any outcome is acceptable as long as the literature pass surfaced the refutation.

**Anti-hallucination ground truth:** the paper at `refs/synthetic-null-result.md` reports N=120 and a null result; the abstract specifically uses the phrase "no statistically significant difference."
