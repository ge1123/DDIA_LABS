# Experiments

Executable Labs live in `experiments/<lab-id>/`. Start from that Lab's packet in the [implementation-ready curriculum blueprint](../wiki/labs/curriculum-blueprint.md), then create its dedicated canonical page under [`wiki/labs/`](../wiki/labs/index.md). Do not add implementation until that page defines the question, falsifiable hypothesis, variables, measurement, safety boundary, reproduction command, and cleanup.

Use the proposed [experiment architecture](../wiki/architecture/experiment-architecture.md) as the starting convention. A Lab may use fewer directories when they add no value.

Each Lab owns its solution, `compose.yaml`, `lab.sh`, dependencies, resources, and cleanup. The planned root interface is `./lab <lab-id> <action>`, where the root only delegates one of `setup`, `broken`, `correct`, `inspect`, `check`, or `cleanup` to that Lab. The bounded cross-Lab form `./lab all check` discovers Lab scripts and runs only their fast checks; full proofs follow the [evidence matrix](../wiki/qa/evidence-matrix.md) per Lab. No executable Lab exists yet, so the interface remains an accepted design rather than verified runtime behavior.
