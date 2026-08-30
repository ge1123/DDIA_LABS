# System Quality Attributes

## Status

Pending. This page seeds study questions; it is not yet a verified chapter note.

## Source locator

- DDIA, topic: reliable, scalable, and maintainable applications.
- Add the edition, chapter, and section used during study.

## Working questions

### Reliability

- Which faults are expected, and which failures should remain invisible to a user?
- How will hardware, software, and human faults be introduced and observed safely?

### Scalability

- What load parameters describe the system before discussing whether it scales?
- Which latency percentile, throughput, resource, or queue measurement answers the actual question?

### Maintainability

- How do operability, simplicity, and evolvability appear in code and operational work?
- Which complexity is inherent to the problem, and which is accidental?

## Evidence classification

Verified facts:

- This repository uses these three attributes as initial learning dimensions, as recorded in the current Wiki architecture.

Reasonable inferences:

- Future Labs will often need more than one metric because throughput, latency, correctness, and operational cost can trade off.

Open questions:

- Which first Lab best demonstrates the difference between a load parameter and a performance metric?
- Which fault-injection boundary can be reproduced safely on a developer machine?

## Related pages

- [Learning architecture](../architecture/learning-architecture.md)
- [Evidence quality](../qa/evidence-quality.md)
- [Labs](../labs/index.md)

