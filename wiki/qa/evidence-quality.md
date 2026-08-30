# Evidence Quality

## Status

Verified as the initial acceptance policy.

Numeric run counts, deadlines, tooling boundaries, and flaky-test handling are defined by the proposed [Lab evidence matrix](evidence-matrix.md).

## Acceptance matrix

| Claim type | Minimum evidence | Common invalid shortcut |
| --- | --- | --- |
| Conceptual | Source locator plus explanation in the learner's own words | Treating memory or an unsourced summary as authoritative |
| Correctness | Deterministic setup and an observable invariant, preferably automated | Treating process exit code alone as correctness |
| Performance | Workload, environment, versions, units, warm-up, repeated runs, and variability | Reporting one run or only an average |
| Failure behavior | Controlled fault, bounded blast radius, observed response, and cleanup | Causing an uncontrolled outage |
| Comparative | Same relevant conditions and one intentional changed variable | Comparing unlike workloads or environments |

## Review questions

- Can another learner run the documented entry point without hidden state?
- Does the observation address the hypothesis rather than merely showing the program ran?
- Are facts separated from interpretation?
- Are contradictory observations and known confounders preserved?
- Is the conclusion no broader than the tested workload and environment?
- Would a dependency, fixture, or configuration change make this evidence stale?

## Outcomes

- Verified: acceptance criteria pass for the explicitly stated scope.
- Partial: useful evidence exists, but named boundaries remain unverified.
- Inconclusive: the setup ran, but evidence cannot distinguish the competing explanations.
- Rejected: evidence contradicts the hypothesis.
- Invalid: setup or measurement defects prevent interpretation.
