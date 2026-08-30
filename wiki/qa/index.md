# QA

QA pages explain what study notes, experiments, and evidence must prove. They do not replace automated tests or raw results.

## Pages

| Page | Purpose | Status |
| --- | --- | --- |
| [Evidence quality](evidence-quality.md) | Acceptance rules for conceptual and experimental claims | Verified |
| [Lab evidence matrix](evidence-matrix.md) | Numeric proof profiles, tool boundaries, timeouts, retained summaries, and flaky-test policy | Proposed |

## QA rules

- Every conclusion maps to a source or observable evidence.
- Correctness checks and performance measurements are distinguished.
- A benchmark records context, units, and variability, not only an average.
- Failed setup, rejected hypothesis, and inconclusive result are valid terminal states.
- Evidence never contains secrets, personal information, or uncontrolled production data.
