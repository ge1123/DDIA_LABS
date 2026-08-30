# Assemble the implementation-ready curriculum blueprint

Type: prototype
Status: resolved
GitHub: https://github.com/ge1123/DDIA_LABS/issues/8

## Question

最終課程藍圖應如何呈現，才能讓讀者在數十秒內看懂每個 Lab 研究的問題，又能直接交給後續實作者？請整合已決定的排序、Lab contract、技術矩陣、repo 結構與證據標準，為每個 Core/Extension Lab 填入 Problem、Invariant、Broken Version、重現、Correct Version、驗證、API 預算、技術和前置 Lab，並明確標示 Verified fact、Reasonable inference 與 Open question。

## Answer

### Verdict

採用 **「五階段 30 秒總覽＋每 Lab 一份完整 implementation packet」**。總覽只保留 ID、問題、Invariant、Broken → Correct、Profile、技術與先修；後半部再以固定欄位提供 Data/API、deterministic workload 或 fault、direct proof、limits 和 evidence strength。這結合 prototype Variant A 的路徑可掃描性與 Variant C 的交付完整度；不採超寬 evidence matrix 作主要入口。

正式 canonical page 是 [`wiki/labs/curriculum-blueprint.md`](../../../wiki/labs/curriculum-blueprint.md)。它涵蓋 20 Core 與 E01～E05，所有 Lab 都已選定：

- 一個可反駁的 Problem／Question 與一個 executable invariant；
- 最小資料形狀與 Broken／Correct 合計 1～3 支 API；
- 同 fixture 下的 Broken mechanism、唯一 changed variable 與 Correct mechanism；
- deterministic barrier、fault point、seed、concurrency 或 performance workload；
- direct invariant proof、evidence profile／modifier、run gates 與 timeout；
- 最小技術、Compose 邊界、前置 Lab、non-goals、confounders 與 100～300 行預算。

### Final technical decisions

- Lab 11 使用真實 PostgreSQL physical streaming standby；以暫停 WAL replay 建立 deterministic lag，不用人工 sleep 冒充產品複寫行為。
- Lab 19 使用 Kafka 單 partition input，加上 PostgreSQL 同一 transaction 內的 checkpoint、state 與 output；Kafka committed offset 只是提示。結論只稱 database-visible effectively-once，禁止宣稱 Kafka 或端到端 exactly-once。
- Lab 20 沿用 Lab 19 的 transaction boundary，只更換 .NET event-time policy；Kafka 只作 ordered input log，不引入 Kafka Streams／JVM application。
- E02 唯一變因是 per-key single-flight；TTL jitter 移出本 Lab。
- E05 唯一 correctness 變因是 resource-side assignment epoch fence；stop／drain 在兩版都只是 best effort。
- Wiki 不預先建立 25 張薄頁。藍圖是規劃期 canonical page；每張 Lab 進入實作時，再由其 packet 建立獨立 canonical Lab page 並加入實際 evidence。

### Prototype result

- Branch: `codex/prototype-curriculum-blueprint`
- Commit: `d5547aa`
- Artifact: `.scratch/prototypes/issue-08-curriculum-blueprint.prototype.html`
- Three variants: learning journey、evidence matrix、implementation packet。
- Structural check: 25 Lab records，三種 URL-stable variants，filter／selection state visible，JavaScript syntax valid。

### Evidence strength

**Verified fact:** DDIA／產品一手來源支持概念與產品語義；Issues 01～07 已接受 25 張邊界、先修、技術政策、Lab contract 與 evidence profiles。

**Reasonable inference:** 本票選定的 exact APIs、fixtures、thresholds、barriers、fault schedules、line budgets 與「總覽＋packet」資訊架構，都是尚待實作驗證的課程設計。

**Open at implementation:** 只剩 exact optional-product pins、Docker fault 可攜性、reference-runner calibration，以及每張 Lab 的第一份 accepted evidence。沒有剩餘的課程層級設計選擇。
