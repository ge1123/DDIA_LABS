# DDIA Labs：從失敗到證據的迷你專案學習路線

Type: wayfinder:map
Status: open

## Destination

產出一份可直接逐 Lab 實作的課程藍圖：單一 GitHub monorepo、20 個 Core Labs 加 4～6 個 Extension Labs，依學習相依性由簡到難排列。每個 Lab 都必須明確列出單一 Problem、Invariant、Broken Version、重現方式、Correct Version、驗證證據、技術與前置 Lab，足以讓後續實作以一個 Lab 一個小型變更展開。

## Notes

- Domain: DDIA 概念、資料一致性、資料庫交易與分散式系統的可重現學習實驗。
- Consult: `domain-modeling`, `research`, `prototype`; 遇到真正需要使用者取捨時才使用 `grilling`。
- 使用者已授權代理先做後續設計判斷，最後以完整結果供其審閱。
- 固定選擇：20 個 Core Labs；另有 4～6 個 Extension Labs；Broken/Correct 在同一 Lab 並列；每 Lab 自帶 Docker Compose；先用 local-markdown tracker，GitHub repo 可用後再遷移。
- 預設技術：.NET / ASP.NET Core、PostgreSQL、Docker Compose；只有當研究問題本身需要時才加入 Redis、RabbitMQ/Kafka、Testcontainers 或 k6。
- 尺寸護欄：每 Lab 1 個核心問題、1～3 支 API、核心程式碼目標 100～300 行；不得靠會員、後台、前端或一般 CRUD 增加情境。
- 學習節奏固定為：先做錯 → 重現 bug → 解釋機制 → 最小修正 → 以測試或壓測驗證。
- 本 map 只處理課程藍圖決策，不實作 executable Labs。

## Decisions so far

- [Anchor the curriculum in DDIA concepts and primary sources](issues/01-anchor-the-curriculum-in-ddia.md): 以 DDIA 第二版為概念基準，採 20 個不可再合併而不混淆 failure mechanism 的 Core Labs，並清楚區分 DDIA 直接概念與業界模式。
- [Choose the reproducible technology baseline](issues/02-choose-the-technology-baseline.md): 預設 .NET 10 LTS、PostgreSQL 18 與逐 Lab Docker Compose；精確 pin 版本／digest，其他服務只按語意或證據需求升級。
- [Define the canonical Lab contract](issues/03-define-the-canonical-lab-contract.md): 每個 Lab 固定為一個可反駁問題、一個 invariant 與一個主要變因，Broken/Correct 共用 workload，並以明確 API、行數、證據與拆分門檻守住範圍。

## Not yet specified

- 每個 Lab 的具體 API 名稱、資料形狀與 deterministic workload；必須等 Lab 邊界和排序確定後才能逐一收斂。
- Wiki 中需要新增哪些 concept pages、Lab registry entries 與 source-ledger slices；必須等最終課程清單確定。
- 根目錄的一鍵執行介面與 CI matrix；必須等 monorepo execution model 和 Lab 技術矩陣確定。
- local-markdown tickets 遷移為 GitHub sub-issues 與 native dependencies 的方式；等遠端 repository 可存取後處理。

## Out of scope

- 實作任何 executable Lab、共用框架或產品功能；這些屬於藍圖完成後的交付階段。
- 雲端部署、Kubernetes、會員、管理後台、前端 UI、一般用途 CRUD 與 production hardening。
- 用單機或單一 workload 的結果宣稱普遍效能或 production correctness。
