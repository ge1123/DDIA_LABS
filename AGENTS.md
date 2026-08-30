# DDIA Labs Repository Guide

## Purpose

This repository turns DDIA concepts into small, reproducible experiments. Keep examples focused on one question or trade-off; avoid product features that do not improve the learning evidence.

## Wiki-first workflow

For every repository task:

1. Read [wiki/index.md](wiki/index.md) first.
2. Open only the canonical Wiki pages relevant to the question.
3. Check page status and evidence coverage in [wiki/source.md](wiki/source.md).
4. If the Wiki is sufficient for a read-only question, do not perform an unrelated broad source scan.
5. When current behavior must be confirmed, inspect the relevant experiment, test, configuration, and raw result.
6. Distinguish Verified fact, Reasonable inference, and Open question.

The complete Wiki maintenance rules are in [wiki/AGENTS.md](wiki/AGENTS.md).

## Change and verification rules

- Confirm target files and working-tree state before editing.
- Preserve user changes and avoid unrelated edits.
- Define the hypothesis, controlled variables, workload, measurement, and expected observation before implementing a new Lab.
- Keep generated or machine-specific output out of the Wiki. Retain only small, stable evidence needed to reproduce or interpret a result.
- When an experiment changes durable behavior or invalidates an explanation, update its canonical Wiki page, `source.md`, and any necessary `log.md` entry.
- For documentation changes, check local Markdown links.
- For experiment changes, run the narrowest relevant check first, then the reproducibility command documented by that Lab.

## Code navigation

If a `.codegraph/` directory exists at the repository root, use CodeGraph before grep, find, or broad file reading when locating or understanding code. Otherwise use `rg`/`rg --files` first.

