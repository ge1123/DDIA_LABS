# Source Coverage

## Status

The Wiki-first structure and initial repository decisions are present on `main` as working-tree changes dated 2026-08-30. No DDIA chapter note or executable Lab has yet been accepted as Verified.

## Coverage status

- Verified: the stated scope is supported by a cited source or reproducible repository evidence.
- Partial: only the explicitly described portion is supported.
- Pending: intent or a study prompt exists without sufficient evidence.
- Outdated: a watched source changed and the page has not been rechecked.

## Coverage ledger

| Slice | Status | Verified revision | Canonical pages | Evidence scope | Remaining boundary | Watched paths |
| --- | --- | --- | --- | --- | --- | --- |
| Wiki-first architecture | Verified | Working tree, 2026-08-30 | [Wiki index](index.md), [Learning architecture](architecture/learning-architecture.md), [Decision baseline](architecture/decision-baseline.md) | Navigation, status model, evidence roles, and maintenance workflow exist in the repository | First real maintenance cycle has not occurred | `AGENTS.md`, `wiki/**` |
| Experiment architecture | Pending | — | [Experiment architecture](architecture/experiment-architecture.md), [Labs](labs/index.md) | Proposed Lab contract and directory convention | No executable Lab validates the convention | `wiki/architecture/experiment-architecture.md`, `wiki/labs/**`, `experiments/**` |
| System quality attributes | Pending | — | [System quality attributes](concepts/system-quality-attributes.md) | Initial questions and repository framing only | Edition/section locator, complete notes, and experiments are missing | `wiki/concepts/system-quality-attributes.md` |
| Evidence acceptance policy | Verified | Working tree, 2026-08-30 | [Evidence quality](qa/evidence-quality.md) | Initial claim categories, review questions, and outcomes are documented | Policy has not yet been exercised by a completed Lab | `wiki/qa/**` |

## Freshness rule

A newer revision does not automatically verify a page. When watched paths change, recheck the relevant statement and evidence before updating the status or revision.

## Evidence policy

- A book reference supports what the source says, not what local code does.
- A design decision defines intent, not observed behavior.
- Tests can support defined invariants but do not automatically establish realistic performance.
- Benchmark results remain scoped to their documented workload and environment.
- Detailed raw output belongs with its Lab artifact or regeneration procedure, not in this ledger.

