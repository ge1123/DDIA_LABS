# Wiki Maintenance Guide

This Wiki is the project's knowledge entry point and evidence map. It does not replace DDIA, implementation code, tests, benchmark output, or accepted architecture decisions.

## Wiki-first workflow

1. Read [index.md](index.md) and identify the relevant area.
2. Open only the directly relevant canonical pages.
3. Check page status and [source.md](source.md) before treating a statement as established.
4. Separate Verified facts, Reasonable inferences, and Open questions.
5. Before a new experiment, record its question, hypothesis, variables, workload, measurement, and stop conditions.
6. After an experiment, link reproducible evidence and update its status without overstating the result.

## Evidence roles

- The book and other primary references explain concepts and claims; record edition/chapter/section locators when useful.
- Decision pages record accepted repository or experiment choices.
- Experiment code and configuration define what was actually run.
- Automated tests verify invariants and setup behavior.
- Raw measurements support observations for a particular workload and environment; they do not prove universal performance.
- The Wiki provides navigation, explanations in the learner's own words, evidence links, and known gaps.

## Page status

- Proposed: a study or experiment design that has not been executed.
- Pending: intent exists, but the page lacks enough evidence for its stated scope.
- Partial: only the explicitly named scope has evidence.
- Verified: the explicitly named scope is supported by reproducible evidence.
- Outdated: watched sources changed and the page has not been rechecked.

Status applies to the stated scope, not automatically to every sentence on a page.

## Maintenance rules

- Keep each fact on one canonical page and cross-link instead of duplicating it.
- Keep `index.md` focused on navigation and a short status summary.
- Use `source.md` as the evidence ledger, not as a test log.
- Use `log.md` only for material knowledge, architecture, evidence-status, or known-gap changes.
- Use stable relative links. Do not link ephemeral local paths or commit secrets, credentials, personal data, or production datasets.
- Prefer small committed fixtures and result summaries. Document how to regenerate large measurements.
- Record hardware, software version, dataset/workload, warm-up, run count, and units for performance claims.
- If evidence conflicts with the current explanation, preserve the conflict and downgrade status until resolved.
- When adding a page, update its directory index and necessary cross-links.

