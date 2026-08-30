# Define the canonical Lab contract

Type: grilling
Status: resolved

## Question

每個 Lab 的最小且強制契約應是什麼，才能同時保證單一核心問題、先錯後對的教學敘事、100～300 行核心程式碼護欄，以及可重現的證據？決定必填段落、非目標、假設與 failure model、控制變因、重現與清理命令、證據接受門檻，以及超出尺寸護欄時的拆分規則。

## Answer

### Governing rule

每個 Lab 只能包含：**一個可反駁的 Question、一個主要 Invariant、一個刻意改變的 correctness mechanism**。Broken Version 和 Correct Version 必須在相同的資料、workload、併發排程或 fault injection 下比較；若修正本身必須改 schema 或基礎設施，該差異就是唯一 changed variable，其他條件保持不變並明列。

Lab 不是 production reference architecture。Correct Version 只需要在已記錄的 assumptions、failure model、workload 和環境內維持 invariant，並明確說明它沒有保證什麼。

### Required planning record

每個 Lab 在實作前，canonical Wiki page 必須完整回答：

1. **Identity**：Lab ID、短名稱、Core/Extension、狀態、前置 Lab。
2. **Problem**：一段具體情境，以及只問一件事的 Question。
3. **Invariant**：以可觀察或可執行的 predicate 表達，例如 `stock >= 0` 或「同一 `message_id` 最多提交一次 effect」。不得只寫「資料要一致」。
4. **Hypothesis**：Broken 預期如何違反 invariant；Correct 為何預期不再違反；另列能推翻假設的 observation。
5. **Concept anchor**：相關 DDIA 章節／段落；若是業界模式，分開列其一手規格或產品文件，不冒充 DDIA 術語。
6. **Non-goals**：至少列出不研究的相鄰 failure mode、效能或 production concern。
7. **Assumptions and failure model**：參與者、交易或訊息邊界，以及本 Lab 主動控制的 concurrent interleaving、timeout、crash point、duplicate、delay、clock 或 partition 行為。
8. **Experiment design**：唯一 changed variable、controlled variables、synthetic fixture／dataset、workload seed、併發度、量測與單位、warm-up、run count、timeout／stop condition、已知 confounders。
9. **Safety boundary**：明確的 Compose project/resource names、資料範圍與 bounded cleanup；不得依賴未記錄的互動狀態、production credential 或 production data。
10. **Expected observation**：Broken 與 Correct 各自應看到的狀態、計數、錯誤或時序；process exit code 本身不是 observation。
11. **Exact entry points**：逐字列出 setup、Broken reproduction、Correct verification、inspect/result regeneration 和 cleanup 命令，以及預期 exit semantics。
12. **Evidence and conclusion**：implementation、tests、stable result summary、raw result regeneration；分開記錄 Verified facts、Reasonable inferences、Open questions、衝突結果與適用限制。

缺少 Question、Invariant、rejection observation、failure model、changed/control variables、reproduce 或 cleanup 中任一項時，不得開始實作。

### Required Broken → Correct learning flow

每個 Lab 的 README 與測試名稱依序呈現：

1. **Problem**：為何直覺作法看似合理。
2. **Invariant**：什麼條件絕對不能被破壞。
3. **Broken Version**：最小不安全機制；註解說明故意保留的缺陷，不加入第二個 bug。
4. **Reproduce**：以 barrier、fixture、可指定的 crash point 或可重播的 seed 優先建立 deterministic counterexample；隨機 sleep 或人工狂按 API 不能是唯一重現方式。
5. **Why it breaks**：用實際 operation/interleaving/commit 順序解釋因果，不只寫 framework 名稱或 isolation level。
6. **Correct Version**：只改變目標 mechanism，並明列新增的 constraint、retry、dedup、transaction boundary、token 或 routing rule。
7. **Verify**：用與 Broken 相同的輸入與 failure model 執行，檢查 invariant，而非只檢查 HTTP 2xx 或程序成功結束。
8. **Limits**：記錄修正仍不涵蓋的故障與不應外推的結論。

### API and code-size guardrails

- 一個 Lab 對外最多 **1～3 支 API，為 Broken 與 Correct 合計**；預設使用明確的 `/broken` 與 `/correct` 路徑，第 3 支僅保留給觀察狀態。reset/setup 優先由 test harness、fixture 或 bounded script 完成，不為了湊 CRUD 增加 endpoint。
- 不建立會員、登入、後台、前端、通用 repository/service layer 或與 invariant 無關的 CRUD。health check 若不是研究對象，不應占用額外 application endpoint；容器可用 dependency-native readiness check。
- **核心程式碼 100～300 行是目標範圍，且 Broken＋Correct 合計計算，不是各 300 行。**計入承載研究機制的手寫 endpoint/handler、SQL、transaction、consumer/relay 與最小 orchestration；不計生成檔、migration metadata、Compose、fixtures、tests、using/import、空白與註解。
- 少於 100 行且問題已清楚時保留簡潔，不得為達行數而抽象化。超過 300 行時必須在 Lab page 說明不可分割原因並進行拆分檢查。
- Shared code 不能包含本 Lab 正在比較的 correctness mechanism；否則 Broken 與 Correct 的差異會被隱藏。可共用的內容及上限由 `Choose the monorepo execution model` 決定。

### Evidence acceptance

| Evidence target | Minimum acceptance |
| --- | --- |
| Broken counterexample | 在文件化的 controlled run 中觀察到 invariant violation，並保存足以辨識實際狀態／次數／順序的輸出。若宣稱 deterministic，CI proof run 必須每次重現；若本質上 probabilistic，必須說明機率、run count 和不確定性。 |
| Correct invariant | 使用同一 fixture、workload 與 failure model，在預先宣告的有限 run count 內為零 invariant violations；不得把「尚未觀察到」寫成普遍證明。 |
| Correct mechanism | 至少一個自動化測試直接檢查 invariant 或 durable effect；只 assert HTTP status、message received 或 process exit code 不足。 |
| Failure behavior | fault 必須可控制、blast radius 有界、反應可觀察，且 cleanup 可重跑。setup/measurement defect 的結果標為 Invalid，不算支持或反駁 hypothesis。 |
| Performance claim | 只有當 hypothesis 涉及吞吐、延遲、skew、stampede 或 backpressure 時才加入 warm-up、重複 runs、units、variability 與 k6/等價 workload；correctness Lab 不必為了好看加入 benchmark。 |
| Retained evidence | Git 只保留小型穩定 summary、fixture 與再生命令；記錄 commit、OS/architecture、版本、image digest、seed、concurrency、run count 和異常。 |

通用 run count 或 timeout 不在此票硬編一個數字；`Define the evidence and acceptance matrix` 依 concurrency、message delivery、crash recovery、replication、performance 和 stream semantics 分類設定。每個 Lab 必須在執行前選定適用類別與門檻。

### Mandatory split rules

符合下列任一條件時，預設拆成兩個 Labs；只有能證明兩部分共享同一 causal mechanism 和同一 invariant 時才例外：

- 標題必須用「and／與」連接兩個可獨立失敗的概念。
- 需要兩個彼此獨立的 invariants 或 rejection observations。
- Broken Version 同時故意保留兩個主要 bug，移除其中一個仍可重現另一種 violation。
- Correct Version 必須同時教授兩個可獨立選擇的 correctness mechanisms。
- Broken 與 Correct 無法使用同一主要 workload 或 failure model 比較。
- API 超過 3 支，或 Broken＋Correct 核心程式碼超過 300 行，且多出的部分不是不可避免的 protocol boundary。
- 讀者必須先理解尚未教過的外部系統語義，才能判讀本 Lab 的主要 observation；先建立前置 Lab 或將比較移到 Extension Lab。

### Status and exit conditions

- **Proposed**：上述設計欄位完整，但尚未執行。
- **Pending**：已有實作或 run，但 acceptance evidence 尚不完整。
- **Partial**：只對明確列出的子範圍有足夠 evidence。
- **Verified**：Broken counterexample、Correct invariant、reproduction/cleanup 與 scoped conclusion 都通過 acceptance criteria。
- **Outdated**：watched code、dependency、fixture、workload 或 configuration 改變後尚未重驗。

Lab contract 在第一個 executable Lab 完成後必須回顧；若實際證據顯示某欄位無法操作或不足，更新 canonical Wiki contract、source ledger 與 change log，不把 Proposed contract 誤標為 Verified。
