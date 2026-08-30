# Technology baseline for reproducible DDIA Labs

Research date: 2026-08-30  
Scope: official, first-party sources only

## Decision summary

Use **.NET 10 / ASP.NET Core 10 LTS**, **PostgreSQL 18**, and the **Docker Compose plugin** as the default stack. Keep the API as an ASP.NET Core Minimal API and PostgreSQL as the only stateful dependency until the Lab's question specifically requires another system.

The canonical snapshot for the first implementation wave should be:

| Component | Initial audited pin | Policy |
| --- | --- | --- |
| .NET SDK | `10.0.400` | Commit `global.json` with `allowPrerelease: false` and `rollForward: disable`; update the exact pin through reviewed maintenance changes. |
| .NET / ASP.NET Core runtime | `10.0.11`, target `net10.0` | Stay on .NET 10 and take supported patches promptly; do not start on .NET 8 or 9. |
| PostgreSQL | `18.6` | Use an exact image tag plus a committed image digest; follow later PostgreSQL 18 minor releases without changing the Lab question. |
| Docker Compose | plugin, canonical CI snapshot `5.4.0` | Use `docker compose`, not legacy `docker-compose`; omit the top-level Compose `version`; record Engine and Compose versions with retained evidence. |

NuGet dependencies should have exact versions, committed `packages.lock.json` files, and CI restore with `dotnet restore --locked-mode`. Each Lab owns its small `compose.yaml`; there is no always-on shared stack. Generate and commit a digest-lock override with `docker compose config --lock-image-digests`, and validate configuration with `docker compose config -q`.

## Version and support facts

These are source facts, not the design recommendation above:

- Microsoft's policy covers the .NET runtime, SDK, ASP.NET Core, and EF Core together. As of the research date, .NET 10 is active LTS, runtime patch `10.0.11`, with support through 2028-11-14. .NET 8 and .NET 9 both end support on 2026-11-10. Microsoft ships patches monthly and requires customers to remain current on patches for support. ([.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy))
- The 2026-08-11 .NET 10 servicing release contains SDK `10.0.400` and runtime/ASP.NET Core `10.0.11`. ([.NET 10.0.11 release](https://github.com/dotnet/core/blob/main/release-notes/10.0/10.0.11/10.0.11.md))
- `global.json` accepts a full SDK version and can disable roll-forward; NuGet locked mode refuses dependency-graph changes rather than silently rewriting the lock file. ([`global.json`](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json), [`dotnet restore --locked-mode`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-restore))
- PostgreSQL supports each major version for five years, recommends the current minor of that major, and treats minor releases as low-risk bug/security fixes. PostgreSQL `18.6` is current and PostgreSQL 18 is supported through 2030-11-14. ([PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/))
- Current Compose implementations use the rolling Compose Specification; the old top-level `version` field is ignored. Docker provides an image-digest lock command, while manual plugin installation can select an exact release but does not auto-update. The official Compose repository listed `5.4.0` as the latest release on 2026-08-03 at research time. ([Compose history](https://docs.docker.com/compose/intro/history/), [`docker compose config`](https://docs.docker.com/reference/cli/docker/compose/config/), [plugin installation](https://docs.docker.com/compose/install/linux/), [Compose releases](https://github.com/docker/compose/releases))

## Optional-tool escalation triggers

Optional tools are pinned only in the Labs that use them; they never enter the repo-wide default Compose stack.

| Tool | Initial pin when first needed | Introduce only when the Lab must demonstrate | Do not introduce merely for |
| --- | --- | --- | --- |
| Redis | Redis Open Source `8.2.x` Extended, exact patch + digest | A networked cache's stale window/invalidation/stampede, hot-key behavior, or a lease/lock/fencing failure that cannot be represented faithfully with PostgreSQL alone | General idempotency, lost updates, or ordinary transactions |
| RabbitMQ | `4.3.5`, exact management image + digest | Queue acknowledgements, redelivery, publisher confirms, retry/dead-letter behavior, duplicate-message Inbox, or Saga choreography | Replayable logs, partition ordering, or basic in-process background work |
| Kafka | official `apache/kafka:4.3.1`, digest-pinned, single combined KRaft node for local Lab use | Replay by offset, keyed partition ordering, consumer-group rebalancing, CDC/Connect, or stateful/windowed stream processing | A single duplicate-delivery exercise that RabbitMQ can expose with less setup |
| Testcontainers for .NET | NuGet `4.13.0`, locked | A proof needs a fresh real dependency per test, parallel CI isolation, or controlled container restart/crash; use the same pinned service image as Compose | Pure logic tests or a Lab whose one-shot Compose harness already owns isolation |
| k6 | `2.2.0`, exact container tag + digest | The observation depends on external HTTP concurrency, workload shape, throughput, latency percentiles, hot partitions, stampedes, or backpressure | Deterministic races that an xUnit barrier and `Task.WhenAll` can reproduce faster |

Why these pins and triggers are defensible:

- Redis 8.2 is an Extended release supported through 2030-09-01. Redis's own lock guidance warns that asynchronous failover can violate mutual exclusion and explicitly recommends fencing tokens for correctness-sensitive work. ([Redis version management](https://redis.io/docs/latest/operate/oss_and_stack/install/version-mgmt/), [distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/))
- RabbitMQ 4.3.5 was the current 4.3 patch; community support for the series ends 2026-11-30, so RabbitMQ requires a frequent refresh rather than an assumed community LTS. RabbitMQ documents that acknowledged delivery is at-least-once, that failures can cause duplicates, and that consumers should be idempotent. ([RabbitMQ releases](https://www.rabbitmq.com/release-information), [reliability guide](https://www.rabbitmq.com/docs/reliability))
- Apache lists Kafka 4.3.1 as a supported release and publishes the official `apache/kafka:4.3.1` image. Kafka 4.x is KRaft-only; combined broker/controller mode is explicitly suitable for small development environments. ([Kafka downloads](https://kafka.apache.org/community/downloads/), [KRaft operations](https://kafka.apache.org/42/operations/kraft/))
- Testcontainers models throwaway real dependencies and requires a Docker-compatible runtime; `4.13.0` was the current .NET release at research time. ([Testcontainers](https://testcontainers.com/), [Testcontainers for .NET releases](https://github.com/testcontainers/testcontainers-dotnet/releases))
- k6 scenarios define workload models, while thresholds turn metrics into pass/fail criteria and produce a non-zero exit status on failure. The official docs identify `2.2.x` as latest at research time. ([scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/), [thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), [release notes](https://grafana.com/docs/k6/latest/release-notes/))

## Upgrade policy

1. **Monthly security pass:** update the exact .NET SDK/runtime pin and affected NuGet packages after Patch Tuesday; regenerate lock files and rerun every Lab's proof.
2. **Quarterly dependency pass:** move PostgreSQL 18 and optional services to their latest supported patch, refresh image digests, and rerun only Labs that use each service plus the full smoke suite.
3. **Immediate escalation:** patch outside the cadence for a relevant security advisory, data-corruption bug, broken supported host, or reproducibility failure.
4. **Major-version decision:** open a new decision when the baseline has 12 months of support remaining, an optional product series loses community support, or a required Lab behavior needs a newer major. A major bump must preserve the Broken observation and Correct invariant before it replaces the prior snapshot.
5. **Evidence rule:** every retained run records commit, OS/architecture, `dotnet --info`, `docker version`, `docker compose version`, resolved image digests, workload seed/concurrency, and command. Different machines need not match latency, but must reproduce the stated correctness observation.

This policy deliberately separates **reproduction** (an immutable audited snapshot) from **maintenance** (small reviewed changes that advance that snapshot). Floating `latest` tags satisfy neither.
