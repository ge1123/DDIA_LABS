# Wiki Log

This page records only material changes to knowledge architecture, experiment architecture, evidence status, and known gaps.

## 2026-08-30 — Proposed implementation-ready curriculum blueprint

- Completed consistent implementation packets for all 20 Core and five Extension Labs, including exact API budgets, data shapes, deterministic schedules, fault points, evidence profiles, and limits.
- Chose a phase overview plus per-Lab implementation packets as the canonical information structure; retained three alternative layouts on prototype branch `codex/prototype-curriculum-blueprint` at commit `d5547aa`.
- Selected a real PostgreSQL physical standby for replication lag and a .NET processor with PostgreSQL-atomic checkpoint, state, and output for the final stream Labs; explicitly excluded Kafka end-to-end exactly-once claims.
- Kept the blueprint Partial in source coverage because all concrete fixtures and thresholds remain unvalidated design inferences until executable Labs retain accepted evidence.

## 2026-08-30 — Proposed Lab evidence matrix

- Assigned all 20 Core and five Extension Labs to seven evidence profiles with explicit Broken／Correct run counts and deadlines.
- Defined performance variability, probabilistic exceptions, retained-summary fields, and a no-auto-retry flaky-test policy.
- Allowed a bounded `./lab all check` with filesystem discovery, at most two workers, complete failure aggregation, and per-Lab cleanup.
- Kept the matrix Pending until the first executable Lab validates its numeric gates and runner behavior.

## 2026-08-30 — Proposed Extension Lab portfolio

- Selected five optional Labs: two alternative-mechanism comparisons, two realistic fault models, and one performance-degradation experiment.
- Kept every Extension downstream of the Core path and prohibited it from becoming a Core prerequisite.
- Split replication durability from RTO and rejected Redis failover because it overlapped the Core lease/fencing mechanism.
- Marked the portfolio Partial in source coverage: its prerequisites and boundaries are supported, but implementation feasibility and teaching value remain unverified.

## 2026-08-30 — Proposed Core Lab learning path

- Ordered 20 Core Labs into five phases from transaction races through event-time processing.
- Recorded 28 prerequisite edges while keeping every Lab independently executable.
- Kept ACK/Inbox/Outbox, cache/replication staleness, routing/hot partition, lease/fencing, and stream restart/event time as separate failure boundaries.
- Marked the path Partial in source coverage: concept anchors and graph structure have evidence, but implementation feasibility and teaching effectiveness remain unverified.

## 2026-08-30 — Per-Lab execution boundary

- Accepted one independent solution, Compose project, command implementation, data lifecycle, and evidence boundary per Lab.
- Chose a thin root `lab` dispatcher with six standard single-Lab actions; deferred cross-Lab execution until the evidence matrix is defined.
- Limited shared execution policy to `global.json`, `Directory.Build.props`, and the dispatcher, with no shared runtime or correctness code.
- Kept experiment architecture Pending until the first executable Lab validates isolation, portability, and idempotent cleanup.

## 2026-08-30 — Wiki-first baseline

- Established the Wiki as the project knowledge entry point.
- Separated concept explanations, Lab designs/results, flows, QA rules, diagnosed problems, and source coverage.
- Adopted Proposed, Pending, Partial, Verified, and Outdated page states.
- Adopted a learning loop from question and source study through falsifiable experiment, scoped observation, and reflection.
- Deferred programming language, build system, infrastructure, and benchmark tooling until a concrete Lab requires them.
- Added the first Pending concept page for reliability, scalability, and maintainability; no executable Lab is claimed complete.
