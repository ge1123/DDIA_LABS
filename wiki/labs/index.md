# Labs

Lab pages define and interpret experiments. Executable artifacts live under [`experiments/`](../../experiments/README.md).

## Planned learning path

| Path | Scope | Status |
| --- | --- | --- |
| [Implementation-ready curriculum blueprint](curriculum-blueprint.md) | Thirty-second overview and complete implementation packets for all 25 Labs | Proposed |
| [Core Lab learning path](core-learning-path.md) | Five phases and the prerequisite DAG for 20 planned Core Labs | Proposed |
| [Extension Lab learning path](extension-learning-path.md) | Five optional Labs for mechanism comparison, realistic faults, and performance degradation | Proposed |

## Registry

No executable Labs have been accepted yet.

| Lab | Question | Related concept | Status | Evidence |
| --- | --- | --- | --- | --- |
| [01 — Race Condition／Overselling](curriculum-blueprint.md) | Can concurrent orders oversell the final item? | Atomic conditional update | Proposed | Profile C; executable evidence pending |
| [02 — Lost Update](curriculum-blueprint.md) | Do all accepted increments survive concurrent writes? | Lost-update prevention | Proposed | Profile C; executable evidence pending |
| [03 — Isolation](curriculum-blueprint.md) | Do two reads belong to one explicit snapshot? | Transaction isolation | Proposed | Profile C; executable evidence pending |
| [04 — Write Skew](curriculum-blueprint.md) | Can disjoint row updates break a cross-row constraint? | Serializable transactions | Proposed | Profile C; executable evidence pending |
| [05 — HTTP Idempotent Command](curriculum-blueprint.md) | Does a retried logical command create one effect and result? | Idempotency keys | Proposed | Profile M; executable evidence pending |
| [06 — MQ ACK／Redelivery](curriculum-blueprint.md) | Where must ACK occur to avoid permanent message loss? | At-least-once delivery | Proposed | Profile M; executable evidence pending |
| [07 — Inbox](curriculum-blueprint.md) | Can redelivery avoid a duplicate business effect? | Transactional deduplication | Proposed | Profile M; executable evidence pending |
| [08 — Transactional Outbox](curriculum-blueprint.md) | Can business state and event intent survive a dual-write crash? | Transactional Outbox | Proposed | Profile M; executable evidence pending |
| [09 — Saga／Compensation](curriculum-blueprint.md) | Can a partial multi-service workflow reach an auditable final state? | Durable workflow compensation | Proposed | Profile M; executable evidence pending |
| [10 — Cache Consistency](curriculum-blueprint.md) | Can a version-fenced read reject a stale cache refill? | Derived-state consistency | Proposed | Profile D; executable evidence pending |
| [11 — Replication Lag](curriculum-blueprint.md) | Can a session preserve read-your-writes on an async standby? | Replication lag | Proposed | Profile R; executable evidence pending |
| [12 — Sharding Routing](curriculum-blueprint.md) | Do all API processes route one tenant to one shard? | Stable hash routing | Proposed | Profile D; executable evidence pending |
| [13 — Hot Partition](curriculum-blueprint.md) | Can salting reduce skew while preserving the aggregate? | Hot-spot relief | Proposed | Profile P; executable evidence pending |
| [14 — Distributed Lease](curriculum-blueprint.md) | Can an expired owner avoid deleting a new owner's lease? | Lease ownership | Proposed | Profile C; executable evidence pending |
| [15 — Fencing Token](curriculum-blueprint.md) | Can the resource reject a resumed stale writer? | Resource-side fencing | Proposed | Profile C; executable evidence pending |
| [16 — Event Sourcing](curriculum-blueprint.md) | Does replay rebuild the same state as the live projection? | Event sourcing | Proposed | Profile D; executable evidence pending |
| [17 — Event／Schema Evolution](curriculum-blueprint.md) | Can old and new producers and consumers coexist? | Schema compatibility | Proposed | Profile D; executable evidence pending |
| [18 — CDC Recovery](curriculum-blueprint.md) | Does restart preserve every committed source change? | Change Data Capture | Proposed | Profile X; executable evidence pending |
| [19 — Stream Restart Correctness](curriculum-blueprint.md) | Can restart avoid applying one input twice? | Atomic checkpoint/state/output | Proposed | Profile X; executable evidence pending |
| [20 — Event Time／Out-of-order](curriculum-blueprint.md) | Are bounded-late events classified into the correct window? | Watermarks and event time | Proposed | Profile S; executable evidence pending |
| [E01 — Serializable vs Explicit Locking](curriculum-blueprint.md) | Can explicit locking reduce retry amplification under fixed contention? | Concurrency-control comparison | Proposed | Profile P; executable evidence pending |
| [E02 — Cache Stampede at a TTL Cliff](curriculum-blueprint.md) | Can single-flight bound origin amplification at expiry? | Cache stampede | Proposed | Profile P; executable evidence pending |
| [E03 — Synchronous Replication under Primary Loss](curriculum-blueprint.md) | Do all acknowledged writes survive abrupt primary loss? | Synchronous durability | Proposed | Profile R; executable evidence pending |
| [E04 — Outbox Relay: Polling vs CDC](curriculum-blueprint.md) | Can CDC recover and meet a latency budget that polling misses? | Relay comparison | Proposed | Profile X + P; executable evidence pending |
| [E05 — Consumer-group Rebalance Fencing](curriculum-blueprint.md) | Can a new assignment epoch reject the old partition owner? | Ownership fencing | Proposed | Profile S; executable evidence pending |

## Lab rules

Every Lab page must record:

- one main question, a falsifiable hypothesis, and non-goals;
- variables, workload, environment, measurements, and expected observations;
- reproduction and cleanup commands;
- facts, inferences, open questions, and known confounders;
- evidence links and the exact scope of its conclusion.

Use the [Lab template](../templates/lab.md) and the shared [experiment architecture](../architecture/experiment-architecture.md).
