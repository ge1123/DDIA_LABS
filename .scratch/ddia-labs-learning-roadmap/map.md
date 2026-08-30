# DDIA Labs：從失敗到證據的迷你專案學習路線

Type: wayfinder:map
Status: resolved
GitHub: https://github.com/ge1123/DDIA_LABS/issues

## Destination

產出一份可直接逐 Lab 實作的課程藍圖：單一 GitHub monorepo、20 個 Core Labs 加 4～6 個 Extension Labs，依學習相依性由簡到難排列。每個 Lab 都必須明確列出單一 Problem、Invariant、Broken Version、重現方式、Correct Version、驗證證據、技術與前置 Lab，足以讓後續實作以一個 Lab 一個小型變更展開。

## Notes

- Domain: DDIA 概念、資料一致性、資料庫交易與分散式系統的可重現學習實驗。
- Consult: `domain-modeling`, `research`, `prototype`; 遇到真正需要使用者取捨時才使用 `grilling`。
- 使用者已授權代理先做後續設計判斷，最後以完整結果供其審閱。
- 固定選擇：20 個 Core Labs；另有 4～6 個 Extension Labs；Broken/Correct 在同一 Lab 並列；每 Lab 自帶 Docker Compose。GitHub Issues #1～#8 是工作流程 tracker，本地 Markdown 保留完整設計紀錄與 GitHub URL。
- 預設技術：.NET / ASP.NET Core、PostgreSQL、Docker Compose；只有當研究問題本身需要時才加入 Redis、RabbitMQ/Kafka、Testcontainers 或 k6。
- 尺寸護欄：每 Lab 1 個核心問題、1～3 支 API、核心程式碼目標 100～300 行；不得靠會員、後台、前端或一般 CRUD 增加情境。
- 學習節奏固定為：先做錯 → 重現 bug → 解釋機制 → 最小修正 → 以測試或壓測驗證。
- 本 map 只處理課程藍圖決策，不實作 executable Labs。

## Decisions so far

- [Anchor the curriculum in DDIA concepts and primary sources](issues/01-anchor-the-curriculum-in-ddia.md): 以 DDIA 第二版為概念基準，採 20 個不可再合併而不混淆 failure mechanism 的 Core Labs，並清楚區分 DDIA 直接概念與業界模式。
- [Choose the reproducible technology baseline](issues/02-choose-the-technology-baseline.md): 預設 .NET 10 LTS、PostgreSQL 18 與逐 Lab Docker Compose；精確 pin 版本／digest，其他服務只按語意或證據需求升級。
- [Define the canonical Lab contract](issues/03-define-the-canonical-lab-contract.md): 每個 Lab 固定為一個可反駁問題、一個 invariant 與一個主要變因，Broken/Correct 共用 workload，並以明確 API、行數、證據與拆分門檻守住範圍。
- [Choose the monorepo execution model](issues/04-choose-the-monorepo-execution-model.md): 每個 Lab 自有 solution、Compose、資料生命週期與 authoritative `lab.sh`；根目錄最多以 `global.json`、`Directory.Build.props` 與薄 `lab` dispatcher 提供共同政策，不建立 shared runtime。
- [Sequence the 20 Core Labs by learning prerequisites](issues/05-sequence-the-core-learning-path.md): 採五階段、20 節點、28 條向前相依的 Core path；編號是降低 context switching 的建議線性順序，DAG 只記錄判讀 observation 真正需要的先修概念。
- [Choose the advanced Extension Labs](issues/06-choose-the-extension-labs.md): 採五張不進入 Core 先修的 Extension Labs，配比為兩張替代機制比較、兩張真實故障與一張效能退化；環境仍限本機 Compose，且每張最多兩類有狀態外部系統。
- [Define the evidence and acceptance matrix](issues/07-define-the-evidence-matrix.md): 將 25 張 Labs 分配到七種 evidence profiles，固定 Broken／Correct 次數、逾時、效能 variability、probabilistic 例外與 flaky-test 門檻，並允許最多兩 worker 的 `./lab all check`。
- [Assemble the implementation-ready curriculum blueprint](issues/08-assemble-the-implementation-ready-blueprint.md): 採「五階段總覽＋每 Lab 實作包」呈現 25 張藍圖，定案逐張 API、資料、工作負載、fault、技術與證據；不再留下課程層級的未決設計。

## Remaining implementation work

- 依藍圖逐張建立 executable Lab；開始實作時才從藍圖 packet 建立該 Lab 的獨立 canonical Wiki page，避免預先產生 25 張沒有證據的重複頁。
- 由第一張使用 performance profile 的 Lab 建立 reference runner 規格，任何 threshold calibration 都保留原始結果，不回寫成已驗證事實。
- CI workflow 與實際 `./lab all check` runner 留到 executable Labs 階段；課程藍圖本身已完成。

## Out of scope

- 實作任何 executable Lab、共用框架或產品功能；這些屬於藍圖完成後的交付階段。
- 雲端部署、Kubernetes、會員、管理後台、前端 UI、一般用途 CRUD 與 production hardening。
- 用單機或單一 workload 的結果宣稱普遍效能或 production correctness。
