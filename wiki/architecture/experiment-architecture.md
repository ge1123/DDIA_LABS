# Experiment Architecture

## Status

Proposed for runtime behavior. The per-Lab execution boundary and thin root command model are accepted repository decisions, but the first executable Lab must still validate them.

## Standard layout

Each executable Lab should use `experiments/<lab-id>/` and keep its implementation details close together:

~~~text
experiments/<lab-id>/
├─ <lab-id>.slnx      # independent restore/build/test graph
├─ compose.yaml       # only this Lab's dependencies and resources
├─ lab.sh             # authoritative implementation of standard actions
├─ README.md          # exact reproduce/cleanup commands and expected observation
├─ src/               # smallest implementation needed by the hypothesis
├─ tests/             # invariants and setup checks
├─ fixtures/          # small deterministic input, when needed
└─ results/           # small stable summaries, never secrets or bulky generated data
~~~

Only create directories a Lab actually needs.

## Execution boundary

- Do not create a root solution. Each Lab owns an independent solution and dependency graph.
- Default to one API project and one test project per Lab. Add an executable project only when an independent process boundary is part of the experiment.
- Keep Broken and Correct implementations in the same Lab and, by default, the same API project so they share the fixture and workload.
- Give every Lab its own Compose file and stable `ddia-lab-<id>` project name. Do not share database, broker, network, volume, migration, or container lifecycle across Labs.
- Keep cleanup bounded to that Compose project and make it safe to rerun.

## Command contract

The repository root will expose a thin `./lab <lab-id> <action>` dispatcher. Standard actions are `setup`, `broken`, `correct`, `inspect`, `check`, and `cleanup`. The root command only validates and delegates; Docker, SQL, workload, assertion, and cleanup behavior remains in the Lab's `lab.sh` and README.

The only cross-Lab form is `./lab all check`. It discovers `experiments/*/lab.sh`, runs sequentially by default with an optional maximum of two workers, attempts bounded cleanup after every Lab, and reports every failure before returning non-zero. `all` cannot run `broken`, `correct`, `inspect`, or `cleanup`; full evidence proofs remain per-Lab under the [evidence matrix](../qa/evidence-matrix.md).

## Shared-file ceiling

Repository-wide execution policy is limited to `global.json`, `Directory.Build.props`, and the thin `lab` dispatcher. Shared runtime libraries, infrastructure, migrations, fixtures, domain models, and correctness helpers are not allowed. A fourth shared execution file or any shared code project requires a new recorded decision showing that it does not hide a Lab's causal mechanism.

## Required Lab contract

Before implementation, the canonical page in `wiki/labs/` records:

- question and falsifiable hypothesis;
- related DDIA concept and source locator;
- controlled and changed variables;
- dataset/workload and environment;
- measurement, units, warm-up, run count, and stop conditions;
- expected observations and known confounders;
- exact reproduction and cleanup entry points.

## Isolation and safety

- Default to generated or synthetic data.
- Pin important dependency or service versions when version drift could change the conclusion.
- Use explicit resource names and bounded cleanup commands.
- Do not depend on hidden interactive state.
- Prefer local containers or processes until a Lab specifically studies remote/distributed behavior.

## Result rule

A successful command is not automatically a successful experiment. The result must address the hypothesis, preserve surprising or conflicting observations, and state the scope in which the conclusion is valid.
