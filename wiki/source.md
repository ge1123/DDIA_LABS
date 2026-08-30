# Source Coverage

## Status

The Wiki-first baseline is present on `main` at `f1ca43a`. The monorepo execution model and the complete 25-Lab curriculum blueprint are recorded in the curriculum design snapshot dated 2026-08-30. No DDIA chapter note or executable Lab has yet been accepted as Verified.

## Coverage status

- Verified: the stated scope is supported by a cited source or reproducible repository evidence.
- Partial: only the explicitly described portion is supported.
- Pending: intent or a study prompt exists without sufficient evidence.
- Outdated: a watched source changed and the page has not been rechecked.

## Coverage ledger

| Slice | Status | Verified revision | Canonical pages | Evidence scope | Remaining boundary | Watched paths |
| --- | --- | --- | --- | --- | --- | --- |
| Wiki-first architecture | Verified | `f1ca43a`, 2026-08-30 | [Wiki index](index.md), [Learning architecture](architecture/learning-architecture.md), [Decision baseline](architecture/decision-baseline.md) | Navigation, status model, evidence roles, and maintenance workflow exist in the repository | First real maintenance cycle has not occurred | `AGENTS.md`, `wiki/**` |
| Experiment architecture | Pending | Design snapshot, 2026-08-30 | [Experiment architecture](architecture/experiment-architecture.md), [Decision baseline](architecture/decision-baseline.md), [Labs](labs/index.md) | Lab contract, per-Lab solution/Compose boundary, thin root dispatcher, and shared-file ceiling are accepted designs | No executable Lab validates command portability, isolation, or cleanup | `wiki/architecture/experiment-architecture.md`, `wiki/architecture/decision-baseline.md`, `wiki/labs/**`, `experiments/**`, `global.json`, `Directory.Build.props`, `lab` |
| Core Lab learning path | Partial | Design snapshot, 2026-08-30 | [Core Lab learning path](labs/core-learning-path.md), [Labs](labs/index.md) | Primary-source anchors cover the 20 topics; the retained prototype validates a five-phase DAG with 20 nodes, 28 forward edges, no missing dependency, and no cycle | No executable Labs or learner observations validate implementation feasibility or teaching effectiveness | `.scratch/ddia-labs-learning-roadmap/research/01-ddia-concept-anchors.md`, `.scratch/ddia-labs-learning-roadmap/issues/05-sequence-the-core-learning-path.md`, `wiki/labs/**`, `experiments/**` |
| Extension Lab learning path | Partial | Design snapshot, 2026-08-30 | [Extension Lab learning path](labs/extension-learning-path.md), [Labs](labs/index.md) | Core prerequisites, canonical Lab boundaries, and technology escalation rules support a five-Lab portfolio with two comparisons, two realistic faults, and one degradation experiment | No executable Labs or learner observations validate feasibility, thresholds, or teaching value | `.scratch/ddia-labs-learning-roadmap/issues/06-choose-the-extension-labs.md`, `.scratch/ddia-labs-learning-roadmap/research/02-technology-baseline.md`, `wiki/labs/**`, `experiments/**` |
| Implementation-ready curriculum blueprint | Partial | Design snapshot, 2026-08-30 | [Curriculum blueprint](labs/curriculum-blueprint.md), [Core path](labs/core-learning-path.md), [Extension path](labs/extension-learning-path.md) | All 25 Labs have one problem, executable invariant, data/API budget, Broken and Correct mechanism, controlled workload or fault, direct proof, evidence profile, technology, prerequisites, limits, and evidence-strength labels | The exact fixtures, thresholds, fault controls, line budgets, and local product behavior are design inferences until each executable Lab retains accepted evidence | `.scratch/ddia-labs-learning-roadmap/issues/08-assemble-the-implementation-ready-blueprint.md`, `wiki/labs/**`, `wiki/qa/**`, `experiments/**` |
| System quality attributes | Pending | — | [System quality attributes](concepts/system-quality-attributes.md) | Initial questions and repository framing only | Edition/section locator, complete notes, and experiments are missing | `wiki/concepts/system-quality-attributes.md` |
| Evidence acceptance policy | Verified | `f1ca43a`, 2026-08-30 | [Evidence quality](qa/evidence-quality.md) | Initial claim categories, review questions, and outcomes are documented | Policy has not yet been exercised by a completed Lab | `wiki/qa/**` |
| Lab evidence matrix | Pending | Design snapshot, 2026-08-30 | [Lab evidence matrix](qa/evidence-matrix.md), [Evidence quality](qa/evidence-quality.md) | Seven profiles define Broken／Correct run counts, deadlines, performance variability, probabilistic exceptions, retained summaries, flaky handling, and cross-Lab checks | No executable Lab has exercised the numeric gates, JSON contract, or aggregate runner | `.scratch/ddia-labs-learning-roadmap/issues/07-define-the-evidence-matrix.md`, `wiki/qa/**`, `experiments/**`, `lab` |

## Freshness rule

A newer revision does not automatically verify a page. When watched paths change, recheck the relevant statement and evidence before updating the status or revision.

## Evidence policy

- A book reference supports what the source says, not what local code does.
- A design decision defines intent, not observed behavior.
- Tests can support defined invariants but do not automatically establish realistic performance.
- Benchmark results remain scoped to their documented workload and environment.
- Detailed raw output belongs with its Lab artifact or regeneration procedure, not in this ledger.
