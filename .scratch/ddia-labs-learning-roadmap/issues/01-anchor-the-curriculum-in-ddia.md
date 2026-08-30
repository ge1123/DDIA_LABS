# Anchor the curriculum in DDIA concepts and primary sources

Type: research
Status: resolved

## Question

依 DDIA 的概念相依性與使用者指定主題，最小而完整的 20 個 Core Lab 候選集合是什麼？請以官方書籍目錄、作者資料或其他一手資料建立概念／章節錨點，指出哪些主題必須拆開、哪些可以在不違反「一個 Lab 一個問題」下相鄰安排，並標出本書未直接規範但工程實務常用的模式。

## Answer

採用 2026 年出版的 DDIA 第二版作為概念與章節基準。20 個 Core Labs 依序涵蓋：超賣／Race Condition、Lost Update、Isolation、Write Skew、HTTP 冪等命令、MQ ACK／redelivery、Inbox、Outbox、Saga、Cache Consistency、Replication Lag、Sharding、Hot Partition、Distributed Lock、Fencing Token、Event Sourcing、Event/Schema Evolution、CDC、Stream Processing restart correctness、Event Time／out-of-order window。

交易異常、ACK／Inbox／Outbox、Sharding／Hot Partition、Lock／Fencing、stream restart／event time 必須分拆，否則會把不同 failure mechanism 與 invariant 混成一題。Idempotency Key、Inbox、Outbox、Saga 和 Cache-Aside 應標為 DDIA 問題模型上的業界模式，不能冒充書中的直接術語。

完整來源、分類、拆分理由與每題的 Broken → Correct 邊界見 [DDIA 概念錨點與 20 個 Core Labs 候選](../research/01-ddia-concept-anchors.md)。
