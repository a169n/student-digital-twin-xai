# Research Data Workflows

This guide documents the repository-level scripts for resetting rebuildable
data, generating larger synthetic cohorts, and refreshing the read-only UI
seed. These workflows are intended for local research iteration on Windows.

## Safety Model

The scripts distinguish between rebuildable data and canonical research
evidence.

Rebuildable data can be deleted and recreated:

- `data/raw/*`
- `data/processed/*`
- `data/application/*`
- `data/artifacts/research_demo/*`
- `data/artifacts/eda/*`
- `data/artifacts/reports/*`

Canonical experiment artifacts are preserved:

- `data/artifacts/experiments/**`

Do not delete or overwrite canonical experiment folders when changing dataset
size, schema version, feature sets, targets, split strategy, or model family.
Those changes require new experiment IDs.

## Reset Rebuildable Data

Dry run:

```powershell
.\scripts\Reset-RebuildableData.ps1
```

Apply deletion:

```powershell
.\scripts\Reset-RebuildableData.ps1 -Apply
```

The script resolves every target under the repository root and refuses to
delete anything under `data/artifacts/experiments`.

## Generate Synthetic Dataset

Generate the default research-sized dataset:

```powershell
.\scripts\Generate-Dataset.ps1
```

Generate a larger cohort with a fixed seed:

```powershell
.\scripts\Generate-Dataset.ps1 -Preset large -Seed 123
```

Available presets:

| Preset | Students | Weeks | Groups | Assignments / week | Sessions / week |
| --- | ---: | ---: | ---: | ---: | ---: |
| `small` | 48 | 10 | 2 | 2 | 2 |
| `default` | 120 | 10 | 3 | 2 | 2 |
| `large` | 500 | 12 | 8 | 2 | 2 |
| `xlarge` | 1500 | 14 | 16 | 2 | 2 |

The generator auto-fills extra topic titles when `num_weeks` exceeds the base
10-week course template. Example: week 11 becomes `Extended Practice Week 11`.
The validation layer uses the active generator config for week-number bounds,
so local scale checks can use longer synthetic courses without editing the
schema contract.

## Refresh UI Seed

Refresh the read-only platform payload and SQLite app store:

```powershell
.\scripts\Refresh-UiSeed.ps1
```

This performs two steps:

1. `python -m src.export.export_research_demo_payload` from `services/ml`
2. `python -m src.import_research_payload` from `apps/api`

Important: this reuses the currently available experiment artifacts. It does
not rerun experiments or validate new hypotheses.

## Full Rebuild Convenience Workflow

Dry run:

```powershell
.\scripts\Rebuild-ResearchData.ps1 -Preset large -Seed 123
```

Apply:

```powershell
.\scripts\Rebuild-ResearchData.ps1 -Preset large -Seed 123 -Apply
```

This runs:

1. reset rebuildable data
2. generate synthetic data with the selected preset
3. refresh UI seed

Use this when you want to quickly inspect how the platform behaves with a
larger generated cohort. Use new experiment IDs for a real hypothesis test.

## Direct ML CLI Overrides

The underlying generator also supports direct overrides:

```powershell
cd services\ml
python -m src.main `
  --config configs/generator_v1_3_refined.yaml `
  --seed 123 `
  --num-students 500 `
  --num-weeks 12 `
  --num-groups 8 `
  --assignments-per-week 2 `
  --sessions-per-week 2
```

Generated outputs go to:

- `data/raw`
- `data/processed`
- `data/artifacts/reports`

## Recommended Hypothesis Workflow

For quick UI scale checks:

```powershell
.\scripts\Rebuild-ResearchData.ps1 -Preset large -Seed 123 -Apply
```

For dissertation-quality experiment checks:

1. create a new generator config or record the CLI overrides
2. generate the dataset
3. create new experiment configs with new experiment IDs
4. rerun the relevant experiments
5. export the UI seed
6. update docs and registry

This keeps old evidence reproducible while letting larger-dataset hypotheses
be tested cleanly.
