# Decision Baseline

## Status

Verified as the accepted initial repository design.

## Accepted decisions

| Decision | Rationale | Revisit when |
| --- | --- | --- |
| Wiki-first knowledge entry point | Keeps questions, scope, evidence, and gaps discoverable before implementation | Navigation becomes slower than direct discovery |
| Concept and Lab pages are separate | Prevents a conceptual explanation from being mistaken for experimental proof | A category consistently has no meaningful distinction |
| Technology is selected per Lab | DDIA trade-offs, not a framework, are the curriculum | Shared infrastructure clearly reduces repetition without hiding behavior |
| Default executable-Lab stack is .NET 10, PostgreSQL 18, and Docker Compose | Gives the planned curriculum a reproducible baseline while allowing a Lab to add another dependency only when its question requires it | A source support window, required mechanism, or reproducibility result invalidates the baseline |
| Each Lab owns its solution, Compose project, commands, data lifecycle, and evidence | Keeps restore, execution, cleanup, and conclusions isolated | A completed Lab demonstrates that a named boundary cannot remain independent |
| Root execution support is policy-only and limited to three files | Preserves discoverability without creating shared runtime behavior that hides the experiment | A fourth file or shared code project is justified by a recorded decision |
| Evidence uses seven profiles and a bounded cross-Lab check | Gives each failure class explicit proof counts while keeping long or hardware-sensitive proofs per-Lab | A completed Lab shows a profile gate or runner boundary is not operationally useful |
| The curriculum blueprint uses a phase overview plus one complete implementation packet per Lab | Lets readers scan the route quickly without sacrificing the details needed for implementation handoff | The first implementation cannot find or execute a required decision without consulting planning history |
| Evidence claims are scoped | Local measurements depend on workload, versions, and environment | Never; this is a core validity rule |
| Large generated results are regenerated | Keeps the repository reviewable and avoids stale output | A compact artifact is required to reproduce a finding |

## Deferred decisions

- Benchmark framework and visualization tooling.
- Automation for checking evidence freshness.

These decisions should be made by the first Lab that genuinely needs them, then recorded with their consequences.
