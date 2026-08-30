# DDIA Labs

DDIA Labs is a learning repository where each small experiment isolates one data-intensive systems question and turns its outcome into reproducible evidence.

## Language

**Lab**:
A self-contained experiment that investigates one falsifiable data-consistency or distributed-systems question.
_Avoid_: Demo, sample app, mini product

**Lab Contract**:
The repository-wide minimum information and evidence a Lab must provide before its conclusion can be accepted.
_Avoid_: README shape, project template

**Core Lab**:
A Lab on the prerequisite-ordered learning path that every learner is expected to complete.
_Avoid_: Required feature, milestone

**Extension Lab**:
An optional Lab that deepens or contrasts a Core Lab without becoming a prerequisite for the core path.
_Avoid_: Bonus feature, extra scope

**Broken Version**:
The deliberately unsafe implementation used to reproduce a named invariant violation under a documented workload.
_Avoid_: Bad code, before version

**Correct Version**:
The smallest implementation that preserves the stated invariant within the Lab's documented assumptions and failure model.
_Avoid_: Perfect solution, production-ready version

**Evidence**:
A reproducible observation, test result, or bounded measurement that supports or refutes a Lab's hypothesis within its documented environment.
_Avoid_: Proof without scope, successful command
