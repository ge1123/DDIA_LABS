# Decision Baseline

## Status

Verified as the accepted initial repository design.

## Accepted decisions

| Decision | Rationale | Revisit when |
| --- | --- | --- |
| Wiki-first knowledge entry point | Keeps questions, scope, evidence, and gaps discoverable before implementation | Navigation becomes slower than direct discovery |
| Concept and Lab pages are separate | Prevents a conceptual explanation from being mistaken for experimental proof | A category consistently has no meaningful distinction |
| Technology is selected per Lab | DDIA trade-offs, not a framework, are the curriculum | Shared infrastructure clearly reduces repetition without hiding behavior |
| Evidence claims are scoped | Local measurements depend on workload, versions, and environment | Never; this is a core validity rule |
| Large generated results are regenerated | Keeps the repository reviewable and avoids stale output | A compact artifact is required to reproduce a finding |

## Deferred decisions

- Primary programming language and build system.
- Container orchestration or cloud platform.
- Benchmark framework and visualization tooling.
- Automation for checking evidence freshness.

These decisions should be made by the first Lab that genuinely needs them, then recorded with their consequences.

