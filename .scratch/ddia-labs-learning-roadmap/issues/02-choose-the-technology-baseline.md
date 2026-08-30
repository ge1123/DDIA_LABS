# Choose the reproducible technology baseline

Type: research
Status: resolved

## Question

對一套以 .NET / ASP.NET Core、PostgreSQL、Docker Compose 為主且預計在 2026 年維護的學習 Labs，應採用哪些版本政策與工具升級門檻，才能兼顧可重現性、學習成本和長期支援？請以官方支援週期與產品文件為依據，提出預設基線，以及何時才引入 Redis、RabbitMQ、Kafka、Testcontainers 和 k6。

## Answer

預設採 .NET 10 / ASP.NET Core 10 LTS、PostgreSQL 18 與 Docker Compose plugin；API 使用 Minimal API，每個 Lab 擁有自己的小型 `compose.yaml`，未被該題目需要的服務不得加入。SDK、runtime、NuGet 與 container image 都使用可稽核的精確版本或 digest，並把 patch refresh 與 major-version decision 分開處理。

Redis 只在真實 cache、hot key 或 lease semantics 是題目時加入；RabbitMQ 用於 ACK/redelivery/confirm/Inbox/Saga choreography；Kafka 用於 replay、partition order、CDC/Connect 或 stateful/windowed stream；Testcontainers 只用於需要每測試 fresh real dependency 或 crash/restart 的證據；k6 只用於外部 HTTP workload shape、吞吐、延遲、hot partition、stampede 或 backpressure。

完整版本事實、初始 audited pins、升級節奏與一手來源見 [Technology baseline for reproducible DDIA Labs](../research/02-technology-baseline.md)。
