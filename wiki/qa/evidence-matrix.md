# Lab Evidence Matrix

## Status

Proposed. The profiles and numeric gates are accepted planning defaults, but no executable Lab has exercised them yet.

## Governing rule

Every Lab selects one primary evidence profile before implementation. Every accepted proof directly checks the Lab invariant under the same fixture, workload, and failure model for Broken and Correct. A tool or successful process exit is never evidence by itself.

## Profiles

| Profile | Labs | Broken gate | Correct gate | Per-run／whole-proof ceiling |
| --- | --- | --- | --- | --- |
| D — Deterministic transformation | 10, 12, 16, 17 | 3／3 violations | 10／10, zero violations | 30 s／5 min |
| C — Controlled concurrency | 01–04, 14–15 | 5／5 violations | 25／25, zero violations | 60 s／10 min |
| M — Message delivery／workflow | 05–09 | 5／5 violations | 20／20, zero violations | 90 s／15 min |
| R — Replication behavior | 11, E03 | 3／3 violations | 10／10, zero violations | 180 s／20 min |
| X — Crash／restart recovery | 18, 19, E04 | 3／3 violations | 10／10, zero violations | 180 s／20 min |
| P — Performance／comparison | 13, E01, E02 | 1 warm-up + 5 measured; baseline fails at least 4／5 | 5／5 correctness; Correct meets the gate at least 4／5 | 5 min measured run／45 min |
| S — Stream time／ownership | 20, E05 | 5／5 violations | 20／20, zero violations | 120 s／20 min |

Setup has a separate default ceiling of 10 minutes; first image pull and package restore are outside the proof clock. A timeout is Invalid evidence unless bounded completion is itself the declared invariant.

## Performance rule

Run one warm-up, then five interleaved measured runs per variant. A comparative claim requires direction agreement in at least four paired runs, a median improvement of at least 20%, and coefficient of variation no greater than 15% for the primary metric of each variant. Otherwise the result is Inconclusive.

Absolute performance budgets gate only the recorded reference runner. Correctness must pass on every runner and cannot be offset by a performance improvement.

## Probabilistic exception

Probabilistic evidence requires a documented reason that deterministic control would change the subject. Broken runs at least 50 times, observes at least 20 violations, and retains a 95% Wilson lower bound of at least 20%. Correct runs 100 times with zero violations and explicitly records that this implies only an approximate 3% upper bound, not proof of impossibility.

## Tool boundary

- Every Lab has an automated integration assertion over the invariant or durable effect.
- Use barriers for controlled interleavings and a bounded Compose harness for process or service faults.
- Use Testcontainers only for per-test fresh dependencies, parallel isolation, or programmatic restart that Compose cannot provide reliably.
- Use k6 or an equivalent driver only when external concurrency, throughput, tail latency, skew, stampede, or backpressure is the primary observation.
- Every accepted Lab retains a small `results/accepted.json`; raw logs remain reproducible rather than committed.

## Flaky evidence

Acceptance runs never auto-retry. Mixed pass／fail results for the same commit, environment, fixture, and seed invalidate the evidence and prevent Verified status. Diagnostic reruns preserve the first failure.

After a fix, D／C／M／S profiles require 50 consecutive passes, R／X profiles require 20, and the original failing seed or fault point requires 10. P repeats its full warm-up and five paired measurements. Quarantine may isolate a job but may not skip or allow the failure.

## Cross-Lab check

The planned root command `./lab all check` discovers `experiments/*/lab.sh`, runs fast checks sequentially by default, permits at most two workers, attempts cleanup after every Lab, and reports all failures before returning non-zero. Full profile proofs remain per-Lab and run for changed Labs or before a Lab becomes Verified.

## Evidence and limits

The detailed planning decision is [Issue 07](../../.scratch/ddia-labs-learning-roadmap/issues/07-define-the-evidence-matrix.md), tracked by [GitHub Issue #7](https://github.com/ge1123/DDIA_LABS/issues/7).

**Verified fact:** the existing evidence policy and Lab contract define the evidence roles and invariant-first acceptance boundary.

**Reasonable inference:** these numeric defaults provide a conservative, locally runnable first acceptance matrix.

**Open question:** the first executable Lab must test whether the run counts, deadlines, retained JSON, and cross-Lab check are operationally appropriate.
