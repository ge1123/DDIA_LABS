# Core Lab Learning Path

## Status

Proposed. Primary-source research supports the concept anchors, and a retained logic prototype validates the prerequisite graph's structure. No executable Lab or learner observation yet validates the path's runtime behavior or teaching effectiveness.

## Path rule

The numeric order is the recommended learning route. The prerequisite column is a DAG of concepts required to interpret a later Lab; it is not an execution-time dependency between Lab environments.

Each Lab introduces one main failure boundary or correctness mechanism. Every Lab still owns an independent solution, Compose project, workload, evidence, and cleanup.

## Five phases

| Phase | Labs | Learning transition |
| --- | --- | --- |
| A — Transactions | 01–04 | Row-level races → lost update → snapshot semantics → cross-row write skew |
| B — Retry and messaging | 05–09 | Client retry → broker redelivery → consumer dedup → producer dual write → multi-service compensation |
| C — Distributed reads and placement | 10–13 | Cache staleness → replica lag → shard routing → workload skew |
| D — Coordination safety | 14–15 | Lease ownership → resource-side rejection of stale writers |
| E — Immutable and derived data | 16–20 | Event replay → schema coexistence → CDC recovery → processor recovery → event-time ordering |

## Proposed sequence

| # | Lab | Prerequisites | Main new mechanism |
| --- | --- | --- | --- |
| 01 | Race Condition／overselling | — | Conditional atomic update |
| 02 | Lost Update | 01 | Atomic update or compare-and-set retry |
| 03 | Isolation | 02 | Explicit repeatable snapshot |
| 04 | Write Skew | 03 | Serializable transaction retry |
| 05 | HTTP idempotent command | 02 | Idempotency key and stored result |
| 06 | MQ acknowledgement and redelivery | 05 | Acknowledge after durable effect |
| 07 | Inbox | 02, 06 | Transactional message deduplication |
| 08 | Transactional Outbox | 06, 07 | Transactional event intent and retrying relay |
| 09 | Saga／compensation | 05, 07, 08 | Durable workflow state and idempotent compensation |
| 10 | Cache Consistency | 03 | Versioned cache and minimum-read version |
| 11 | Replication Lag | 03, 10 | Replay token, wait, or primary fallback |
| 12 | Sharding Routing | 02 | Stable hash and explicit shard map |
| 13 | Hot Partition | 12 | Key salting and read fan-in |
| 14 | Distributed Lease | 06, 11 | Owner token, TTL, and compare-delete |
| 15 | Fencing Token | 14 | Monotonic token checked by the resource |
| 16 | Event Sourcing | 02, 08 | Append-only events and deterministic fold |
| 17 | Event／Schema Evolution | 16 | Additive schema and tolerant reader |
| 18 | CDC | 08, 17 | WAL offset／LSN recovery |
| 19 | Stream Restart Correctness | 07, 18 | Atomic input offset, state, and output |
| 20 | Event Time／Out-of-order | 19 | Watermark, grace, and observable late events |

## Boundary checks

- ACK, Inbox, and Outbox remain separate because they study loss/redelivery, duplicate effects, and producer dual write respectively.
- Cache staleness and replica lag remain separate even though both can produce an old read.
- Sharding routing must be correct before Hot Partition measures skew.
- Lease safety precedes Fencing because a valid lease still cannot stop a paused stale worker from writing later.
- Stream restart correctness precedes Event Time so crash atomicity and time semantics are not changed together.

## Evidence

- Concept set and source anchors: [DDIA concept anchors and Core Lab candidates](../../.scratch/ddia-labs-learning-roadmap/research/01-ddia-concept-anchors.md).
- Planning decision and detailed scenarios: [Sequence the 20 Core Labs](../../.scratch/ddia-labs-learning-roadmap/issues/05-sequence-the-core-learning-path.md).
- GitHub tracker: [Issue #5](https://github.com/ge1123/DDIA_LABS/issues/5).
- Prototype: branch `codex/prototype-core-lab-sequence`, commit `94a5a10`.

## Evidence strength

**Verified fact:** primary sources support the named concepts and the split boundaries recorded in the research note. The prototype structurally validates 20 unique nodes, 28 forward-only edges, five phases, no missing dependency, and no cycle.

**Reasonable inference:** this linear order should reduce conceptual jumps. It has not been tested with learners or executable Labs.

**Open question:** exact APIs, workloads, and the final stream implementation boundary are now defined by the [curriculum blueprint](curriculum-blueprint.md). They remain Proposed until executable Labs test feasibility, portability, and the selected evidence gates.
