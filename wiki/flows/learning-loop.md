# Learning Loop

## Status

Verified as the accepted workflow; individual study iterations provide their own execution evidence.

## Process

| Step | Activity | Output | Exit condition |
| --- | --- | --- | --- |
| 1 | Frame | One question, motivation, and non-goals | The question is narrow enough to answer |
| 2 | Study | Source locators and an explanation in the learner's own words | Claims are distinguishable from interpretation |
| 3 | Hypothesize | Falsifiable expected observation | A counterexample could prove it wrong |
| 4 | Design | Variables, workload, metrics, environment, risks, cleanup | Confounders and stop conditions are explicit |
| 5 | Implement | Small experiment plus setup checks | The setup can be recreated without hidden state |
| 6 | Observe | Commands and scoped measurement summary | Units, versions, run count, and anomalies are recorded |
| 7 | Interpret | Facts, inferences, conflicts, and limitations | Conclusion answers the original question only |
| 8 | Integrate | Updated canonical page, source ledger, and follow-up questions | Links and reproduction path are valid |

## Failure and retry

- A failed setup is a Lab infrastructure result, not evidence for the hypothesis.
- A surprising result is retained and investigated; do not tune it away merely to match the source.
- If versions, workload, or implementation materially change, rerun the relevant checks and mark stale conclusions Outdated until reviewed.
- Cleanup must be bounded to explicitly named Lab resources.

