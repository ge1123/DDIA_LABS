# Extension Lab Learning Path

## Status

Proposed. The five-Lab portfolio is an accepted curriculum decision grounded in the Core prerequisite graph and the canonical Lab boundary. No executable Lab or learner observation yet validates its feasibility or teaching value.

## Portfolio rule

Extension Labs deepen an already-established Core concept through an alternative mechanism, a realistic fault, or a performance-degradation workload. They never become prerequisites of the 20-Lab Core path.

Every Extension retains one main question, invariant, and changed variable. It uses the same Broken → Correct evidence flow and the same per-Lab solution, Compose, workload, evidence, and cleanup boundary as a Core Lab.

## Proposed sequence

| ID | Lab | Primary purpose | Core prerequisites | New dimension | Main non-goal |
| --- | --- | --- | --- | --- | --- |
| E01 | Serializable vs Explicit Locking under Contention | Alternative-mechanism comparison | 03, 04 | Concurrency-control strategy under a fixed contention workload | Re-teaching isolation or claiming a universal winner |
| E02 | Cache Stampede at a TTL Cliff | Performance degradation | 10 | Origin amplification and tail latency during a synchronized expiry burst | Changing the cache-consistency rule |
| E03 | Synchronous Replication under Primary Loss | Realistic fault | 11 | Acknowledged-write durability during abrupt primary loss and promotion | RTO or general availability comparison |
| E04 | Outbox Relay: Polling vs CDC | Alternative-mechanism comparison | 08, 18 | Relay recovery and commit-to-observable latency | Re-teaching Outbox or CDC correctness |
| E05 | Consumer-group Rebalance Ownership Fencing | Realistic fault | 15, 19 | Stale partition owner after assignment changes | Broker loss, generic deduplication, or event-time semantics |

## Ordering rule

The recommended order is `E01 → E02 → E03 → E04 → E05`. It increases operational complexity from one-database contention through cache bursts and replica promotion to CDC and consumer-group coordination. The Extension Labs do not depend on each other at runtime.

## Environment ceiling

- Use no more than two kinds of stateful external system in one Extension; multiple nodes of one system are allowed.
- Keep every environment local and Compose-owned.
- Introduce Redis, Kafka, Debezium, Testcontainers, or k6 only for the observation named by the Lab.
- Do not add cloud services, Kubernetes, production credentials, or production data.

## Evidence

- Core prerequisite graph: [Core Lab learning path](core-learning-path.md).
- Detailed selection and rejected alternative: [Choose the advanced Extension Labs](../../.scratch/ddia-labs-learning-roadmap/issues/06-choose-the-extension-labs.md).
- GitHub tracker: [Issue #6](https://github.com/ge1123/DDIA_LABS/issues/6).
- Technology escalation rules: [Technology baseline](../../.scratch/ddia-labs-learning-roadmap/research/02-technology-baseline.md).

## Evidence strength

**Verified fact:** the Core path, Lab contract, and technology escalation rules define the prerequisites and scope constraints used by this selection.

**Reasonable inference:** this five-Lab portfolio adds useful depth without weakening or lengthening the Core prerequisite path. It has not been validated by implementation or learner evidence.

**Open question:** exact workloads, primary metrics, APIs, fixtures, and profiles are now declared in the [curriculum blueprint](curriculum-blueprint.md). They remain Proposed until executable Labs validate the comparison thresholds, fault harnesses, and reference-runner assumptions.
