# DDIA Labs Wiki

## Status

The Wiki-first knowledge architecture is established. Its navigation and maintenance rules are Verified by the current repository structure. The 25-Lab implementation-ready curriculum blueprint is Proposed: concept anchors, ordering, Lab boundaries, workloads, and evidence gates are recorded, but no executable Lab yet verifies runtime behavior.

## Entry points

| Area | Purpose | Entry |
| --- | --- | --- |
| Architecture | Learning boundaries, evidence model, and experiment structure | [architecture/index.md](architecture/index.md) |
| Concepts | Canonical explanations and relationships between DDIA ideas | [concepts/index.md](concepts/index.md) |
| Labs | Experiment questions, designs, results, and limitations | [labs/index.md](labs/index.md) |
| Flows | Repeatable study and experiment workflows | [flows/index.md](flows/index.md) |
| QA | Evidence quality and reproducibility rules | [qa/index.md](qa/index.md) |
| Problems | Failed experiments, misleading results, and resolved causes | [problems/index.md](problems/index.md) |
| Source coverage | Knowledge-to-evidence coverage ledger | [source.md](source.md) |
| Log | Material Wiki, architecture, and evidence changes | [log.md](log.md) |
| Templates | Starting formats for new canonical pages | [templates/index.md](templates/index.md) |

## Knowledge map

~~~text
DDIA source or engineering question
├─ concept: explain the model and trade-offs
├─ decision: define the boundary of a Lab
└─ lab: test one falsifiable hypothesis
   ├─ code/configuration
   ├─ automated checks
   ├─ observations and raw evidence
   └─ conclusion, limits, and new questions
~~~

## Lookup strategy

- To understand how this learning repository is designed, start with [Architecture](architecture/index.md).
- To study an idea, use [Concepts](concepts/index.md), then follow its related Labs.
- To reproduce or extend an experiment, use [Labs](labs/index.md).
- To plan a study iteration, use the [Learning loop](flows/learning-loop.md).
- To judge whether a conclusion is trustworthy, use [Evidence quality](qa/evidence-quality.md) and [Source coverage](source.md).
- To diagnose a failed or misleading experiment, use [Problems](problems/index.md).

## Authority and terminology

- DDIA and cited primary references are sources for conceptual claims.
- Repository code, tests, configuration, and retained measurements are sources for current Lab behavior.
- A benchmark observation is valid only within its documented workload and environment.
- The labels Verified fact, Reasonable inference, and Open question describe evidence strength, not confidence alone.

## Maintenance

When a concept, Lab, flow, QA rule, or problem is added or changed, update its directory index. When evidence is added or invalidated, update [source.md](source.md) and, for a material change, [log.md](log.md).
