# Learning Architecture

## Status

Verified for the repository knowledge structure; experiment implementations are not yet present.

## Goal

Turn a DDIA claim or engineering question into an explanation that is traceable to a source and, where practical, a small reproducible experiment.

## Knowledge layers

| Layer | Question answered | Canonical location | Evidence boundary |
| --- | --- | --- | --- |
| Source locator | Where did the claim originate? | Concept or Lab page | Does not prove local behavior |
| Concept | What model and trade-off explain it? | `wiki/concepts/` | Written in the learner's own words |
| Decision | What scope and assumptions are accepted? | `wiki/architecture/` or Lab page | Defines intent, not results |
| Experiment | What observable result could support or refute it? | `wiki/labs/` + `experiments/` | Bound to a documented setup |
| Evidence | What actually happened? | Tests and retained result summary | Must be reproducible and scoped |
| Reflection | What changed in our understanding? | Lab conclusion and `wiki/log.md` | May create new open questions |

## Topic map

The study backlog is grouped into three navigational themes:

1. Foundations: system quality attributes, data models, query languages, storage, retrieval, encoding, and evolution.
2. Distributed data: replication, partitioning, transactions, distributed failure, consistency, and consensus.
3. Derived data: batch processing, stream processing, and systems built from dataflows.

Topic order should follow learning dependencies, not force every idea into a coding exercise.

## Boundaries

- One Lab should answer one main question and state its non-goals.
- Concept pages may exist without code when an experiment would add little evidence.
- Labs must not claim that one local benchmark establishes universal product guidance.
- Technology is chosen per Lab so the tool does not become the curriculum.
- Raw generated data should be reproducible; only small stable evidence belongs in Git.

## Evidence classification

Verified facts are supported by an identified source or reproducible repository evidence. Reasonable inferences follow from facts but have not been directly tested. Open questions identify missing knowledge, conflicting evidence, or deliberately deferred scope.

