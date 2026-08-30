# Experiment Architecture

## Status

Proposed. Apply and refine this structure when the first executable Lab is created.

## Standard layout

Each executable Lab should use `experiments/<lab-id>/` and keep its implementation details close together:

~~~text
experiments/<lab-id>/
├─ README.md          # exact reproduce/cleanup commands and expected observation
├─ src/               # smallest implementation needed by the hypothesis
├─ tests/             # invariants and setup checks
├─ fixtures/          # small deterministic input, when needed
└─ results/           # small stable summaries, never secrets or bulky generated data
~~~

Only create directories a Lab actually needs.

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

