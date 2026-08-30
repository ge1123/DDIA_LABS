# DDIA 概念錨點與 20 個 Core Labs 候選

研究日期：2026-08-30  
用途：回覆「Anchor the curriculum in DDIA concepts and primary sources」；這是課程決策依據，不是 Lab 執行證據。

## 建議結論

以 2026 年 2 月出版的《Designing Data-Intensive Applications, 2nd Edition》為主要版次。官方目錄已把使用者要求的大部分主題集中在 Ch. 3、5–10、12–13：Event Sourcing/CQRS、encoding/evolution、replication、sharding、transactions、distributed locks/leases、consistency，以及 CDC/stream processing。[O'Reilly 的第二版書目與完整目錄](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/)可直接支持這個課程骨架。

最小而仍連貫的核心集合是下列 20 個 Lab。排序是「單一資料庫並行 → 重試與訊息 → 跨元件一致性 → 分散式讀寫 → 租約安全 → 不可變資料流」；相鄰 Lab 可以共用概念語彙，但每個 Lab 必須有自己的 Compose、資料、重現命令與 invariant，不形成執行期相依。

標記：

- **DDIA 直接**：官方第二版章名或節名直接涵蓋該概念。
- **實務模式**：DDIA 提供問題模型，但這個具名解法主要來自標準或產品／平台的一手文件。
- **教學情境**：用來重現 DDIA 機制的應用情境，不是書中的規範術語。

## 建議的 20 個 Core Labs

| # | 單一核心問題與 invariant | Broken → Correct 的最小邊界 | 概念錨點 | 分類 |
| --- | --- | --- | --- | --- |
| 01 | **Race Condition／超賣**：並發成功訂單數不得超過初始庫存，`stock >= 0`。 | `SELECT` 後在應用程式判斷再 `UPDATE` → 單一條件式 `UPDATE ... WHERE stock >= qty`，以受影響列數決定成功。 | [DDIA2 Ch. 8 Transactions](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch08.html)；PostgreSQL 將同時存取列的行為歸在[並行控制](https://www.postgresql.org/docs/current/mvcc.html)。 | 教學情境；機制是 DDIA 直接 |
| 02 | **Lost Update**：兩個已接受的增量都必須反映在終值。 | read-modify-write 覆寫 → 原子更新，或版本欄位 compare-and-set 加完整重試。 | DDIA2 Ch. 8 目錄明列 “Preventing Lost Updates”；PostgreSQL 的[交易隔離](https://www.postgresql.org/docs/current/transaction-iso.html)定義 serialization anomaly 與各隔離層級。 | DDIA 直接 |
| 03 | **Isolation**：同一交易需要的兩次讀取應屬同一可說明的快照。 | 在 Read Committed 下誤以為兩次讀取相同 → 明確使用 Repeatable Read，並把 observable 差異寫成測試。 | [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)指出 Read Committed 可有 nonrepeatable read，而 PostgreSQL Repeatable Read 不允許它。 | DDIA 直接 |
| 04 | **Write Skew**：跨多列的業務約束（例如至少一名醫師值班）永遠成立。 | Snapshot/Repeatable Read 下兩交易讀相同集合、各改不同列 → Serializable + 對 `40001` 重跑完整交易。 | DDIA2 Ch. 8 明列 “Write Skew and Phantoms” 與 SSI；PostgreSQL 說明 Serializable 只提交可對應某個序列順序的執行，且應用必須[重試完整交易](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html)。 | DDIA 直接 |
| 05 | **HTTP 冪等命令**：同一 logical command 重送 N 次只產生一個業務效果，且回傳同一結果。 | POST timeout 後重試造成重複扣款／訂單 → idempotency key、唯一約束、同交易保存結果並檢查參數一致。 | RFC 9110 定義[冪等方法](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)；POST 的 idempotency key 是應用層模式，可由 [Stripe 一手 API 文件](https://docs.stripe.com/api/idempotent_requests)錨定。 | 實務模式；DDIA Ch. 13 correctness 為概念背景 |
| 06 | **MQ acknowledgement 與重送**：一個已被 broker 接受的訊息不可因 consumer crash 永久遺失。 | 處理前 ACK（at-most-once，會遺失）→ 完成 durable effect 後才 ACK（at-least-once，允許重送），並刻意證明 duplicate 仍可能出現。 | [RabbitMQ Reliability Guide](https://www.rabbitmq.com/docs/reliability)明載無 ACK 可能遺失；ACK 提供 at-least-once，故障時可能重送。DDIA2 Ch. 12 是 messaging systems 錨點。 | DDIA 直接 + broker 語義 |
| 07 | **Inbox／MQ 重複訊息**：同一 `message_id` 最多只能提交一次業務效果。 | effect commit 後、ACK 前 crash，重送造成二次效果 → `processed_messages` 唯一鍵與業務寫入放在同一 PostgreSQL transaction。 | RabbitMQ 要求 consumer 能處理舊 delivery；[NServiceBus Outbox 文件](https://docs.particular.net/nservicebus/outbox/)展示以 incoming `MessageId` 去重並與 business data 同交易。DDIA2 Ch. 8 “Exactly-Once Message Processing Revisited” 是問題錨點。 | **Inbox 是實務模式名稱**，不是 DDIA 目錄術語 |
| 08 | **Transactional Outbox**：業務狀態與「應發出的事件意圖」不可一有一無；relay 可以至少一次投遞。 | DB commit 與 broker publish 雙寫，在任一 crash point 產生漏訊息或 ghost message → business row + outbox row 同一 DB transaction，獨立 relay 重試。 | [AWS Transactional Outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)直接定義 dual-write 問題，也明示仍可能重複；[Debezium Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)是第一方實作。概念對應 DDIA2 Ch. 12 “Keeping Systems in Sync”。 | **Outbox 是實務模式名稱**；勿宣稱它單獨提供 exactly-once |
| 09 | **Saga／補償**：跨兩個資料庫的流程最終只能是 `Completed` 或可稽核的 `Compensated`，不可永久卡在未記錄的半完成。 | 連續呼叫兩服務，第二步失敗後留下第一步效果 → durable saga state、冪等 local steps、明確 compensation 與重試。 | [Azure Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga)定義 local transactions 與 compensating transactions；[Compensating Transaction](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction)強調補償本身可能失敗且步驟須冪等。DDIA2 Ch. 5 workflows／Ch. 8 distributed transactions 是背景。 | **Saga 是實務模式名稱**，非 DDIA 的核心章節術語 |
| 10 | **Cache Consistency**：完成寫入後，帶有該寫入版本的讀取不得回傳更舊版本。 | naive cache-aside 在 invalidation/repopulation 競態中重新寫回舊值 → DB row version + cache value version；讀者帶 `minVersion`，舊 cache 必須 bypass/refresh，TTL 只作有界退路。 | [Azure Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)明示此模式不保證 DB/cache 一致；[Redis cache-aside](https://redis.io/docs/latest/develop/use-cases/cache-aside/)把 TTL 描述為 staleness bound。 | **Cache-aside／版本化讀取是實務模式**；DDIA Ch. 13 derived state 為背景 |
| 11 | **Replication Lag／read-your-writes**：成功寫入後，同一 session 的後續讀取不得看見較舊狀態。 | write primary、立即 read async replica → 回傳 commit/LSN token，讀取時等待 replica replay 到 token或暫時路由 primary。 | DDIA2 [Ch. 6 Replication](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch06.html)明列 replication lag；PostgreSQL 證實 streaming replication [預設非同步](https://www.postgresql.org/docs/current/warm-standby.html)，`replay_lag`近似交易對查詢可見前的延遲。 | DDIA 直接 |
| 12 | **Sharding routing**：同一 shard key 在所有 API instance 都只能路由到同一 shard。 | round-robin 或 process-randomized hash 讓同一 tenant 散落多庫 → 穩定 hash + 明確 shard map，測試跨 process 一致性。 | DDIA2 [Ch. 7 Sharding](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch07.html)定義每筆資料屬於一個 shard，並涵蓋 key-range/hash routing。 | DDIA 直接；routing bug 是教學情境 |
| 13 | **Hot Partition**：在指定 skew workload 下，最忙 partition 的負載比率必須降到明定門檻，同時聚合結果正確。 | 直接以超熱門 tenant/key 分割 → 對可交換、可結合的 counter 進行 key salting/bucketing，讀取 fan-in。 | DDIA2 Ch. 7 目錄明列 “Skewed Workloads and Relieving Hot Spots”。 | DDIA 直接；修法只對此 workload 成立 |
| 14 | **Distributed Lock 的 lease 所有權**：過期 owner 不得刪除新 owner 的 lease，crash 也不可永久阻塞資源。 | 無 TTL 的 `SETNX` 或無條件 `DEL` → unique owner token + TTL + compare-and-delete；明確把保證限制在 validity window。 | DDIA2 Ch. 9 明列 “Distributed Locks and Leases”；[Redis distributed-lock 文件](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)定義 TTL、unique value 與安全釋放。 | DDIA 直接 |
| 15 | **Fencing Token**：resource 一旦接受 token `n`，任何 `< n` 的 stale worker 都不得再寫。 | A lease 過期但 A 暫停後恢復並晚到寫入，覆蓋 B → 每次取得 lease 配發單調遞增 token，resource 端拒絕較舊 token。 | [Martin Kleppmann 的 distributed locking 分析](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)解釋 stale client 與 fencing；Redis 官方文件亦明確建議 consistency-sensitive 工作使用 fencing tokens。 | DDIA 直接概念；resource-side 實作是必要條件 |
| 16 | **Event Sourcing**：同一事件序列重播後必須得到與 live projection 相同的狀態。 | 只覆寫 current state，無法重建或稽核 → append-only events + deterministic fold；比較 live 與清空後 rebuild。 | DDIA2 Ch. 3 目錄直接列 “Event Sourcing and CQRS”；Ch. 12 “State, Streams, and Immutability”補上資料流錨點。 | DDIA 直接；不要把 CQRS 強綁進同一 Lab |
| 17 | **Event/schema evolution**：部署期間 old/new producer 與 consumer 的指定相容矩陣都能解碼。 | rename/remove/change type 使舊 consumer 壞掉 → additive optional field/default、tolerant reader，將 forward/backward compatibility 各自測試。 | DDIA2 [Ch. 5 Encoding and Evolution](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch05.html)指出 schema 與 code 無法原子同時升級，需處理多版本共存。 | DDIA 直接 |
| 18 | **CDC**：connector restart 前後，每個 committed row change 最終至少被觀察一次；不得用「無 duplicate」作 invariant。 | 以 `updated_at` 輪詢，在時間邊界／短暫狀態漏變更 → PostgreSQL WAL logical decoding + Debezium offset/LSN；sink 仍按 event identity 去重。 | DDIA2 Ch. 12 直接列 “Change Data Capture”；[Debezium PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)說明 snapshot 後從 WAL 位置續讀，故障恢復時可能重複但不漏事件。 | DDIA 直接 + 第一方產品語義 |
| 19 | **Stream Processing fault tolerance**：同一 input log 在 processor crash/restart 後，聚合結果不得被重複計算。 | state 更新後、offset commit 前 crash → 原子提交 input offsets、state store 與 output（或等價的 transactional boundary），以 fault injection 比對 baseline。 | DDIA2 Ch. 12 “Fault Tolerance”；[Kafka Streams Core Concepts](https://kafka.apache.org/documentation/streams/core-concepts/)將 input offsets、state updates、output 原子化描述為 end-to-end exactly-once。 | DDIA 直接；產品保證只限 Kafka 邊界 |
| 20 | **Event time／out-of-order window**：lateness bound 內的事件必須進入其 event-time window；超界事件須可觀察而不是靜默誤算。 | processing-time 或到達即封窗 → event timestamp + watermark/grace + late-event counter/DLQ；用亂序 fixture 驗證。 | DDIA2 Ch. 12 “Reasoning About Time”；Kafka Streams 官方概念文件明載 event-time windows 與 out-of-order records。 | DDIA 直接 + 第一方產品語義 |

## 必須拆開與可相鄰安排

### 必須拆開

1. **Lost Update、一般 Isolation、Write Skew** 必須是三個 Lab。三者的 read/write dependency 不同；用一個「提高 isolation」Lab 會掩蓋 PostgreSQL Repeatable Read 仍可能出現 serialization anomaly，而 Serializable 又要求完整交易重試的事實。
2. **MQ ack/redelivery 與 Inbox** 必須拆開。前者研究 broker 的 loss/duplicate trade-off；後者研究 duplicate 已存在時如何讓 business effect 去重。若直接套 Inbox，學習者看不到重送從哪裡來。
3. **Inbox 與 Outbox** 必須拆開。Inbox 保護接收端 effect；Outbox 解決送出端 DB + broker dual write，方向和 invariant 不同。
4. **Distributed Lock 與 Fencing Token** 必須拆開。安全釋放 lease 不能阻止已過期 worker 寫入 resource；fencing 的拒絕發生在 resource 端。
5. **Sharding 與 Hot Partition** 必須拆開。前者驗證 routing correctness，後者是在 routing 正確後研究 workload skew 與負載分布。
6. **Event Sourcing、CDC、Stream Processing** 必須拆開。三者分別是應用資料模型、從既有 DB log 取得 change stream、以及對 unbounded stream 維護計算；共享「log」不代表同一問題。
7. **Stream restart correctness 與 event-time ordering** 必須拆開。前者是處理保證／原子性，後者是時間語義；一個結果可以 exactly-once 但仍被放錯 window。

### 最有教學價值的相鄰關係

- 01 → 02 → 03 → 04：先看到 check-then-act，再辨識 lost update，最後理解 isolation 不只是把等級名稱調高。
- 05 → 06 → 07 → 08 → 09：client retry、broker retry、consumer dedup、producer dual write、跨服務補償逐層擴大 failure boundary。
- 10 → 11：兩者都會 stale read，但 cache staleness 與 replica lag 的來源、可觀察 token、修法不同。
- 12 → 13：先保證 key-to-shard 正確，再討論分布是否均勻。
- 14 → 15：先完成 lease protocol，再用 process pause 證明 lease 不等於 stale writer protection。
- 16 → 17 → 18 → 19 → 20：先定義 immutable event 與 evolution，再將 DB change 轉為 stream，最後處理 restart 與時間。

## 書本術語與業界模式的邊界

**Verified fact**

- DDIA2 官方目錄直接包含 Lost Updates、Write Skew、Replication Lag、Sharding/Hot Spots、Distributed Locks and Leases、Event Sourcing/CQRS、CDC、Stream Processing，以及 Exactly-Once Message Processing Revisited；因此它們可直接標為 DDIA concept anchors。
- HTTP idempotency key、Inbox、Transactional Outbox、Saga、Cache-Aside 是具體應用／架構模式。RFC、Stripe、RabbitMQ、AWS、Azure、Redis、NServiceBus 與 Debezium 文件能支持它們的操作語義，但不能把 vendor 的保證外推成所有系統的保證。

**Reasonable inference**

- 「超賣」是最小且可量測的 race-condition 教學情境；它不是 DDIA 章節術語，但能乾淨呈現非原子 check-then-act。
- 把 schema evolution 納入 20 個 Core Labs 是必要的：後五個 Lab 都依賴 durable event/history；若不先測 mixed-version compatibility，課程會把 payload 演進當成無關細節。
- 20 個已是合理下限。再合併會首先混淆 ack 與 dedup、Inbox 與 Outbox、lease 與 fencing、或 stream fault tolerance 與 event time，直接違反「一個 Lab 一個核心問題」。

**Open question（留給後續技術設計票，不阻擋概念集合）**

- Lab 19–20 是否採 Kafka Streams（最直接驗證官方 semantics，但引入 JVM）或以 .NET 自行實作較窄的 offset/state transaction 與 watermark。這是技術／複雜度決策，不改變兩個概念必須分開。
- Replication Lag Lab 要用真 PostgreSQL physical replica，還是可控延遲的 logical subscriber；前者更貼近讀副本，後者故障注入更穩定。兩者都不能把人工 delay 冒充實際產品延遲分布。

## 一手來源清單

- Martin Kleppmann、Chris Riccomini，[Designing Data-Intensive Applications, 2nd Edition](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/)，O'Reilly，2026-02。
- PostgreSQL，[Concurrency Control / Transaction Isolation](https://www.postgresql.org/docs/current/mvcc.html)與[Log-Shipping Standby Servers](https://www.postgresql.org/docs/current/warm-standby.html)。
- IETF，[RFC 9110: HTTP Semantics, §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)。
- RabbitMQ，[Reliability Guide](https://www.rabbitmq.com/docs/reliability)。
- AWS Prescriptive Guidance，[Transactional Outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)與[Saga Patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-patterns.html)。
- Microsoft Azure Architecture Center，[Saga](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga)、[Compensating Transaction](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction)、[Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)。
- Redis，[Distributed Locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)與[Cache-Aside](https://redis.io/docs/latest/develop/use-cases/cache-aside/)。
- Debezium，[PostgreSQL Connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)與[Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)。
- Apache Kafka，[Kafka Streams Core Concepts](https://kafka.apache.org/documentation/streams/core-concepts/)。

