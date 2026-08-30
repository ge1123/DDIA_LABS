# DDIA Labs

這個 repository 用可重現的小型實驗學習 *Designing Data-Intensive Applications*（DDIA）。
重點不是完成單一產品，而是把書中的模型、取捨與失敗模式轉成可以觀察、測量、反駁的工程證據。

## Wiki-first

每次閱讀、設計或實作前，先從 [wiki/index.md](wiki/index.md) 進入：

1. 找到對應的概念、Lab、流程或 QA 頁面。
2. 檢查頁面的 Status，以及 [wiki/source.md](wiki/source.md) 的證據覆蓋範圍。
3. 先寫問題、假設、預期結果與量測方式，再開始實作。
4. 實驗完成後補上命令、結果、限制與可重現證據。
5. 明確區分 Verified fact、Reasonable inference 與 Open question。

Wiki 是知識入口與證據索引，不取代書籍、程式碼、測試、benchmark 原始結果或正式設計決策。

## 學習範圍

學習路徑依 DDIA 的三個主題群組循序展開：

- Foundations：可靠性、可擴展性、可維護性、資料模型、儲存與編碼。
- Distributed data：複製、分割、交易、分散式系統困難與一致性。
- Derived data：批次、串流，以及由資料流衍生系統狀態。

這是主題導航，不是逐章內容的替代品。書籍內容只記錄定位資訊與自己的摘要，不大量抄錄原文。

## Repository layout

| Path | Purpose |
| --- | --- |
| `wiki/` | 概念、Lab 設計、流程、QA、問題與證據索引 |
| `experiments/` | 可執行實驗及其就近 README |
| `wiki/source.md` | Wiki 知識與實作證據的覆蓋 ledger |
| `wiki/log.md` | 重要知識、架構與證據狀態變更 |

目前完成的是 Wiki-first 基線；實驗技術與語言在具體 Lab 被定義時再決定。

