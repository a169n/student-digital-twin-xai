# Experiment Logbook

This directory is the research logbook for model experiments. It complements the
data-model documentation and schema contracts; it does not replace them.

## Conventions

- Experiment IDs use `exp_###_short_name`, for example `exp_001_baseline`.
- Every completed experiment has:
  - a versioned config in `services/ml/configs/experiments/`,
  - an isolated artifact folder in `data/artifacts/experiments/<experiment_id>/`,
  - machine-readable `experiment_metadata.json`,
  - a Markdown writeup in `docs/experiments/<experiment_id>.md`,
  - a row in `docs/experiments/registry.md`.
- Status values:
  - `planned` - defined but not run,
  - `completed` - run and documented,
  - `superseded` - retained for history but replaced by a later experiment,
  - `invalidated` - retained because it was run, but should not be cited as a valid result.

## Artifact Policy

Experiment outputs are preserved by experiment ID. Do not reuse an existing
experiment ID for materially different code, data, feature sets, targets, or
split logic. Create a new experiment ID instead.

CSV tables may be regenerated locally and are ignored by default. JSON and
Markdown summaries are the citation-friendly artifacts tracked in the repository.

## Schema Policy

These experiments currently use schema `v1.2`. Experiment logging and ablation
do not require a schema bump because no fields are added, removed, renamed, or
reinterpreted.
