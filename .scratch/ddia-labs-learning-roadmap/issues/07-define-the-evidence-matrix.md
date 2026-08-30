# Define the evidence and acceptance matrix

Type: grilling
Status: resolved
GitHub: https://github.com/ge1123/DDIA_LABS/issues/7

## Question

不同類型的 invariant violation 應以何種最小證據驗收修正有效？建立 deterministic integration test、並行測試、故障注入、Testcontainers、k6 與 retained result summary 的選用矩陣，並決定反例重現率、correct run 次數、timeout、環境紀錄和 flaky-test 處理門檻。

## Answer

採用 **七種 evidence profiles**。每個 Lab 在實作前選一個主要 profile；若提出效能 claim，另外套用 performance 規則。工具不是驗收本身，直接檢查 invariant 的 observation 才是。

### Default profiles and numeric gates

| Profile | Planned Labs | Broken minimum | Correct minimum | Per-run deadline | Whole proof ceiling |
| --- | --- | --- | --- | --- | --- |
| D — Deterministic transformation | 10, 12, 16, 17 | 3／3 controlled runs 重現同一 predicate violation | 10／10，同 fixtures，零 violation | 30 秒 | 5 分鐘 |
| C — Controlled concurrency | 01–04, 14–15 | 5／5 barrier-controlled schedules 重現 violation | 25／25，同 schedule family，零 violation | 60 秒 | 10 分鐘 |
| M — Message delivery／workflow | 05–09 | 5／5 固定 command/message ID 與 failure point 重現錯誤 durable effect | 20／20，同 retry／duplicate／failure schedule，零 violation | 90 秒 | 15 分鐘 |
| R — Replication behavior | 11, E03 | 3／3 受控 lag 或 primary-loss runs 重現舊讀／acknowledged-write loss | 10／10，同 observation point／promotion procedure，零 violation | 180 秒 | 20 分鐘 |
| X — Crash／restart recovery | 18, 19, E04 | 3／3 在 named checkpoint／offset／LSN fault point 重現 gap、duplicate 或 latency-budget violation | 10／10，同 fault schedule，correctness 零 violation | 180 秒 | 20 分鐘 |
| P — Performance／comparative degradation | 13, E01, E02 | 1 次 warm-up 後 5 次 measured runs；baseline 至少 4／5 違反預先宣告門檻 | 5 次 measured runs；correctness 5／5，correct 至少 4／5 通過門檻 | 每次 5 分鐘 | 45 分鐘 |
| S — Stream time／ownership | 20, E05 | 5／5 固定 event／partition fixture 重現錯誤 window 或 stale-owner commit | 20／20，同 watermark／rebalance schedule，零 violation | 120 秒 | 20 分鐘 |

Readiness、fixture reset 和 bounded cleanup 在每個 run 前後驗證。第一次 image pull／package restore 不計入 proof deadline；`setup` 預設上限 10 分鐘。任何較寬 deadline 必須在執行前寫入 Lab page 並說明原因，不能看到 timeout 後再調整門檻。

Timeout 預設代表 **Invalid evidence**，同時令 CI 失敗；只有當「在期限內完成／拒絕」本身就是預先宣告的 invariant 時，timeout 才能成為 Rejected 或 Verified observation。

### Performance acceptance

- 固定 dataset、seed、concurrency、arrival model、duration、warm-up、hardware class 和唯一 changed variable。
- 每個 variant 先 warm-up 一次，再交錯執行五次，避免把時間順序當成機制差異。
- 比較型 claim 需同時滿足：主要指標方向在至少 4／5 paired runs 一致、median 改善至少 20%，且每個 variant 的主要指標跨 run coefficient of variation 不超過 15%。否則結論為 Inconclusive。
- absolute latency／throughput budget 只有在記錄的 reference runner 上作 gating；其他硬體只要求 correctness 相同並把效能結果標為 informational。
- p95／p99、throughput、retry／abort、skew 或 origin amplification 依 hypothesis 擇一為 primary metric；其餘是 diagnostics，不能事後挑最好看的指標。
- Correct 的效能勝出不能抵銷任何 correctness violation。

### Probabilistic exception

優先使用 barrier、named fault point、fixed event sequence 或可重播 seed。只有無法合理建立 deterministic trigger 時才可申請 probabilistic evidence：

- Lab page 必須先說明 deterministic control 為何會改變研究對象，並固定 seed distribution。
- Broken 至少執行 50 次，且 violation 至少 20／50，95% Wilson lower bound 仍須不低於 20%。
- Correct 至少執行 100 次且零 violation；結論必須明列「零觀察不等於證明」，其 95% 上界約為 3%。
- 不得把未宣告的偶發失敗事後改稱 probabilistic behavior。

### Tool selection

| Tool／method | Required when | Not sufficient or not required |
| --- | --- | --- |
| Deterministic integration test | 每個 Lab 至少一個 assertion 直接檢查 invariant／durable effect | 只檢查 HTTP status、message receipt 或 exit code 不足 |
| Barrier／controlled scheduler | C profile，以及需要固定 interleaving 的 E01 correctness guard | random sleep 或人工重試不能作唯一 trigger |
| Compose fault harness | 指定 consumer／relay／worker crash、replica loss、pause、network cut 或 rebalance | fault 必須只作用於該 Lab 的 Compose project |
| Testcontainers | 每個測試需要 fresh real dependency、平行 CI 隔離或程式化 restart／crash，且 Compose harness 無法穩定提供時 | 不是所有 integration tests 的預設；必須使用與 Compose 相同的 pinned image |
| k6／等價 driver | 外部 HTTP concurrency、throughput、tail latency、hot partition、stampede 或 backpressure 是 primary observation | correctness-only Lab 不加入 benchmark |
| `results/accepted.json` | 每個達到 Partial／Verified 的 Lab | 大型 raw log、trace 或 machine-specific dump 不提交 Git |

Fault-harness modifier 強制套用於 06、08、09、11、14、15、18、19、E03、E04、E05。E04 以 X 為主要 profile，另套用 performance comparison 規則；效能比較不得掩蓋任何 relay recovery violation。

### Retained evidence contract

每個 accepted summary 至少記錄：schema version、Lab ID、commit、timestamp、verdict、profile、exact commands、OS／architecture、CPU／memory class、`.NET`／Docker／Compose versions、resolved image digests、fixture hash、seed、concurrency、run counts、deadlines、fault point、Broken／Correct observations、每次 run 的 primary result、anomalies、confounders 與 regeneration command。README／Wiki 只解釋結論並連到該小型 JSON；大型 raw output 由命令再生。

Verdict 只能是 `Verified`、`Partial`、`Inconclusive`、`Rejected` 或 `Invalid`，且必須與 Wiki status 的明確 scope 一致。

### Flaky-test policy

- Acceptance run **不自動重試**。第一次失敗必須保存；診斷可用同 seed 重跑一次，但重跑成功不能把原結果改綠。
- 同一 commit、environment、fixture 和 seed 出現 pass／fail 混合，即確認為 flaky。該 evidence 立即失效，Lab 不得維持 Verified，並建立 problem／issue 記錄。
- Quarantine 只能把測試移到獨立 job 以維持其他診斷訊號；不得 skip、允許失敗或從 required checks 移除。
- 修正後，D／C／M／S profile 必須連續 50 次通過，R／X profile 連續 20 次通過；另將原始 failing seed／fault point 重跑 10 次。P profile 重新完成整套 1 warm-up + 5 measured paired runs。
- readiness 未達、cleanup 失敗、port／volume／topic 污染、clock 或 runner overload 都標為 Invalid setup，不算支持或反駁 hypothesis，但仍令 CI 失敗。

### CI and cross-Lab execution

- 允許根目錄 `./lab all check`，只發動每個 Lab 的 fast deterministic checks；`all` 不接受 `broken`、`correct`、`inspect` 或 `cleanup`。
- Discovery 只掃描 `experiments/*/lab.sh`，directory ID 必須與 script 宣告 ID 相同；不新增 root manifest 或 shared test project。
- 預設循序執行；CI 可設定 `DDIA_LAB_JOBS=2`，不得更高。每個 Lab 完成後都嘗試 bounded cleanup。
- Aggregate report 列出 Lab ID、status、duration、first failure 和 cleanup status；所有 Labs 都執行完才以 non-zero 結束，不因第一個失敗遺失其他訊號。
- Pull request 執行 `all check`，並對 changed Labs 執行其完整 profile proof。global pin／dispatcher／evidence policy 改變時，所有受影響 Labs 重跑完整 proof。
- R、X、P 的完整 proof 可在 reference runner／接受前 job 執行，不用把長時間或硬體敏感量測塞進每次 smoke；未通過完整 proof 的 Lab 不得標為 Verified。

### Evidence strength

**Verified fact:** 現有 Wiki policy、Lab contract 與 technology baseline 已要求 deterministic setup、直接 invariant assertion、受控 fault、效能 variability、版本／digest／seed 記錄，以及工具按需升級。

**Reasonable inference:** 上述數字是在尚無 executable Labs 時選定的保守起始門檻，足以防止單次偶然成功被誤認為證據，同時讓本機課程仍可運行。

**Open question:** 第一個 executable Lab 必須驗證這些 run counts、deadlines、JSON schema 與 `all check` 是否可操作。若實測成本或錯誤分類不合理，透過新決策調整，不事後修改已執行 Lab 的 acceptance gate。
