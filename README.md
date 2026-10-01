# DDIA 第二版學習 Roadmap

本專案依 [Vonng 的 DDIA 第二版繁體中文講義目錄](https://ddia.vonng.com/tw/toc/) 編制，沿用講義的篇章分組、章名、章內小節名稱與閱讀順序。後續講解、筆記與 labs 都以此結構為準，重要名詞搭配英文說明。

## 目錄

講義提供 [完整目錄](https://ddia.vonng.com/tw/toc/)，包含插圖目錄、表格目錄與示例目錄。

## 序言

[閱讀序言](https://ddia.vonng.com/tw/preface/)

- 本書的目標讀者
- 本書涉及的領域
- 本書綱要
- 參考文獻與延伸閱讀
- O‘Reilly Safari
- 聯絡我們
- 致謝

## I 資料系統基礎

[閱讀本篇導讀](https://ddia.vonng.com/tw/part-i/)

### 1 資料系統架構中的權衡

[閱讀第 1 章](https://ddia.vonng.com/tw/ch1/)

- 分析型與事務型系統
- 雲服務與自託管
- 分散式與單節點系統
- 資料系統、法律與社會
- 總結

### 2 定義非功能性需求

[閱讀第 2 章](https://ddia.vonng.com/tw/ch2/)

- 案例研究：社交網路首頁時間線
- 描述效能
- 可靠性與容錯
- 可伸縮性
- 可維護性
- 總結

### 3 資料模型與查詢語言

[閱讀第 3 章](https://ddia.vonng.com/tw/ch3/)

- 關係模型與文件模型
- 圖資料模型
- 事件溯源與 CQRS
- 資料框、矩陣與陣列
- 總結

### 4 儲存與檢索

[閱讀第 4 章](https://ddia.vonng.com/tw/ch4/)

- OLTP 系統的儲存與索引
- 分析型資料儲存
- 多維索引與全文索引
- 總結

### 5 編碼與演化

[閱讀第 5 章](https://ddia.vonng.com/tw/ch5/)

- 編碼資料的格式
- 資料流的模式
- 總結

## II 分散式資料

[閱讀本篇導讀](https://ddia.vonng.com/tw/part-ii/)

導讀小節：伸縮至更高的負載。

### 6 複製

[閱讀第 6 章](https://ddia.vonng.com/tw/ch6/)

- 單主複製
- 複製延遲的問題
- 多主複製
- 無主複製
- 總結

### 7 分片

[閱讀第 7 章](https://ddia.vonng.com/tw/ch7/)

- 分片的利與弊
- 鍵值資料的分片
- 請求路由
- 分片與二級索引
- 總結

### 8 事務

[閱讀第 8 章](https://ddia.vonng.com/tw/ch8/)

- 事務到底是什麼？
- 弱隔離級別
- 可序列化
- 分散式事務
- 總結

### 9 分散式系統的麻煩

[閱讀第 9 章](https://ddia.vonng.com/tw/ch9/)

- 故障與部分失效
- 不可靠的網路
- 不可靠的時鐘
- 知識、真相和謊言
- 總結

### 10 一致性與共識

[閱讀第 10 章](https://ddia.vonng.com/tw/ch10/)

- 線性一致性
- ID 生成器和邏輯時鐘
- 共識
- 總結

## III 派生資料

[閱讀本篇導讀](https://ddia.vonng.com/tw/part-iii/)

導讀小節：

- 記錄系統和派生資料系統
- 章節概述
- 索引

### 11 批處理

[閱讀第 11 章](https://ddia.vonng.com/tw/ch11/)

- 使用 Unix 工具的批處理
- 分散式系統中的批處理
- 批處理模型
- 批處理用例
- 本章小結

### 12 流處理

[閱讀第 12 章](https://ddia.vonng.com/tw/ch12/)

- 傳遞事件流
- 資料庫與流
- 流處理
- 本章小結

### 13 流式系統的哲學

[閱讀第 13 章](https://ddia.vonng.com/tw/ch13/)

- 資料整合
- 分拆資料庫
- 追求正確性
- 本章小結

### 14 做正確的事情

[閱讀第 14 章](https://ddia.vonng.com/tw/ch14/)

- 預測分析
- 隱私與追蹤
- 總結

## 術語表

[查閱術語表](https://ddia.vonng.com/tw/glossary/)

## 索引

[查閱索引](https://ddia.vonng.com/tw/indexes/)

## 後記

[閱讀後記](https://ddia.vonng.com/tw/colophon/)

- 關於作者
- 關於譯者
- 後記

## 貢獻者

[查看貢獻者](https://ddia.vonng.com/tw/contrib/)

- 譯者
- 校訂與維護
- 繁體中文版本
- 貢獻列表

## 專案學習方式

每章依「閱讀對應講義小節與理解觀念 → 實驗 → 觀察結果 → 討論權衡」推進。實驗安排在學習該章時決定；第 14 章可採案例討論。

每章完成時，應能：

1. 用自己的話說明問題與解法。
2. 用實驗結果或案例解釋系統行為。
3. 說明解法的成本、限制與適用情境。

引用講義內容時附上對應章節或小節連結。專案補充講解與 labs 另行標示，並歸入對應章節；WAL、Cache 等實作題材可作為補充實驗。

閱讀起點：序言與 I 資料系統基礎導讀，再進入第 1 章「資料系統架構中的權衡」。

## 網站與 GitHub Pages 部署

筆記站的內容、版型與建置程式放在 `site/`，以 Markdown 撰寫筆記，再產生 HTML、CSS 與 JavaScript 靜態頁面。首頁依三篇分組顯示 14 章，章節頁提供導覽、本頁目錄、比較表與程式碼複製功能。

14 章皆已建立 Q&A，共 142 題，目前皆為整理中。第一章 12 題、第二章 10 題已保留原答與回饋；第三至十四章各 10 題待作答。

第一次設定建置環境（Python 3.9 以上）：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r site/requirements.txt
```

產生頁面：

```sh
.venv/bin/python site/build.py
```

修改筆記或版型後，重新執行建置並重新整理瀏覽器。產出位於 `site/public/`，不納入版本控制。

本機預覽：

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory site/public
```

開啟 `http://127.0.0.1:4173/`。

### 撰寫與維護筆記

- `site/content/chapters.json`：篇章、小節、摘要、筆記狀態與更新日期。
- `site/content/01.md` 至 `site/content/14.md`：各章筆記與 Q&A。
- `site/templates/`：首頁、章節頁與共用導覽版型。
- `site/assets/`：共用樣式與閱讀互動。

新增章節筆記時，在該章的 metadata 填入 `note`（例如 `02.md`）與 `updated`（例如 `2026-10-01`），並設定 `status`：`pending`（尚未開始）、`draft`（示範草稿）、`in-progress`（整理中）、`complete`（已整理）。更新日期顯示於章節頁，不自動推定閱讀進度。

筆記可依「學習目標 → 閱讀筆記 → 設計權衡 → 實驗與案例 → Q&A → 尚未理解的問題 → 講義來源」整理。閱讀筆記沿用對應講義的小節順序；Q&A依主題分組，保留題目、原答與回饋。支援 Markdown 表格、程式碼區塊，以及 `!!! note`、`!!! warning`、`!!! question` 提示區塊。

### 手動部署

部署 workflow：`.github/workflows/deploy-pages.yml`，僅使用 `workflow_dispatch` 手動觸發。

1. 將檔案推送到 GitHub repository 的預設分支。
2. 在 **Settings → Pages → Build and deployment → Source** 選擇 **GitHub Actions**。
3. 在 **Actions → Deploy GitHub Pages → Run workflow** 手動部署。

Workflow 會安裝 Markdown 套件、執行 `site/build.py`，再部署 `site/public/`，不會發布內容來源與建置程式。Push 與 pull request 不會觸發此 workflow；部署完成後可從 workflow 的 `github-pages` environment 開啟網站。
