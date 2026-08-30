# Curriculum Blueprint

## Status

Proposed. This page is the accepted implementation-ready curriculum design for 20 Core Labs and five Extension Labs. It settles each Lab's question, executable invariant, Broken／Correct boundary, deterministic workload or fault, evidence profile, minimum technology, prerequisites, and limits.

There is no executable Lab evidence yet. The packets below are canonical planning records, not claims that the mechanisms, timing gates, line budgets, or teaching sequence have passed locally. All remaining uncertainty is implementation-stage validation; there is no unresolved curriculum-level design choice.

## 30-second overview

| ID | Question | Invariant | Broken → Correct | Profile | Tech | Prerequisites |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Can two orders oversell the last unit? | Stock equals initial minus accepted quantity and never falls below zero. | Check-then-act → conditional atomic update. | C | .NET, PostgreSQL | — |
| 02 | Can two accepted increments collapse into one? | Final value equals initial value plus accepted increments. | Read/overwrite → in-database atomic increment. | C | .NET, PostgreSQL | 01 |
| 03 | Do two report reads use one stable snapshot? | First and second read in the report transaction are equal. | Read Committed → Repeatable Read. | C | .NET, PostgreSQL | 02 |
| 04 | Can disjoint row updates violate a cross-row constraint? | At least one doctor remains on call. | Repeatable Read write skew → Serializable plus full-transaction retry. | C | .NET, PostgreSQL | 03 |
| 05 | Does retrying one logical POST duplicate its effect? | One key creates one payment and returns one stored result. | Unkeyed POST → transactional idempotency record and result replay. | M | .NET, PostgreSQL | 02 |
| 06 | Can an acknowledged broker message be lost on consumer crash? | Every publisher-confirmed message has at least one durable effect after recovery. | ACK before effect → ACK after durable effect. | M | .NET, PostgreSQL, RabbitMQ | 05 |
| 07 | Can redelivery apply the same business effect twice? | One message ID commits exactly one effect. | Unprotected consumer → transactional Inbox deduplication. | M | .NET, PostgreSQL, RabbitMQ | 02, 06 |
| 08 | Can a committed business row lose its outbound event intent? | Order existence equals outbox-intent existence; committed intent is eventually observed. | DB/broker dual write → transactional outbox plus retrying relay. | M | .NET, PostgreSQL, RabbitMQ | 06, 07 |
| 09 | Can a two-service workflow remain permanently half-complete? | Saga ends Completed or Compensated with participant states aligned. | Direct calls → durable saga state and idempotent compensation. | M | .NET, two PostgreSQL nodes | 05, 07, 08 |
| 10 | Can a stale cache refill defeat a completed write? | A read carrying minimum version v returns version at least v. | Unfenced cache hit → version-fenced read and refresh. | D | .NET, PostgreSQL, Redis | 03 |
| 11 | Can an immediate replica read miss the session's write? | Returned row meets the write version; replica reads require replay LSN at least the token. | Unconditional standby read → LSN wait or primary fallback. | R | .NET, PostgreSQL primary/standby | 03, 10 |
| 12 | Can two processes route one tenant to different shards? | Every process resolves the tenant to one identical physical shard. | Process-local hash salt → stable hash and explicit shard map. | D | .NET, two PostgreSQL shards | 02 |
| 13 | Can salting relieve a correctly routed hot tenant? | Aggregate is exact and busiest-shard share is at most 35%. | Tenant-only key → deterministic buckets plus read fan-in. | P | .NET, four PostgreSQL shards, k6 | 12 |
| 14 | Can an expired owner delete a new owner's lease? | A release with a different token cannot change the lease. | Unconditional delete → compare-token-and-delete. | C | .NET, Redis | 06, 11 |
| 15 | Can a paused former owner overwrite the new owner? | Accepted fencing tokens never decrease; older writes are rejected. | Resource ignores token → resource-side conditional write. | C | .NET, Redis, PostgreSQL | 14 |
| 16 | Can current state be rebuilt exactly from history? | Live, folded, and rebuilt projection digests are equal. | Current-state overwrite → append-only events and deterministic fold. | D | .NET, PostgreSQL | 02, 08 |
| 17 | Do old/new producers and consumers coexist safely? | All four compatibility cells decode the same domain meaning. | Destructive rename → additive optional field and tolerant reader. | D | .NET | 16 |
| 18 | Does capture restart omit a committed row version? | Every committed row version is eventually observed; duplicates are allowed. | Timestamp polling → WAL/LSN CDC recovery. | X | .NET, PostgreSQL, Kafka, Debezium | 08, 17 |
| 19 | Does processor restart double-apply a Kafka record? | One durable output per source coordinate and state equals inputs through DB checkpoint. | Split effect/checkpoint commits → atomic PostgreSQL checkpoint, state, and output. | X | .NET, PostgreSQL, Kafka | 07, 18 |
| 20 | Are out-of-order events assigned and closed by event time? | Within-bound events enter the proper window; post-close events are recorded late. | Arrival-time windows → watermark, grace, and late-event record. | S | .NET, PostgreSQL, Kafka | 19 |
| E01 | Under contention, can ordered locks meet a budget that bounded Serializable retry does not? | Capacity, reservation count, retry, and p99 compound predicate holds. | Serializable retry → ordered explicit row locks. | P | .NET, PostgreSQL, k6 | 03, 04 |
| E02 | Can single-flight prevent a TTL-cliff stampede? | Correct version; at most one origin fetch and one origin request in flight per generation. | Independent cache fills → per-key single-flight. | P | .NET, PostgreSQL, Redis, k6 | 10 |
| E03 | Does synchronous commit retain every acknowledged write after primary loss? | Acknowledged ID set is a subset of promoted-standby data. | Local/asynchronous acknowledgement → synchronous standby acknowledgement. | R + fault | .NET, PostgreSQL primary/standby, netem | 11 |
| E04 | Can CDC meet recovery and latency budgets that polling cannot? | All committed outbox IDs appear within the declared bound; no unknown IDs. | Fixed-interval polling relay → WAL/LSN CDC relay. | X + fault; P modifier | .NET, PostgreSQL, Kafka, Debezium | 08, 18 |
| E05 | Can a rebalance fence a paused former partition owner? | Accepted commit epoch equals current assignment epoch. | Unchecked delayed handler → resource-side assignment-epoch check. | S + fault | .NET, PostgreSQL, Kafka | 15, 19 |

## Shared implementation contract

Every Lab implements the repository's [experiment architecture](../architecture/experiment-architecture.md) within its own boundary:

~~~text
experiments/<lab-id>/
├─ <lab-id>.slnx
├─ compose.yaml
├─ lab.sh
├─ README.md
├─ src/
├─ tests/
├─ fixtures/
└─ results/
   └─ accepted.json
~~~

Create only directories that the Lab actually needs. Each Lab owns its solution, dependency graph, Compose project, database or broker resources, fixture, evidence, and bounded cleanup. Runtime libraries, migrations, domain models, correctness helpers, and stateful services are not shared across Labs.

Broken and Correct together expose one to three application APIs and target 100–300 lines of handwritten core mechanism code. Fewer than 100 lines is acceptable when the question is already clear; exceeding 300 lines requires a documented split check. Infrastructure, tests, fixtures, generated metadata, comments, imports, and blank lines do not count toward this target.

The exact per-Lab entry points are:

~~~text
./lab <id> setup
./lab <id> broken
./lab <id> correct
./lab <id> inspect
./lab <id> check
./lab <id> cleanup
~~~

The root dispatcher only validates the Lab ID/action and delegates to that Lab's `lab.sh`. The only aggregate form is `./lab all check`; full profile proofs remain per-Lab.

Broken and Correct must receive the same dataset, input IDs, seed, concurrency, request shape, connection topology, schedule, delay, crash point, and stop condition. The packet's named correctness mechanism is the only changed variable. If a required barrier, broker state, replica state, reassignment, connector readiness, or fault point is not observed, the result is Invalid rather than a pass or failure.

Every Lab follows the [evidence matrix](../qa/evidence-matrix.md). A process exit code is not evidence: verification directly evaluates the invariant and retains the decisive rows, counts, tokens, offsets, epochs, timings, or state transitions. An accepted run writes a small `results/accepted.json` containing at least schema version, Lab ID, commit, timestamp, verdict, profile, exact commands, environment and image versions/digests, fixture hash, seed, concurrency, run deadlines, fault point, observations, per-run results, anomalies, confounders, and regeneration instructions. Accepted proofs never auto-retry.

All stateful dependencies run locally under that Lab's digest-pinned Compose project, named `ddia-lab-<id>`. Setup and cleanup must be rerunnable and bounded to that project. Labs use synthetic data, no production credentials, no hidden interactive state, and no destructive command outside their own named resources. A Lab may use several nodes of one stateful system or at most two stateful-system types when its question requires them.

This blueprint remains the curriculum-level planning canonical. When implementation starts, create an independent canonical page in `wiki/labs/` for that Lab. The per-Lab page owns actual commands, watched paths, retained evidence, result interpretation, and status transitions from Proposed through Pending／Partial／Verified or Outdated. It links back here and records any evidence-driven departure; the implementation must not silently rewrite this curriculum packet.

## Evidence labels

- **Verified fact** is reserved for a cited primary-source/product semantic, an accepted repository decision, or reproducible repository evidence. It does not mean the planned local Lab has passed.
- **Reasonable inference** marks the selected scenario, API, threshold, fault schedule, technology fit, line budget, or expected observation when it follows from the sources but lacks executable evidence.
- **Open at implementation** names only operational validation still required: deterministic control, dependency compatibility, reference-runner stability, numeric-gate separation, cleanup, and retained proof. It is not an unresolved curriculum question.
- A successful future run may upgrade only the exact scoped claim it proves. Performance observations remain bound to their workload and reference runner.

## Evidence and sources

- Canonical Core order and prerequisite DAG: [Core Lab learning path](core-learning-path.md).
- Canonical optional portfolio and escalation boundary: [Extension Lab learning path](extension-learning-path.md).
- Profiles, gates, flaky policy, and retained-result contract: [Lab evidence matrix](../qa/evidence-matrix.md).
- Per-Lab execution and repository boundary: [Experiment architecture](../architecture/experiment-architecture.md).
- DDIA and primary-source concept anchors: [DDIA concept anchors and Core Lab candidates](../../.scratch/ddia-labs-learning-roadmap/research/01-ddia-concept-anchors.md).
- Audited runtime and optional-tool baseline: [Technology baseline for reproducible DDIA Labs](../../.scratch/ddia-labs-learning-roadmap/research/02-technology-baseline.md).
- Planning record that assembled this accepted design: [Assemble the implementation-ready curriculum blueprint](../../.scratch/ddia-labs-learning-roadmap/issues/08-assemble-the-implementation-ready-blueprint.md).

## Implementation packets

## Phase A — Transactions (01–04)

### 01 — Race Condition／Overselling

| Field | Decision |
| --- | --- |
| Problem | 兩張訂單同時搶最後一件庫存時，如何避免非原子 check-then-act 讓兩張都成功？Slug：`01-race-condition`；目標核心行數 130–190。 |
| Invariant | `stock = initial_stock - SUM(accepted_order.qty) AND stock >= 0`；fixture 的 `initial_stock=1`。 |
| Data & API | `inventory(sku PK, stock int)`、`orders(order_id PK, sku, qty)`；`POST /broken/orders`、`POST /correct/orders`、`GET /inventory/{sku}`。 |
| Broken → Correct | Broken 在 Read Committed transaction 先 `SELECT stock`，應用端判斷後無條件扣庫存並新增 order。Correct 的唯一變因是改為同 transaction 的 `UPDATE ... SET stock=stock-qty WHERE stock>=qty RETURNING`；affected row=1 才新增 order，否則 409。 |
| Reproduce | `sku=book, stock=1`，兩個不同 order ID 各買 1；seed `1001`、concurrency `2`。同一 start gate；Broken 在兩邊完成 `SELECT` 後放行，Correct 在兩邊抵達 conditional update 前放行。 |
| Proof | Broken 預期兩筆成功、`stock=-1`；Correct 一筆成功、一筆 409、`stock=0`。直接執行 invariant query。Profile `C`：5/5 vs 25/25，60 秒／10 分鐘。 |
| Tech & prerequisites | .NET 10 Minimal API、PostgreSQL 18；Compose `ddia-lab-01`；無前置 Lab。 |
| Limits | 不研究 lost update、isolation 比較、idempotency 或效能。每 request 必須用獨立 DB connection；ORM tracking 或共享 transaction 造成的序列化是 confounder。 |
| Evidence strength | **Verified source fact:** DDIA／PostgreSQL 來源支持並行 check-update 邊界。**Reasonable inference:** 超賣 fixture、API、SQL、barrier 與行數目標。**Implementation-stage open:** barrier 穩定性與 profile gate 尚未由 executable Lab 驗證；無剩餘概念決策。 |

### 02 — Lost Update

| Field | Decision |
| --- | --- |
| Problem | 兩個都被接受的 `+1` 為何只留下其中一個，如何讓每個 accepted increment 都反映在終值？Slug：`02-lost-update`；目標核心行數 100–150。 |
| Invariant | `counter.value = initial_value + accepted_increment_count`。 |
| Data & API | `counters(counter_id PK, value int)`；`POST /broken/counters/{id}/increment`、`POST /correct/counters/{id}/increment`、`GET /counters/{id}`。 |
| Broken → Correct | Broken 讀 value、在應用程式算 `value+1`、再以絕對值覆寫。Correct 的唯一變因是改為 `UPDATE counters SET value=value+1`；不改 isolation、fixture 或 request shape。 |
| Reproduce | counter 初值 0，兩個 `+1`；seed `2001`、concurrency `2`。Broken 的 `read-complete` barrier 保證兩邊都讀到 0；Correct 使用相同 start gate，在兩邊進入 atomic update 前一起放行。 |
| Proof | Broken 兩個 HTTP success、終值 1；Correct 兩個 success、終值 2。以 accepted response count 與 DB value 直接計算 predicate。Profile `C`：5/5 vs 25/25，60 秒／10 分鐘。 |
| Tech & prerequisites | .NET 10、PostgreSQL 18；Compose `ddia-lab-02`；前置 01。 |
| Limits | 不比較 CAS、retry 策略或 isolation；不研究跨列 constraint。每 request 必須使用獨立 connection。 |
| Evidence strength | **Verified source fact:** DDIA 直接涵蓋 lost update；PostgreSQL 來源支持原子 DML。**Reasonable inference:** counter fixture、API 與單列 SQL。**Implementation-stage open:** driver interleaving、行數與 gate 尚待執行確認。 |

### 03 — Isolation／Stable Snapshot

| Field | Decision |
| --- | --- |
| Problem | 一個宣稱使用同一快照的 report transaction，在 concurrent commit 發生時能否讓兩次讀取一致？Slug：`03-isolation`；目標核心行數 110–170。 |
| Invariant | 在 writer 已於兩次讀取間提交的 controlled schedule 下，`report.first_balance = report.second_balance`。 |
| Data & API | `accounts(account_id PK, balance int)`；`GET /broken/reports/{accountId}`、`GET /correct/reports/{accountId}`、`GET /accounts/{accountId}`。writer 由 harness 直接執行，不增加 API。 |
| Broken → Correct | Broken 使用顯式 Read Committed transaction。Correct 的唯一變因是改成 Repeatable Read；SQL、資料與排程不變。 |
| Reproduce | balance=100；一 reader、一 writer，writer `+50`；seed `3001`、concurrency `2`。`first-read-complete` barrier：reader 第一次讀後放行 writer，確認 writer commit 才讓第二次讀。 |
| Proof | Broken report=`100/150`；Correct report=`100/100`，同時 DB 最終值仍是 150，以證明 writer 確實提交。Profile `C`：5/5 vs 25/25，60 秒／10 分鐘。 |
| Tech & prerequisites | .NET 10、PostgreSQL 18；Compose `ddia-lab-03`；前置 02。 |
| Limits | 不研究 write skew、Serializable、cache 或 replica。兩次 SELECT 必須在同一顯式 transaction；autocommit 結果為 Invalid evidence。 |
| Evidence strength | **Verified source fact:** PostgreSQL 明載 Read Committed 可 nonrepeatable read、Repeatable Read 不允許。**Reasonable inference:** 單列 report fixture、API 與 barrier。**Implementation-stage open:** in-process barrier 與外部 reproduction 的穩定性仍待首個 run 驗證。 |

### 04 — Write Skew

| Field | Decision |
| --- | --- |
| Problem | 兩個 transaction 更新不同列時，Repeatable Read 為何仍可能破壞「至少一人值班」？Slug：`04-write-skew`；目標核心行數 150–230。 |
| Invariant | `SELECT COUNT(*) FROM doctors WHERE on_call = true >= 1`。 |
| Data & API | `doctors(doctor_id PK, on_call boolean)`；`POST /broken/doctors/{id}/leave`、`POST /correct/doctors/{id}/leave`、`GET /on-call`。 |
| Broken → Correct | Broken 的兩個 Repeatable Read transaction 都讀到 count=2，各自更新不同 doctor。Correct 的唯一 correctness mechanism 是 PostgreSQL Serializable + `40001` 時以 fresh transaction 完整重跑，最多 3 attempts。 |
| Reproduce | doctors A/B 均 on-call，兩人同時請假；seed `4001`、concurrency `2`。首次 attempt 在讀完 predicate 後進入 `predicate-read` barrier；retry 不再等待 barrier。 |
| Proof | Broken 兩個 accepted、on-call=0；Correct 一個 accepted，另一個 serialization retry 後因只剩一人被拒、on-call=1。Profile `C`：5/5 vs 25/25，60 秒／10 分鐘。 |
| Tech & prerequisites | .NET 10、PostgreSQL 18；Compose `ddia-lab-04`；前置 03。 |
| Limits | 不研究同列 lost update、deadlock tuning 或 Serializable 效能。只 retry 最後一條 UPDATE 不算完整 transaction retry。 |
| Evidence strength | **Verified source fact:** DDIA 直接涵蓋 write skew／SSI；PostgreSQL 要求 serialization failure 後重試完整 transaction。**Reasonable inference:** 醫師 fixture、3-attempt ceiling、API 與 barrier。**Implementation-stage open:** serialization victim 順序可變，但 invariant 與 gate 必須由 executable proof 驗證。 |

## Phase B — Retry and messaging (05–09)

### 05 — HTTP Idempotent Command

| Field | Decision |
| --- | --- |
| Problem | payment 已 commit、response 卻逾時時，同一 logical POST 重送如何只產生一個 effect 並回傳相同結果？Slug：`05-http-idempotency`；目標核心行數 180–260。 |
| Invariant | 對 key `K`：`COUNT(payments WHERE command_key=K)=1 AND COUNT(DISTINCT successful_response.payment_id)=1`；同 key 不同 request hash 必須 409。 |
| Data & API | `payments(payment_id PK, command_key, amount_cents, currency)`；`idempotency_records(key PK, request_hash, payment_id, status_code, response_json)`；`POST /broken/payments`、`POST /correct/payments`、`GET /payments/by-command/{key}`。 |
| Broken → Correct | Broken 每次 POST 都建立 payment。Correct 的唯一 mechanism 是 effect 與 idempotency record／stored response 放在同一 transaction；相同 key+hash 重播保存結果，不同 hash 回 409。 |
| Reproduce | key=`pay-5001`、amount=1000、currency=TWD；seed `5001`、logical concurrency `1`、3 attempts。第一次 commit 後停在 `after-commit-before-response`，client 100ms timeout；確認 commit 後放行，再送兩次相同 request。 |
| Proof | Broken 3 個 payment，後兩個 response ID 不同；Correct 1 個 payment、1 筆 record，後兩次 status／body 相同；另驗證同 key 異參數為 409。Profile `M`：5/5 vs 20/20，90 秒／15 分鐘。 |
| Tech & prerequisites | .NET 10 Minimal API、PostgreSQL 18；Compose `ddia-lab-05`；前置 02。 |
| Limits | 不研究 broker redelivery、key expiry、多區域一致性或 payment provider。timeout 必須在 DB commit 後；若 cancellation 導致 rollback，結果為 Invalid。 |
| Evidence strength | **Verified source fact:** RFC 定義 HTTP idempotency 語義；一手 API 文件支持 POST idempotency-key／stored result 模式。**Reasonable inference:** payment schema、100ms fault plan、API 與 409 contract。**Implementation-stage open:** ASP.NET cancellation／response delay 的精確控制與 `M` gate 尚待執行驗證。 |

### 06 — MQ ACK／Redelivery

| Field | Decision |
| --- | --- |
| Problem | broker 已接受的訊息，在 consumer crash 後如何不永久遺失；代價是否是可能重送？Slug：`06-mq-ack-redelivery`；目標核心行數 180–270。 |
| Invariant | `publisher_confirmed(message_id) => COUNT(durable_effects WHERE message_id) >= 1`，須在 recovery deadline 內成立。 |
| Data & API | `effects(effect_id PK, message_id, recorded_at)`；`message_id` 故意不 unique；RabbitMQ durable queue。`POST /commands`、`GET /effects/{messageId}`；consumer variant 由 `lab.sh` 選擇。 |
| Broken → Correct | Broken 先 ACK，再 commit PostgreSQL effect。Correct 的唯一變因是將順序改為 durable effect commit 後才 ACK；其他 message、queue、consumer 與 fault harness 不變。 |
| Reproduce | message=`m-6001`；seed `6001`、publisher=1、consumer concurrency=1、prefetch=1。故障點都是「第一步完成、第二步之前」：Broken 等 broker ready=0/unacked=0，Correct 等 DB effect=1 且 broker unacked=1，再 kill worker；以 fault-disabled worker restart。 |
| Proof | Broken 有 publisher confirm、queue 已空，restart 後 effect=0；Correct redelivery 後 effect=2、queue drained。duplicate 是預期限制，不是 violation。Profile `M`：5/5 vs 20/20，90 秒／15 分鐘。 |
| Tech & prerequisites | .NET 10 API + 獨立 consumer、PostgreSQL 18、RabbitMQ 4.3.5 management image；Compose `ddia-lab-06`；前置 05。 |
| Limits | 不解決 duplicate effect（Lab 07）、producer dual write（Lab 08）或 broker HA。kill 前必須由 RabbitMQ management state 證明 ACK／unacked 狀態；worker log 不足。 |
| Evidence strength | **Verified source fact:** RabbitMQ 一手文件支持 ACK、at-least-once 與 failure 時 redelivery。**Reasonable inference:** effect fixture、API、variant startup 與 broker-state barrier。**Implementation-stage open:** ACK frame 的可控觀察與 restart timing 必須由 Compose proof 驗證。 |

### 07 — Inbox Deduplication

| Field | Decision |
| --- | --- |
| Problem | effect 已 commit、ACK 前 consumer crash，重送同一 message 時如何避免第二次 business effect？Slug：`07-inbox`；目標核心行數 190–280。 |
| Invariant | 對每個 `message_id`：`COUNT(effect_applications)=1`，且 `account.balance = initial_balance + SUM(distinct_message_amount)`。 |
| Data & API | `accounts(account_id PK, balance)`、`effect_applications(id PK, message_id, account_id, amount)`、`processed_messages(message_id PK, processed_at)`；`POST /commands`、`GET /accounts/{accountId}`；consumer variant 由 `lab.sh` 選擇。 |
| Broken → Correct | Broken transaction 更新 balance 並新增 application，commit 後才 ACK。Correct 的唯一 mechanism 是同 transaction 先 `INSERT processed_messages ... ON CONFLICT DO NOTHING`；只有新 message 才做 effect，duplicate 直接 ACK。 |
| Reproduce | account A balance=0；message=`m-7001`, amount=10；seed `7001`、consumer concurrency=1、prefetch=1。兩 variant 都在 DB commit 後、ACK 前停住；確認 effect=1 且 broker unacked=1 後 kill，restart 時停用一次性 fault。 |
| Proof | Broken 兩筆 application、balance=20；Correct 一筆 processed、一筆 application、balance=10，broker drained。Profile `M`：5/5 vs 20/20，90 秒／15 分鐘。 |
| Tech & prerequisites | .NET 10 API + consumer、PostgreSQL 18、RabbitMQ；Compose `ddia-lab-07`；前置 02、06。 |
| Limits | ACK ordering 固定為 effect 後 ACK，不重做 Lab 06；不研究 producer outbox、poison message 或 ordering。crash 只可由第一個 delivery 觸發。 |
| Evidence strength | **Verified source fact:** RabbitMQ 支持 redelivery；一手 Inbox／Outbox 文件支持 message ID 與 business effect 同 transaction 去重。**Reasonable inference:** balance fixture、schema、API 與 crash schedule。**Implementation-stage open:** kill/restart 是否穩定落在同一 boundary 與 `M` gate 尚待驗證。 |

### 08 — Transactional Outbox

| Field | Decision |
| --- | --- |
| Problem | order DB commit 與 broker publish 之間 crash 時，如何讓 committed order 的事件意圖仍可恢復並至少投遞一次？Slug：`08-transactional-outbox`；目標核心行數 220–300。 |
| Invariant | 對 fixture order：`order_exists = outbox_intent_exists`；若存在，deadline 內 `matching_broker_event_count >= 1`；observed event 必須對應存在的 order。 |
| Data & API | `orders(order_id PK, total, status)`；`outbox(event_id PK, aggregate_id UNIQUE, event_type, payload, created_at, published_at NULL)`；RabbitMQ durable queue。`POST /broken/orders`、`POST /correct/orders`、`GET /orders/{orderId}/publication`。 |
| Broken → Correct | Broken transaction 只 commit order，之後由 handler 直接 publish。Correct 的唯一 mechanism 是 order+outbox row 同一 DB transaction，單一 relay 讀 unpublished row，publisher confirm 後才填 `published_at`。 |
| Reproduce | order=`o-8001`；seed `8001`、request concurrency=1、relay concurrency=1。兩 variant 都在 order transaction commit 後、任何 publish 前執行一次性 process crash；確認 container exit 後以 fault-disabled 設定 restart。 |
| Proof | Broken：order=true、outbox=false、event=0；Correct：order=true、outbox=published、matching event≥1。不得要求 exactly once。Profile `M`：5/5 vs 20/20，90 秒／15 分鐘。 |
| Tech & prerequisites | .NET 10 API + hosted relay、PostgreSQL 18、RabbitMQ；Compose `ddia-lab-08`；前置 06、07。 |
| Limits | 不研究 publish-first ghost、relay 在 confirm 後／mark 前 crash、consumer dedup 或 CDC。faulted process crash 前 relay 不得先 publish；publisher confirm 是必要 observation。 |
| Evidence strength | **Verified source fact:** AWS／Debezium 一手文件支持 dual-write、transactional outbox 與可能 duplicate。**Reasonable inference:** order fixture、single relay、API 與 crash point。**Implementation-stage open:** restart wake-up、publisher confirm、300 行上限與 `M` gate 尚待驗證。 |

### 09 — Saga／Compensation

| Field | Decision |
| --- | --- |
| Problem | 第一個 local transaction 已成功、第二個 participant 明確失敗時，如何避免永久留下未記錄的半完成？Slug：`09-saga-compensation`；目標核心行數 220–300。 |
| Invariant | 對 attempted `saga_id`：`state IN ('Completed','Compensated') AND (active_reservation = charged_payment)`；Completed 時兩者 true，Compensated 時兩者 false。 |
| Data & API | DB A：`inventory(sku PK, available)`、`reservations(saga_id PK, sku, qty, status)`、`sagas(saga_id PK, state, last_error)`；DB B：`payments(saga_id PK, amount, status)`。`POST /broken/checkouts`、`POST /correct/checkouts`、`GET /checkouts/{sagaId}`。 |
| Broken → Correct | Broken 在 DB A 扣庫存並建立 active reservation，payment step 失敗後直接回錯。Correct 的唯一 mechanism 是 durable saga state machine：保存 state、以 saga ID 執行冪等 local step；payment decline 後 conditional release，再保存 `Compensated`。 |
| Reproduce | sku=book、available=1、saga=`s-9001`、qty=1；seed `9001`、concurrency=1。barrier 確認 reservation commit 後，payment adapter 對該 saga 固定回 `DECLINED`，不使用 timeout 或隨機網路錯誤。 |
| Proof | Broken：available=0、reservation=Reserved、payment absent、無 final saga state。Correct：available=1、reservation=Released、payment absent、state=Compensated；重複 compensation 不再增加庫存。Profile `M`：5/5 vs 20/20，90 秒／15 分鐘。 |
| Tech & prerequisites | .NET 10 coordinator、兩個獨立 PostgreSQL 18 containers／local transaction boundaries；Compose `ddia-lab-09`；前置 05、07、08；禁止 ambient `TransactionScope` 或 distributed transaction。 |
| Limits | 不比較 orchestration／choreography，不研究 compensation 自身失敗、coordinator crash recovery、Outbox transport 或通用 rollback。若意外升級為跨 DB transaction，結果為 Invalid。 |
| Evidence strength | **Verified source fact:** Azure 一手文件支持 Saga 的 local transactions、durable workflow 與可能失敗的 idempotent compensation。**Reasonable inference:** reservation/payment fixture、兩 DB 簡化、API 與 state predicate。**Implementation-stage open:** state transitions、line budget 與 `M` gate 尚待實作驗證；無剩餘概念決策。 |

## Phase C — Distributed reads and placement (10–13)

### 10 — Cache Read Fence

| Field | Decision |
| --- | --- |
| Problem | A cache-miss reader loads DB v1, a writer commits v2 and invalidates, then the old reader refills v1. Can a session holding the completed-write token avoid reading an older value? Slug: `10-cache-consistency`. |
| Invariant | `Read(itemId, minVersion=v).version >= v` for every completed write that returned `v`. |
| Data & API | PostgreSQL `items(id,value,version)`; Redis `item:{id} -> {value,version}`.<br>1. `PUT /items/{id}` returns version. 2. `GET /broken/items/{id}?minVersion=`. 3. `GET /correct/items/{id}?minVersion=`. |
| Broken → Correct | Broken accepts every cache hit and ignores `minVersion`. Correct changes only the read policy: reject cache entries below `minVersion`, read DB, then version-aware compare-set the refreshed value. Write/invalidate behavior is identical. |
| Reproduce | Fixture `cache-refill-v1`, DB/cache v1, concurrency 2. Pause reader at `after-db-read-before-cache-set`; writer commits v2 and invalidates; resume stale v1 refill; read with `minVersion=2`. |
| Proof | Profile D: Broken 3/3 returns v1; Correct 10/10 returns version >=2. Directly assert response version, DB version, and retained cache version; 30 s/run, 5 min proof. |
| Tech & prerequisites | .NET 10, PostgreSQL 18, Redis; Core 03; estimated 180–240 core LOC. |
| Limits | Not TTL stampede (E02), replica lag (11), or general multi-writer cache coherence. Missing the named barrier makes the run Invalid. |
| Evidence strength | Cache-aside limitation is Verified source fact; version-fence design is Reasonable inference; executable result remains Open. |

### 11 — Read-your-writes on a Physical Replica

| Field | Decision |
| --- | --- |
| Problem | A primary write has committed, but the same session is immediately routed to an asynchronous hot standby. How can the read avoid returning the pre-write row? Slug: `11-replication-lag`. |
| Invariant | `response.row_version >= write.row_version`; if `response.source == replica`, also require `replica_replay_lsn >= min_lsn`, otherwise the source must be primary fallback. |
| Data & API | Physical primary/standby row `accounts(id,balance,row_version)`.<br>1. `PUT /accounts/{id}` commits on primary and returns row version plus post-commit `pg_current_wal_flush_lsn()`. 2. `GET /broken/accounts/{id}`. 3. `GET /correct/accounts/{id}?minLsn=`. |
| Broken → Correct | Broken always reads standby. Correct changes only routing: bounded-poll `pg_last_wal_replay_lsn()` against `minLsn`; if deadline expires, read primary. |
| Reproduce | Real PostgreSQL 18 physical streaming replica. Seed v1 and await catch-up. Run `pg_wal_replay_pause()` and wait until `pg_get_wal_replay_pause_state()='paused'`. Commit v2 on primary and capture flush LSN. Wait until standby `receive_lsn >= token` while `replay_lsn < token`, proving WAL arrived but was not applied. Broken then reads v1; Correct falls back to primary. Always resume replay in bounded cleanup. |
| Proof | Profile R: Broken 3/3 stale; Correct 10/10 no stale. Retain token, receive LSN, replay LSN, row versions, and chosen source; 180 s/run, 20 min proof. |
| Tech & prerequisites | .NET 10, two PostgreSQL 18 containers of the same stateful type; Core 03 and 10; estimated 180–250 core LOC. |
| Limits | Does not measure natural lag distribution or cover promotion, timeline change, synchronous replication, RPO, or RTO (E03). A replay-pause request not yet in `paused` state is Invalid. |
| Evidence strength | PostgreSQL async streaming/hot-standby/replay controls are Verified product facts; harness and fallback are Reasonable inference; local evidence remains Open. |

### 12 — Stable Cross-process Shard Routing

| Field | Decision |
| --- | --- |
| Problem | Can two API processes using a process-local hash salt route the same tenant to different physical shards? Slug: `12-sharding-routing`. |
| Invariant | `Route(instanceA,T) == Route(instanceB,T)` and `COUNT(DISTINCT shard containing T) == 1`. |
| Data & API | Two PostgreSQL shards, each `records(tenant_id,record_id,payload)`.<br>1. `POST /broken/tenants/{tenant}/records`. 2. `POST /correct/tenants/{tenant}/records`. 3. `GET /inspect/placements/{tenant}`. |
| Broken → Correct | Broken mixes a fixed per-process salt into an otherwise stable hash. Correct changes only the route function to `SHA-256(NFC UTF-8 tenantId)` with explicit byte order and fixed shard map. |
| Reproduce | Fixture `routing-v1`; two API containers with salts of opposite parity each write `tenant-007`. The deliberately fixed salts make split placement deterministic rather than relying on runtime hash randomness. |
| Proof | Profile D: Broken 3/3 places the tenant on two shards; Correct 10/10 gives identical routes and one physical shard; 30 s/run, 5 min proof. |
| Tech & prerequisites | .NET 10, two PostgreSQL 18 shard containers; Core 02; estimated 150–210 core LOC. |
| Limits | Not resharding, shard-count changes, hot partitioning (13), or cross-shard transactions. Inconsistent normalization/map versions invalidate the proof. |
| Evidence strength | Stable routing requirement is Verified concept; concrete hash/map is Reasonable inference; executable portability remains Open. |

### 13 — Salted Hot-key Placement

| Field | Decision |
| --- | --- |
| Problem | With correct routing but 95% of operations targeting one tenant, can salting a combinable counter reduce the busiest shard's share without changing the aggregate? Slug: `13-hot-partition`. |
| Invariant | `SUM(bucket.value) == COUNT(unique accepted op_id)` and `max(shard_accepted_ops) / total_accepted_ops <= 0.35`. |
| Data & API | Four PostgreSQL shards, each with `counter_buckets(tenant_id,bucket,value)` and `accepted_ops(op_id,tenant_id,bucket)`.<br>1. `POST /broken/counters/{tenant}/increment`. 2. `POST /correct/counters/{tenant}/increment`. 3. `GET /observations/{runId}`. |
| Broken → Correct | Broken routes solely by stable tenant key, concentrating the hot tenant on one shard/row. Correct changes only key construction: `bucket=op_sequence % 16`, mapped explicitly across four shards; reads fan in 16 buckets. |
| Reproduce | Fixture `hot-tenant-v1`: 16,000 unique operations, 95% `tenant-hot`, 5% across 20 fixed cold tenants, HTTP concurrency 64. Same operation order and IDs in paired variants. |
| Proof | Profile P: one warm-up plus five interleaved pairs. Broken `max_share >= 0.90` in >=4/5; Correct aggregate exact 5/5 and `max_share <= 0.35` in >=4/5. Primary metric `max_shard_share`: direction agrees >=4/5, median reduction >=20%, CV <=15% per variant. Throughput/p95 are non-gating observations; 5 min measured run, 45 min proof. |
| Tech & prerequisites | .NET 10, four PostgreSQL 18 shard containers, k6; Core 12; estimated 220–290 core LOC. |
| Limits | Scoped to commutative/associative counters, not arbitrary aggregates, resharding, or multi-key transactions. Any HTTP error or unequal accepted-op set invalidates a pair. |
| Evidence strength | Hot-spot concept is Verified; fixture and 35% gate are Reasonable defaults; runtime variability remains Open. |

## Phase D — Coordination safety (14–15)

### 14 — Token-safe Lease Release

| Field | Decision |
| --- | --- |
| Problem | After A's lease expires and B acquires a new lease, can A's delayed release delete B's ownership? Slug: `14-distributed-lease`. |
| Invariant | If `stored_token != releasing_token`, release must not change the lease key. |
| Data & API | Redis `lease:{resource} -> owner_token` with TTL.<br>1. `POST /leases/{resource}` shared `SET NX PX` acquire. 2. `DELETE /broken/leases/{resource}`. 3. `DELETE /correct/leases/{resource}`. |
| Broken → Correct | Both variants already use TTL and unique tokens. Broken release is unconditional `DEL`; Correct changes only release to atomic compare-token-and-delete Lua. |
| Reproduce | Two clients. A acquires and pauses before release; poll until Redis actually expires the key; B acquires token B; resume A release. Use a hard deadline, never a fixed sleep as the proof. |
| Proof | Profile C: Broken 5/5 deletes B; Correct 25/25 preserves B; 60 s/run, 10 min proof. |
| Tech & prerequisites | .NET 10, Redis; Core 06 and 11; estimated 120–170 core LOC. |
| Limits | Not stale resource writes (15), renewal, clock drift, Redis failover, or quorum locking. Failure to observe actual expiration is Invalid. |
| Evidence strength | TTL/token-safe release semantics are Verified product facts; interleaving is Reasonable inference; local timing evidence remains Open. |

### 15 — Resource-side Fencing Token

| Field | Decision |
| --- | --- |
| Problem | Even with a correct lease protocol, can a paused former owner resume and overwrite a newer owner's resource write? Slug: `15-fencing-token`. |
| Invariant | After resource accepts token `n`, every write with token `< n` is rejected and `last_fence` never decreases. |
| Data & API | Redis `lease:{resource}` and `fence_seq:{resource}`; PostgreSQL `resources(id,value,last_fence)` plus `write_attempts(resource_id,owner,fence,accepted)`.<br>1. `POST /leases/{resource}`. 2. `PUT /broken/resources/{id}`. 3. `PUT /correct/resources/{id}`. |
| Broken → Correct | Both variants receive monotonic fence tokens. Broken resource update ignores `last_fence`; Correct changes only resource SQL to `UPDATE ... WHERE last_fence < incoming_fence`, logging accept/reject in the same DB transaction. |
| Reproduce | A gets token 1 and pauses before resource write; its lease expires; B gets token 2 and writes B; A resumes and attempts A with token 1. Concurrency 2. |
| Proof | Profile C: Broken 5/5 ends at stale A/token1 or observes decreasing token; Correct 25/25 remains B/token2 and records A rejected; 60 s/run, 10 min proof. |
| Tech & prerequisites | .NET 10, Redis, PostgreSQL 18; Core 14; estimated 170–230 core LOC. |
| Limits | Lease release is a fixed prerequisite, not the subject. No Redis failover, multi-resource transaction, or token wraparound claim. |
| Evidence strength | Resource-side fencing is Verified concept; SQL predicate/fault is Reasonable inference; executable result remains Open. |

## Phase E — Immutable and derived data (16–20)

### 16 — Deterministic Event Replay

| Field | Decision |
| --- | --- |
| Problem | If current state is lost, can the retained history reproduce exactly the state observed during live processing? Slug: `16-event-sourcing`. |
| Invariant | `Digest(live_projection) == Digest(Fold(events ORDER BY sequence)) == Digest(rebuilt_projection)`. |
| Data & API | PostgreSQL `account_events(stream_id,sequence,event_id,type,amount)` and `account_projection(stream_id,balance,last_sequence)`.<br>1. `POST /broken/accounts/{id}/adjustments`. 2. `POST /correct/accounts/{id}/adjustments`. 3. `POST /accounts/{id}/rebuild?mode=`. |
| Broken → Correct | Broken updates current projection only, leaving the event table empty. Correct changes only persistence to append the event and apply the same deterministic fold in one transaction. |
| Reproduce | Fixture `event-history-v1`, one stream and ordered adjustments `[+100,-30,+10,-5]`. Record live digest, delete projection, rebuild; concurrency 1. |
| Proof | Profile D: Broken 3/3 rebuilds missing/zero state; Correct 10/10 live, folded, and rebuilt digests match, including a second replay; 30 s/run, 5 min proof. |
| Tech & prerequisites | .NET 10, PostgreSQL 18; Core 02 and 08; estimated 180–250 core LOC. |
| Limits | Not CQRS service separation, snapshots, cross-stream transactions, or schema evolution (17). Non-unique event order is Invalid. |
| Evidence strength | Append-only replay is Verified concept; account fixture is Reasonable inference; local replay evidence remains Open. |

### 17 — Mixed-version Schema Compatibility

| Field | Decision |
| --- | --- |
| Problem | During a rolling deployment, can old/new producer and consumer combinations decode the same domain meaning? Slug: `17-schema-evolution`. |
| Invariant | All four `{old,new producer} x {old,new consumer}` cells decode without exception and yield the expected domain amount. |
| Data & API | V1 JSON `{eventId,totalCents}`. Broken V2 `{eventId,amountMinor,currency:'USD'}`. Correct V2 retains `totalCents` and adds optional `currency:'USD'`; new reader defaults missing currency to USD.<br>1. `POST /broken/compatibility-check`. 2. `POST /correct/compatibility-check`. |
| Broken → Correct | Broken destructively renames `totalCents`; Correct changes only schema evolution strategy to additive optional field/default. Serializer settings and semantic assertions stay fixed. |
| Reproduce | Fixture `schema-matrix-v1`, four fixed producer/reader pairs, all scoped to USD; concurrency 1. |
| Proof | Profile D: Broken 3/3 has at least one decode failure or semantic zero; Correct 10/10 passes all four cells; 30 s/run, 5 min proof. |
| Tech & prerequisites | .NET 10/System.Text.Json only; Core 16; estimated 100–150 core LOC. |
| Limits | Does not claim old readers understand non-USD semantics; no registry, Avro/Protobuf, long migration chain, or CDC envelope. |
| Evidence strength | Mixed-version coexistence is Verified concept; JSON matrix is Reasonable scoped design; executable result remains Open. |

### 18 — CDC Restart from WAL Position

| Field | Decision |
| --- | --- |
| Problem | If the capture process is down while a row version commits, will restart eventually expose every committed version? Slug: `18-cdc-restart`. |
| Invariant | `ExpectedCommitted(order_id,version)` is a subset of `Observed(order_id,version)`. Duplicate delivery is allowed and counted; zero duplicates is not an invariant. |
| Data & API | PostgreSQL source `orders(id,status,version,updated_at)`; sink `observed_changes(mode,order_id,version,delivery_count,source_position)`; Broken `poller_checkpoint(last_updated_at)`.<br>1. `POST /orders/{id}/transitions`. 2. `GET /observed?mode=`. |
| Broken → Correct | Broken resumes polling with `updated_at > checkpoint`. Correct changes only capture source to PostgreSQL logical WAL plus Debezium's retained replication slot/LSN offset; the expected-set assertion and idempotent sink are fixed. |
| Reproduce | Commit v1 with fixed `updated_at=T`; wait until observed and Broken checkpoint T is durable; `SIGKILL` capture process; while down commit v2 with the same T; restart. Broken strict `>` misses v2. Correct Debezium resumes WAL and emits v2; a duplicate v1 is acceptable. |
| Proof | Profile X: Broken 3/3 lacks v2; Correct 10/10 contains every expected `(order,version)`, with delivery counts retained; 180 s/run, 20 min proof. |
| Tech & prerequisites | .NET 10, PostgreSQL 18 with `wal_level=logical`, Kafka 4.3.1 single KRaft, Debezium Connect; Core 08 and 17; estimated 230–300 core .NET LOC. |
| Limits | Not exactly-once, connector primary failover, slot recreation, schema evolution, or Outbox-vs-CDC latency (E04). Publication must exclude sink tables; missing slot/WAL or starting before connector readiness is Invalid. |
| Evidence strength | Debezium LSN restart and possible recovery duplicates are Verified product semantics; same-timestamp crash fixture is Reasonable inference; local connector composition remains Open. |

### 19 — Atomic Database Stream Consumption

| Field | Decision |
| --- | --- |
| Problem | If state/output commit but source position does not before a crash, will Kafka replay cause the same record to be applied twice? Slug: `19-stream-restart`. |
| Invariant | For every `(topic,partition,offset)`, durable output count is exactly one, and `state.total == SUM(input.delta for offsets < db_checkpoint.next_offset)` after bounded recovery. |
| Data & API | Kafka single-partition input `{eventId,key,delta}`; PostgreSQL `stream_checkpoint(processor,topic,partition,next_offset)`, `stream_state(key,total)`, `stream_outputs(topic,partition,offset,attempt_id,key,total_after)`.<br>1. `POST /inputs`. 2. `GET /state/{key}`. 3. `GET /outputs?partition=&offset=`. |
| Broken → Correct | Broken transaction A commits state/output, then transaction B saves DB checkpoint, then Kafka offset is best-effort committed. Correct changes only the DB transaction boundary: checkpoint, state, and output commit atomically. Kafka offset is committed only afterward and is never correctness authority. On every assignment the consumer explicitly seeks the PostgreSQL `next_offset`; records below it are skipped as already committed. |
| Reproduce | Fresh topic, one partition, offsets 0..2 with deltas `[+5,+7,-2]`, one processor. At offset 1, crash with exit 137 after DB effect commit but before checkpoint/Kafka commit; restart with fault disabled. Broken applies offset 1 twice. Correct's DB checkpoint is already 2 and replay is skipped. |
| Proof | Profile X: Broken 3/3 has two outputs for offset 1 and state 17 instead of 10; Correct 10/10 has one output per offset, state 10, DB checkpoint 3; 180 s/run, 20 min proof. |
| Tech & prerequisites | .NET 10, PostgreSQL 18, Kafka 4.3.1, locked .NET Kafka client; Core 07 and 18; estimated 230–300 core LOC. |
| Limits | Claim only database-visible effectively-once effects in one PostgreSQL transaction domain. Do not call this Kafka exactly-once or end-to-end exactly-once; output is not a Kafka topic. No multi-partition aggregate, rebalance fencing (E05), retention gap, or poison-record handling. |
| Evidence strength | Atomic source-position/state/result pattern is Verified concept; narrow .NET/PostgreSQL design is Reasonable inference; crash proof remains Open. This is sufficient to avoid a Kafka Streams/JVM application without borrowing Kafka EOS claims. |

### 20 — Bounded Out-of-order Event-time Windows

| Field | Decision |
| --- | --- |
| Problem | When arrival order differs from event time, are within-bound events assigned to their event-time window and post-close events made observable as late? Slug: `20-event-time`. |
| Invariant | Final `[12:00,12:01)` sum is 30; event C is included; event E does not alter the final sum and appears exactly once in `late_events`; every input coordinate is classified once. |
| Data & API | Kafka `{eventId,key,eventTimeUtc,receivedAtUtc,amount}`; PostgreSQL `stream_checkpoint`, `watermark_state`, `window_state`, `final_windows`, `late_events`.<br>1. `POST /events`. 2. `GET /windows`. 3. `GET /late-events`. |
| Broken → Correct | Broken windows by `receivedAtUtc` and has no event-time close/late classification. Correct changes only `ITimePolicy`: event-time window, `watermark=max_event_time_seen-10s`, finalize when `watermark >= window_end+5s`, and route arrivals after finalization to `late_events`. Lab 19's atomic DB checkpoint/state/output transaction is identical in both variants. |
| Reproduce | Single partition, 60 s windows, 10 s out-of-orderness, 5 s grace. Arrival order: A event/receive `12:00:10` +10; B `12:01:12` +7 gives watermark `12:01:02`; C event `12:00:55`, receive `12:01:13` +20 is accepted before close `12:01:05`; D event/receive `12:01:20` +3 advances watermark to `12:01:10` and finalizes window 0; E event `12:00:40`, receive `12:01:21` +99 is late. |
| Proof | Profile S: Broken 5/5 final window 0 is 10 and lacks late E; Correct 20/20 final is 30, includes C, and records E exactly once; 120 s/run, 20 min proof. |
| Tech & prerequisites | .NET 10, PostgreSQL 18, Kafka 4.3.1; Core 19; estimated 240–300 core LOC. |
| Limits | Scoped to one partition and documented bounded disorder. No distributed/idle-partition watermark, clock-skew correction, retractions, or Kafka Streams semantics. |
| Evidence strength | Event-time/watermark/late-event concepts are Verified; custom .NET single-partition policy is Reasonable inference; executable evidence remains Open. Kafka is only the ordered input log, so no Kafka Streams/JVM application or product guarantee is required. |

## Extension Labs

### E01 — Serializable vs Explicit Locking under Contention

| Field | Blueprint |
| --- | --- |
| **Problem** | Under one fixed high-contention global-capacity workload, can ordered row locks preserve the same business constraint while meeting an operational budget that bounded Serializable retries cannot? Slug: `e01-serializable-vs-explicit-locking`. |
| **Invariant** | `SUM(capacity_bucket.used) <= 640`; `COUNT(reservation) = accepted_requests`; `retry_exhausted = 0`. Reference-runner defaults: `transaction_attempts / committed_reservations <= 1.10` and HTTP `p99 <= 10 s`. The baseline is Broken only when it violates this declared compound predicate; being vaguely slower is not a failure. |
| **Data & API** | Two `capacity_bucket(id, used, capacity)` rows with total capacity 640; `reservation(request_id, bucket_id, created_at)` with unique request IDs. `POST /broken/reservations/{requestId}`, `POST /correct/reservations/{requestId}`, `GET /state`. Core-code target: 180–240 lines. |
| **Broken → Correct** | **Broken:** PostgreSQL `SERIALIZABLE`, full-transaction retry at most three times with fixed `5/10/20 ms` backoff. **Correct:** `READ COMMITTED` plus `SELECT ... FOR UPDATE` of both capacity rows in ascending ID order. This concurrency-control strategy is the only changed variable; schema, business predicate, SQL work, hold time, timeout, and input remain fixed. |
| **Reproduce** | Seed `4101`; 32 k6 VUs × 20 unique requests = 640, with a seeded balanced bucket sequence and synchronized start. Both variants hold 10 ms after reading aggregate capacity and before writing. Run one warm-up, then five interleaved paired measurements, resetting the fixture before every variant. |
| **Proof** | SQL directly checks total use, accepted/reservation equality, and request uniqueness; retain attempts, serialization aborts, exhausted retries, and p99. **Profile P:** Broken exceeds the compound gate in at least 4/5 runs; Correct has correctness 5/5 and meets the gate in at least 4/5. Primary comparison is attempts per commit: direction agrees in at least 4/5 pairs, median reduction is at least 20%, and each variant's CV is at most 15%. |
| **Tech & prerequisites** | ASP.NET Core, PostgreSQL, k6; one stateful-system type. Core prerequisites: 03 and 04. |
| **Limits** | No universal claim that explicit locking is faster; no deadlock-strategy or alternate-data-distribution comparison. The 10 ms hold is a controlled workload, not production latency. If the hold rather than lock contention dominates, the evidence is Invalid. |
| **Evidence strength** | **Verified fact:** the accepted portfolio fixes the question, prerequisites, technology ceiling, and Profile P. **Reasonable inference:** this fixture and its numeric defaults isolate useful-work amplification. **Implementation-only open:** validate stable separation at 32 VUs and record the reference-runner specification; do not silently loosen a failed threshold. |

### E02 — Cache Stampede at a TTL Cliff

| Field | Blueprint |
| --- | --- |
| **Problem** | When one hot key receives a synchronized burst immediately after expiry, can per-key single-flight limit each cache generation to one origin fetch while preserving the Core 10 version rule and a declared latency budget? Slug: `e02-cache-stampede-ttl-cliff`. |
| **Invariant** | Every response has `response.version = origin.version = 7`; `origin_fetches_per_expiry_generation <= 1`; `peak_origin_in_flight <= 1`; reference-runner HTTP `p99 <= 250 ms`. |
| **Data & API** | PostgreSQL `item(key, value, version)` with only `hot-1`; Redis `item:hot-1` containing `{value, version}` with a fixed 2 s TTL; run-scoped in-process origin counters. `GET /broken/items/hot-1`, `GET /correct/items/hot-1`, `GET /state`. Core-code target: 170–230 lines. |
| **Broken → Correct** | **Broken:** every Redis miss independently queries PostgreSQL. **Correct:** callers for the same missing key share one in-flight origin Task and cache fill. Per-key single-flight is the only changed variable; TTL jitter is deliberately excluded because changing it simultaneously would make the cause ambiguous. TTL, key, payload, origin query, connection pool, and one-API-instance topology remain fixed. |
| **Reproduce** | Seed `4202`; warm the key, wait until `TTL + 50 ms`, then synchronize 160 VUs for one request each. The common origin query has a controlled 50 ms delay and the PostgreSQL pool is capped at 16. Run one warm-up and five interleaved paired runs, creating a fresh cache generation before each variant. |
| **Proof** | Check every returned version; cross-check API counters with origin-query count; retain amplification, peak origin concurrency, and p99. **Profile P:** Broken violates amplification or p99 in at least 4/5 runs; Correct has correctness 5/5 and passes at least 4/5. Origin-fetch amplification must improve in at least 4/5 pairs, by at least 20% at the median, with CV at most 15% for each variant. |
| **Tech & prerequisites** | ASP.NET Core, PostgreSQL, Redis, k6; two stateful-system types. Core prerequisite: 10. |
| **Limits** | Does not change cache-consistency/version semantics; does not cover multi-replica distributed coalescing or TTL jitter. The 50 ms delay and pool cap must be identical. Instrumentation that materially slows the request path makes the run Invalid. |
| **Evidence strength** | **Verified fact:** the portfolio requires a TTL-cliff degradation Lab with Profile P and permits Redis/k6. **Reasonable inference:** a single-key 160-request burst and 250 ms budget isolate per-key amplification. **Implementation-only open:** verify Redis expiry timing, single-flight cleanup after errors, and stable p99 separation on the reference runner. |

### E03 — Synchronous Replication under Primary Loss

| Field | Blueprint |
| --- | --- |
| **Problem** | With the same replication delay and abrupt primary-loss point, does synchronous commit guarantee that every write acknowledged to the client exists after standby promotion? Slug: `e03-synchronous-replication-primary-loss`. |
| **Invariant** | Let `A` be IDs whose success responses the external harness received before the fault and `P` be IDs on the promoted standby. Require `A ⊆ P`, equivalently `lost_acknowledged_writes = 0`. Unacknowledged in-flight writes are outside the claim. |
| **Data & API** | `lab_write(id, ordinal, payload_hash, created_at)` with unique ID and ordinal; the harness keeps `{id, ordinal, ack_monotonic_time}` outside the database cluster. `POST /writes`, `GET /writes/{id}`. Core-code target: 140–210 lines, excluding Compose fault orchestration. |
| **Broken → Correct** | **Broken:** `synchronous_commit=local` with no synchronous standby. **Correct:** `synchronous_standby_names='FIRST 1 (standby)'` and `synchronous_commit=on`. Commit-acknowledgement policy is the only changed variable; application, schema, delay, workload, kill point, and promotion steps remain fixed. |
| **Reproduce** | Seed `4303`; begin only after the standby is streaming and fully caught up. Add 750 ms delay only to primary→standby replication traffic, not the client network. Four clients issue unique writes; immediately `SIGKILL` primary after the 40th observed success response, drop unacknowledged IDs from the claim, remove delay, promote standby, reconnect, and query all IDs in `A`. |
| **Proof** | Compare the ACK ledger with promoted data and retain sync state, ACK count, fault/promotion timestamps, and missing IDs. **Profile R + required fault modifier:** Broken loses at least one acknowledged ID in 3/3 runs; Correct loses none in 10/10. Per-run ceiling 180 s; whole proof 20 min. |
| **Tech & prerequisites** | ASP.NET Core, PostgreSQL primary/standby, bounded Compose/netem fault harness; one stateful-system type with multiple nodes. Core prerequisite: 11. |
| **Limits** | Scoped RPO only: no RTO, promotion-speed, availability, or latency claim. Graceful shutdown, a non-ready standby, delay on the client path, or promotion of the wrong node makes the run Invalid. |
| **Evidence strength** | **Verified fact:** the portfolio fixes primary loss, acknowledged-write durability, Profile R, and the RTO non-goal. **Reasonable inference:** 750 ms delay and the 40th-ACK kill point create a bounded loss window. **Implementation-only open:** prove replication-interface netem portability, automate promotion, and define readiness with an explicit synchronous `sync_state` check. |

### E04 — Outbox Relay: Polling vs CDC

| Field | Blueprint |
| --- | --- |
| **Problem** | Under the same outbox, Kafka sink, and relay crash/restart, can WAL/LSN-based CDC preserve every committed event and meet recovery/observability budgets that a fixed-interval polling relay cannot? Slug: `e04-outbox-polling-vs-cdc`. |
| **Invariant** | Within 15 s after restart, `committed_event_ids ⊆ observed_event_ids` and no unknown event ID appears. Duplicates are counted but allowed. Reference-runner defaults: backlog drains within 3 s of relay readiness and steady-state `p95_commit_to_observable <= 1 s`. Because bounded completion is declared, exceeding it is a valid violation rather than an uninterpretable timeout. |
| **Data & API** | `business_order(id, status)` and `outbox(event_id, aggregate_id, event_type, payload, committed_at, published_at)` written atomically; the Kafka envelope keeps the same `event_id` and `committed_at`. One API: `POST /orders`. Core-code target: 200–280 lines; declarative connector config is excluded. |
| **Broken → Correct** | **Broken:** correct polling relay with a fixed 5 s interval. **Correct:** Debezium CDC from PostgreSQL WAL to the same Kafka topic. Relay transport is the only changed variable; business transaction, outbox schema, event identity, input, sink, and fault schedule remain fixed. |
| **Reproduce** | Seed `4404`. **Crash proof:** after catch-up, `SIGKILL` relay; while down, commit 20 events at 50 ms spacing, remain down for 1 s, restart, wait for the same explicit ready condition, and time backlog drain. **Performance modifier:** no fault, 60 events at 100 ms spacing, one warm-up plus five interleaved paired runs. Use isolated run IDs/topic prefixes for every run. |
| **Proof** | Compare PostgreSQL's committed ID set with Kafka consumer observations; retain missing, unknown, duplicate, first-observed, and ready-to-drained data. Reject setup if DB/observer clock skew exceeds 25 ms. **Primary Profile X + fault modifier:** Broken violates the 3 s recovery predicate 3/3; Correct has zero violations 10/10. **P modifier:** Correct correctness 5/5 and latency gate at least 4/5; direction agrees at least 4/5, median improves at least 20%, and each CV is at most 15%. |
| **Tech & prerequisites** | ASP.NET Core, PostgreSQL, Kafka, Debezium/Kafka Connect; two stateful-system types. Core prerequisites: 08 and 18. |
| **Limits** | No exactly-once claim and no comparison of CPU, broker throughput, schema registry, or initial snapshot bootstrap. Connector not RUNNING, an enabled initial snapshot, stale-topic contamination, or excess clock skew makes evidence Invalid. |
| **Evidence strength** | **Verified fact:** the accepted comparison, prerequisites, X primary profile, P modifier, and no-loss boundary are fixed. **Reasonable inference:** 5 s polling versus 3 s recovery and 1 s steady-state budgets provide a falsifiable scoped SLO. **Implementation-only open:** pin a compatible Debezium/Connect image, make readiness executable, and verify the reference runner can sustain CV at most 15%. |

### E05 — Consumer-group Rebalance Ownership Fencing

| Field | Blueprint |
| --- | --- |
| **Problem** | After consumer A loses a partition but its paused old work later resumes, can a resource-side assignment epoch prevent that stale owner from committing partition state or output? Slug: `e05-rebalance-ownership-fencing`. |
| **Invariant** | Every accepted commit has `attempt_epoch = current_epoch_at_commit`; after epoch `e+1` is installed, accepted commits from epoch `e` or earlier equal zero. The final fixture requires `projection.last_sequence = 2`, and Correct must directly observe at least one rejected stale attempt. |
| **Data & API** | PostgreSQL `partition_owner(partition_id, epoch, owner_id)`, `projection(partition_id, value, last_sequence, committed_epoch)`, and `commit_audit(record_id, partition_id, sequence, attempt_epoch, accepted, observed_at)`; Kafka has one partition with `r1(seq=1,v1)` and `r2(seq=2,v2)`. `GET /state/0`. Core-code target: 230–300 lines. |
| **Broken → Correct** | **Broken:** assignment obtains an epoch, but the delayed handler commits projection/output without checking it. **Correct:** the same transaction conditionally commits only when partition, epoch, and owner still match; zero affected rows rejects state/output and prevents the following offset commit. Resource-side epoch authorization is the only changed variable; revoke cancellation/drain remains the same best-effort control in both variants. |
| **Reproduce** | Seed `4505`; one partition, two dynamic consumers, 5 s session timeout. A owns epoch 1, reads r1, and stops at a pre-commit barrier. Pause A; start B; wait for A eviction and B epoch 2. B reprocesses r1 then commits r2. Resume A and release the barrier so its epoch-1 write must attempt commit. Every wait has a 15 s ceiling; a run without actual reassignment is Invalid. |
| **Proof** | Audit accepted commits after the epoch transition and verify final projection. Broken accepts A's epoch-1 commit and violates the predicate 5/5; Correct preserves sequence 2, accepts no stale commit, and records a stale rejection 20/20. **Profile S + required fault modifier:** per-run ceiling 120 s; whole proof 20 min. |
| **Tech & prerequisites** | Two .NET consumers, minimal inspect API, Kafka, PostgreSQL, bounded Compose pause/resume harness; two stateful-system types. Core prerequisites: 15 and 19. |
| **Limits** | No broker-loss, cross-partition-ordering, generic deduplication, event-time, or Core 19 crash-atomicity claim. Static membership, failure to reach the barrier, retention of A's assignment, or failure of B to install epoch 2 makes the run Invalid. Stop/drain reduces waste but is not the correctness boundary. |
| **Evidence strength** | **Verified fact:** the portfolio fixes reassignment ownership, prerequisites, Profile S, and the fault modifier. **Reasonable inference:** the two-record pause/rebalance/resume schedule directly exercises the final fence. **Implementation-only open:** pin the .NET Kafka client, make group/session settings deterministic, validate Compose pause portability, and retain rejection evidence without weakening state-transaction atomicity. |

## Evidence strength

**Verified fact:** the repository has accepted a 20-Lab Core DAG, a five-Lab optional portfolio, an isolated per-Lab execution contract, seven evidence profiles, a default technology baseline, and the evidence-label semantics used here. The cited primary sources support the named database, replication, messaging, CDC, stream, cache, lease, fencing, and schema-evolution boundaries. This page contains 25 unique implementation packets and assigns each one a question, invariant, mechanism change, workload or fault, profile, minimum technology, prerequisites, and limits.

**Reasonable inference:** the selected APIs, schemas, deterministic schedules, numeric defaults, and 100–300-line targets should isolate the intended causal mechanism and remain locally runnable. Their feasibility and teaching value are not yet established by executable Labs or learner observations.

**Open at implementation:** each Lab must still prove dependency compatibility, fault/barrier determinism, cleanup safety, actual core-line count, profile deadlines, accepted JSON generation, and—where applicable—reference-runner variability and performance separation. Those are implementation validations, not curriculum design choices.

There is no remaining curriculum-level design choice. A future change to a Lab question, invariant, Broken／Correct boundary, prerequisite, primary evidence profile, or technology escalation must be justified by implementation evidence and recorded as a new decision rather than treated as an unresolved item in this blueprint.
