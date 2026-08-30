# Sequence the 20 Core Labs by learning prerequisites

Type: prototype
Status: resolved
GitHub: https://github.com/ge1123/DDIA_LABS/issues/5

## Question

20 個 Core Labs 應如何由簡到難排列，讓每一個新 Lab 只增加一個主要概念或 failure mode？產出先修關係、分階段理由與粗略情境，並特別處理冪等性、並行異常、隔離層級、訊息投遞、跨服務一致性、快取、複寫、分片、鎖與 fencing、事件與資料流之間的依賴。

## Answer

### Governing rule

採用 **01 → 20 的建議線性閱讀順序，加上一個較寬鬆的 prerequisite DAG**。編號順序用來降低學習時的 context switching；DAG 則只標記「若缺少此概念，就無法正確解釋後續 observation」的真正先修，不把相鄰主題誤寫成 runtime dependency。

每個 Lab 只引入一個新的 failure boundary 或 correctness mechanism；同一 Lab 不同時教兩個可獨立失敗的概念。

### Proposed Core path

| # | Phase | Lab | Prerequisites | New failure boundary / mechanism | Coarse scenario |
| --- | --- | --- | --- | --- | --- |
| 01 | A | Race Condition／超賣 | — | 非原子 check-then-act → 條件式原子更新 | 兩筆訂單同時搶最後一件庫存 |
| 02 | A | Lost Update | 01 | read-modify-write 覆寫 → 原子更新或 CAS 重試 | 兩人同時替計數器加一 |
| 03 | A | Isolation | 02 | 交易內讀取漂移 → 明確快照語意 | 報表查詢期間另一交易提交 |
| 04 | A | Write Skew | 03 | 多列約束在 snapshot 下失效 → Serializable 完整交易重試 | 兩名值班醫師同時請假 |
| 05 | B | HTTP 冪等命令 | 02 | client retry 重複效果 → idempotency key 與結果保存 | 付款成功但 client timeout 後重送 |
| 06 | B | MQ ACK／redelivery | 05 | consumer crash 的 loss／redelivery 取捨 → durable effect 後 ACK | consumer 處理途中崩潰 |
| 07 | B | Inbox | 02, 06 | broker duplicate 變成重複業務效果 → Inbox 同交易去重 | effect commit 後、ACK 前崩潰 |
| 08 | B | Transactional Outbox | 06, 07 | DB＋broker dual write → 同交易 outbox 與可重試 relay | DB commit 與 publish 之間崩潰 |
| 09 | B | Saga／補償 | 05, 07, 08 | 跨服務部分成功 → durable saga state 與冪等補償 | 第二個服務失敗，第一步已提交 |
| 10 | C | Cache Consistency | 03 | cache refill 競態回寫舊值 → version／minVersion | invalidation 與 repopulation 交錯 |
| 11 | C | Replication Lag | 03, 10 | async replica stale read → LSN token、等待或 primary fallback | 寫 primary 後立即讀 replica |
| 12 | C | Sharding Routing | 02 | process 間 routing 不一致 → stable hash 與明確 shard map | 同 tenant 被分散到不同 shard |
| 13 | C | Hot Partition | 12 | routing 正確但 workload skew → key salting 與 fan-in | 熱門 tenant 壓垮單一 shard |
| 14 | D | Distributed Lease | 06, 11 | owner crash／lease expiry → owner token、TTL、compare-delete | lease 過期後舊 owner 才恢復 |
| 15 | D | Fencing Token | 14 | 過期 worker 仍能晚到寫入 → resource-side monotonic fencing | stale worker 覆蓋新 owner |
| 16 | E | Event Sourcing | 02, 08 | current-state overwrite 無法重播 → append-only events 與 deterministic fold | 清空 projection 後重建 |
| 17 | E | Event／Schema Evolution | 16 | rolling deploy 的 mixed versions → additive schema 與 tolerant reader | old/new producer-consumer 共存 |
| 18 | E | CDC | 08, 17 | polling／restart 漏 change → WAL offset／LSN resume | connector snapshot 後重啟 |
| 19 | E | Stream Restart Correctness | 07, 18 | state update 與 offset commit 分離 → offset/state/output 原子提交 | processor 在 commit 邊界崩潰 |
| 20 | E | Event Time／Out-of-order | 19 | arrival time 不等於 event time → watermark、grace、late counter | 亂序事件跨過封窗時間 |

### Phase rationale

1. **A — 單一資料庫的並行與交易（01–04）**：先辨識 row-level check/update，再擴大到 snapshot 與跨列約束。後續所有 dedup、outbox、saga 都需要這裡的 transaction vocabulary。
2. **B — 重試、訊息與跨服務一致性（05–09）**：依序擴大 retry boundary：client → broker → consumer effect → producer dual write → multi-service workflow。ACK、Inbox、Outbox 不合併，因為 loss、duplicate 與 dual write 是三種不同失敗。
3. **C — 陳舊讀取、複寫與分割（10–13）**：先比較 cache 與 replica 的兩種 stale read，再從 routing correctness 走到 routing 正確但 workload skew 的 hot partition。
4. **D — 租約失效與 stale writer（14–15）**：Lease 只管理 ownership window；Fencing 由 resource 拒絕過期 writer。先完成 14 才能在 15 看見 lease 本身保護不了的邊界。
5. **E — 不可變資料與串流（16–20）**：先建立可重播事件，再處理 schema 多版本、DB change capture、processor restart，最後才加入 event-time ordering。Restart correctness 與時間語意保持分開。

### Why these prerequisites are real

- 05 需要 02：idempotency record 的唯一性、result reuse 與業務 effect 必須建立在已理解的原子資料庫更新上。
- 07 需要 06：若未先看見 ACK 後的 redelivery，就會把 Inbox 當成無來源的樣板。
- 08 需要 07：Outbox relay 是 at-least-once；先理解 consumer dedup 才不會把 Outbox 誤解成 end-to-end exactly-once。
- 10 與 11 相鄰但不合併：兩者都產生 stale read，來源分別是 derived cache 與 asynchronous replica。
- 13 需要 12：只有 routing correctness 已成立，負載 skew 的量測才有意義。
- 15 需要 14：Fencing 解決的是 valid lease protocol 仍無法阻止的 stale writer，不是 lease release bug。
- 18 需要 17：CDC 產生的 change stream 會跨部署版本，不能把 payload evolution 當成無關細節。
- 19 需要 07 與 18：restart 後可能重讀 input；必須先理解 duplicate effect 與可恢復的 source offset。
- 20 需要 19：先固定 crash/restart correctness，才能把唯一 changed variable 收斂為 event-time ordering。

### Prototype result

- Prototype branch: `codex/prototype-core-lab-sequence`
- Prototype commit: `94a5a10`
- Structural result: 20 unique nodes, 28 forward-only prerequisite edges, five phases, no missing dependency, and no cycle.
- Guided rejection case: Lab 15 is blocked until Lab 14 is complete.
- Guided stream case: 16 → 17 → 18 → 19 → 20 keeps replay, schema, source recovery, processor recovery, and time semantics separate.

### Evidence strength and remaining questions

- **Verified fact:** the cited primary-source research supports the 20 concept anchors and the need to split transaction anomalies, ACK/Inbox/Outbox, Sharding/Hot Partition, Lease/Fencing, and stream restart/event time.
- **Verified structural fact:** the retained prototype validates the stated node count, dependency references, forward ordering, and absence of cycles for this proposed graph.
- **Reasonable inference:** the five-phase linear order minimizes conceptual jumps for a learner. No learner study or executable Lab yet verifies teaching effectiveness.
- **Open question:** Issue 07 has defined the shared evidence profiles and numeric defaults. Issue 08 must still assign exact API shapes, workloads, profile selections, technology exceptions, and Wiki pages. Kafka Streams versus a narrower .NET implementation for Labs 19–20 remains a later technical decision.
