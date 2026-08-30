# Choose the monorepo execution model

Type: prototype
Status: resolved
GitHub: https://github.com/ge1123/DDIA_LABS/issues/4

## Question

monorepo 應採用哪一種最小結構和執行介面，才能讓每個 Lab 完全獨立、可單獨啟停與清理，又不建立會遮蔽研究機制的大型 Shared Infrastructure？請用一個代表性 Lab 的粗略目錄樹與命令介面比較方案，決定 solution/project 邊界、Compose 所屬位置、共用檔案上限與根目錄便利命令。

## Answer

### Decision

採用 **每 Lab 自有邊界＋薄根目錄入口**：每個 Lab 擁有自己的 solution、Compose project、執行腳本、資料生命週期與證據；repository 根目錄只提供 SDK／編譯政策與單一 Lab 的命令轉交，不提供共用 runtime、資料庫、測試 fixture 或 correctness helper。

~~~text
DDIA_LABS/
├─ global.json
├─ Directory.Build.props
├─ lab                         # thin dispatcher: one Lab, one action
└─ experiments/
   └─ 01-race-condition/
      ├─ 01-race-condition.slnx
      ├─ compose.yaml
      ├─ lab.sh                # authoritative action implementation
      ├─ README.md
      ├─ src/
      │  └─ RaceCondition.Api/
      ├─ tests/
      │  └─ RaceCondition.Tests/
      ├─ fixtures/             # only when required
      └─ results/              # only small stable summaries
~~~

### Boundary rules

- 不建立 root solution。每個 Lab 的 restore、build 與 test graph 必須能獨立解析，避免修改或執行一個 Lab 時載入其他 Labs。
- 預設每個 Lab 一個 API project 加一個 test project。只有 producer、consumer 或 relay 等獨立 process boundary 本身是研究語意時，才增加 executable project。
- Broken 與 Correct Version 預設放在同一個 Lab、同一個 API project，使用同一 fixture 與 workload；不得拆成兩套會自行漂移的基礎設施。
- 每個 Lab 的 `compose.yaml` 與 `lab.sh` 放在 Lab 根目錄。Compose project name 固定為 `ddia-lab-<id>`；network、volume 與可覆寫的 host ports 都由該 Lab 擁有，不使用跨 Lab 的共享 Compose stack。
- Cleanup 必須以該 Lab 的固定 Compose project 為界，執行 `down --volumes --remove-orphans`；不得掃描或刪除 repository 之外的容器、volume 或資料。
- 相依套件與 container image 在 Lab 內精確 pin。更新 root SDK policy 不等同於 Lab evidence 仍然有效，watched paths 改變後仍須重驗。

### Command interface

根目錄介面固定為：

~~~text
./lab <lab-id> setup
./lab <lab-id> broken
./lab <lab-id> correct
./lab <lab-id> inspect
./lab <lab-id> check
./lab <lab-id> cleanup
~~~

根 `lab` 只能驗證 `<lab-id>` 與 action，接著 `exec` 對應 Lab 的 `lab.sh`。它不得持有 Docker、SQL、migration、workload、assertion 或 cleanup 邏輯。`lab.sh` 是命令語意的唯一來源，Lab README 同時列出根目錄入口與可直接執行的本地命令。

Issue 07 完成後只接受 `./lab all check`：依 `experiments/*/lab.sh` discovery，預設循序、最多兩 workers，彙總所有失敗並逐 Lab cleanup。`all` 不得執行 `broken`、`correct`、`inspect` 或 `cleanup`，避免誤導為所有 Lab 共用生命週期。

### Shared-file ceiling

執行模型最多允許三個 repository-wide policy／convenience files：

1. `global.json`：精確 pin .NET SDK。
2. `Directory.Build.props`：僅 compiler、nullable、warnings 等不承載 Lab 語意的建置政策。
3. `lab`：單一 Lab 命令的薄 dispatcher。

Shared runtime libraries、共用資料庫／broker stack、共用 migration、共用 test fixture、共用 domain model 與 correctness helpers 的上限為 **零**。小量重複優先於隱藏 failure mechanism。若未來確實需要第 4 個 shared execution file 或任何 shared code project，必須以新 decision 記錄它消除的重複、未隱藏的語意與使決策失效的條件。

### Alternatives considered

| Model | Result | Reason |
| --- | --- | --- |
| Root solution + shared infrastructure | Rejected | 命令一致，但 cleanup、版本與資料生命週期互相耦合；helper 容易遮蔽研究機制 |
| Per-Lab boundary + thin root dispatcher | Accepted | 保留單一入口與獨立生命週期，runtime 和 evidence 仍由 Lab 擁有 |
| Fully standalone Labs without root convention | Rejected | 隔離良好，但 20 個 Labs 的命令與結構容易漂移，讀者與 CI 必須重複發現入口 |

### Prototype record and evidence strength

- Prototype branch: `codex/prototype-monorepo-execution-model`
- Prototype commit: `ff3b96c`
- The prototype compares cleanup isolation, root-command consistency, and shared-runtime visibility. It is a design probe, not evidence that Docker or .NET execution has already succeeded.
- **Verified fact:** the current repository has no executable Lab or shared runtime infrastructure, and the comparison artifact is retained at the commit above.
- **Reasonable inference:** the accepted model best satisfies the stated isolation and discoverability constraints with the fewest repository-wide execution files.
- **Open question:** the first executable Lab must validate shell portability, Compose project isolation, port overrides, cleanup idempotence, and whether the three-file ceiling is operationally sufficient.
