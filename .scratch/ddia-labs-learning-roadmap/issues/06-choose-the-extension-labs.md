# Choose the advanced Extension Labs

Type: grilling
Status: resolved
GitHub: https://github.com/ge1123/DDIA_LABS/issues/6

## Question

在不稀釋 20 個 Core Labs 的前提下，哪 4～6 個題目最適合作為 Extension Labs？決定哪些內容應用來比較替代技術、注入更真實的故障或量測效能，並說明它們為何不是核心路線的先修要求。

## Answer

採用 **5 個 Extension Labs**：兩個替代機制比較、兩個更真實的故障模型，以及一個效能退化實驗。Extension 編號使用 `E01`～`E05`，不插入 Core 的 `01`～`20`，也不成為任何 Core Lab 的先修。

所有 Extension 仍遵守 canonical Lab contract：一個可反駁問題、一個主要 invariant、一個 changed variable、Broken／Correct 共用 workload，以及 1～3 支 API 與 100～300 行核心程式碼目標。若比較的是兩個都能維持 correctness 的機制，Broken 代表在預先宣告的效能或恢復 invariant 下被反例推翻的 baseline，不把「較慢」含糊地當成錯誤。

| ID | Extension Lab | 類型 | 先修 Core | 單一問題與主要 invariant | Broken → Correct 的唯一變因 | 為何不是 Core 先修 | 技術 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | **Serializable vs Explicit Locking under Contention** | 替代機制比較 | 03, 04 | 在固定 contention workload 下維持相同業務 constraint，且 serialization abort／p99 latency 不得超過 Issue 07 設定的界線。 | Serializable + bounded full-transaction retry → `SELECT ... FOR UPDATE` 的明確鎖定順序；schema、資料、併發度與 invariant 不變。 | Core 只需證明 Serializable 能防止 write skew；策略選型與 contention 成本不影響後續概念。 | PostgreSQL、k6 |
| E02 | **Cache Stampede at a TTL Cliff** | 效能退化 | 10 | 同一 hot key 同時過期時，origin amplification 與 p99 latency 必須維持在預定界線內，回傳值仍符合 Core 10 的版本規則。 | 每個 miss 都回源 → per-key single-flight 加 bounded TTL jitter；key、payload、TTL 平均值與 request burst 不變。 | Core 10 研究 stale-read correctness；stampede 是容量與退化行為，不是理解 replica lag 或 sharding 的先修。 | Redis、k6 |
| E03 | **Synchronous Replication under Primary Loss** | 真實故障 | 11 | 在已定義的 abrupt primary-loss 與 promotion 流程中，已向 client 確認的寫入不得遺失；量測是 acknowledged writes lost，也就是 scoped RPO。 | asynchronous commit → synchronous commit；workload、kill point、promotion procedure 與資料檢查不變。 | Core 11 只需辨識 lag 與 read-your-writes；跨節點 durability 的成本與 failover 操作不是後續 Core 的概念前提。 | PostgreSQL primary/standby、Compose fault harness |
| E04 | **Outbox Relay: Polling vs CDC** | 替代機制比較 | 08, 18 | committed outbox rows 在 relay restart 前後不可遺失，且 commit-to-observable latency 必須通過 Issue 07 的界線。 | bounded-interval polling relay → WAL/LSN-based CDC relay；business transaction、outbox schema、event identity、sink 與 failure schedule 不變。 | Core 08 先教 dual-write，Core 18 再教 WAL recovery；只有兩者完成後才有能力比較 relay transport，這個比較不支撐其他 Core。 | PostgreSQL、Debezium、Kafka |
| E05 | **Consumer-group Rebalance Ownership Fencing** | 真實故障 | 15, 19 | partition 進入新 assignment epoch 後，舊 owner 的延遲工作不得再提交該 partition 的 state 或 output。 | consumer 忽略 revoke 後仍完成 in-flight work → revoke 時停止／drain，並以 assignment epoch fence commit；records、processor logic 與 rebalance schedule 不變。 | Core 19 的單 processor crash/restart 足以教 offset/state/output 原子性；member churn 與 partition reassignment 是產品級協調故障。 | Kafka、PostgreSQL、Compose fault harness |

### Ordering

建議在全部 Core Labs 完成後依 `E01 → E02 → E03 → E04 → E05` 執行。這是由單一資料庫策略比較，逐步增加到 cache burst、replica promotion、CDC relay 與 consumer-group coordination 的環境複雜度；Extension 之間沒有執行期依賴。

### Scope boundaries

- E01 只比較 concurrency-control strategy，不重新教授 isolation 或 write skew，也不外推單一 workload 的效能排名。
- E02 不改 cache consistency mechanism；若版本規則也改變，必須退回 Core 10 或拆成另一張 Lab。
- E03 只驗證 scoped RPO；promotion time、availability 與 RTO 是 non-goal，避免一張 Lab 同時更改 durability 和 recovery orchestration。
- E04 不重新證明 Outbox 或 CDC 的基本 correctness；它比較相同 envelope 下的 relay recovery 與 commit-to-observable latency。
- E05 只研究 reassignment ownership；broker loss、一般 duplicate handling 與 event-time window 分別留在 Core 06／07／20。
- 每張最多使用兩類有狀態外部系統；允許多個同類節點。只使用本機 Compose，不加入 cloud、Kubernetes 或 production data。

### Rejected candidate

**Lease／Fencing under Redis Failover** 不納入。它需要同時重現 Redis failover、lease ownership 與 resource-side fencing，與 Core 14–15 的 causal mechanism 重疊最高；若不能只改 lease backend，就會違反單一 changed-variable 規則。真實 failover 的教學名額由 E03 使用，ownership fencing 的進階名額由 E05 使用。

### Evidence strength

**Verified fact:** Core 路線已把相關基礎概念拆成獨立 Labs；技術基線也只允許在研究問題需要時引入 Redis、Kafka、Debezium、Testcontainers 或 k6。Canonical contract 要求每張 Lab 只有一個主要 invariant 與 changed variable。

**Reasonable inference:** 這五張能在不增加 Core 先修的前提下，均衡補上策略比較、效能退化與更真實故障。這是根據目前 prerequisite DAG 與 Lab boundary 推導，尚未有 executable Lab 或 learner evidence。

**Open question:** Issue 07 已定義共用 evidence profiles 與數字門檻；各 Extension 仍須在 Issue 08 宣告 exact workload、primary metric、API 與 fixture。這些不改變五張 Extension 的概念邊界。
