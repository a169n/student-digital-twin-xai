# ML Service

Python service for research workflows around:

- synthetic LMS-like data generation,
- weekly student twin snapshot construction,
- schema-aware validation,
- future feature engineering and baseline modeling.

## Dependency Management

This service uses **uv** for fast, reproducible Python dependency management across research iterations.

## Windows Quick Start

From the repository root, create and activate a virtual environment.

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then install dependencies with `pip`:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ./services/ml
```

If you prefer a non-editable install, use:

```powershell
python -m pip install ./services/ml
```

If you prefer a plain requirements file, use:

```powershell
python -m pip install -r services/ml/requirements.txt
```

## Dataset Generation

The current entrypoint builds the synthetic dataset pipeline aligned with `schema_v1.2`.

## Benchmark Configs

The repository now keeps explicit benchmark configs instead of relying on one mutable file:

- `configs/generator_v1_2_baseline.yaml`: benchmark baseline using the v1.2 trajectory tuning
- `configs/generator_v1_3_refined.yaml`: recommended refined benchmark using the v1.3 realism tuning
- `configs/generator_v1.yaml`: convenience alias for the current recommended refined setup

Run from `services/ml`:

With `uv`:

```powershell
uv run python -m src.main --config configs/generator_v1.yaml
```

With the activated `venv` and plain `pip` install:

```powershell
python -m src.main --config configs/generator_v1.yaml
```

Recommended benchmark runs:

```powershell
python -m src.main --config configs/generator_v1_2_baseline.yaml --output-root C:\path\to\dataset_v1_2
python -m src.main --config configs/generator_v1_3_refined.yaml --output-root C:\path\to\dataset_v1_3
```

Optional flags:

- `--seed 123`
- `--output-root ../../tmp/dataset_run`
- `--skip-parquet`

Outputs are written to:

- `data/raw/*.csv`
- `data/processed/student_twin_snapshots.csv`
- `data/processed/student_twin_snapshots.parquet` unless skipped
- `data/artifacts/reports/realism_metrics.json`
- `data/artifacts/reports/realism_report.md`

## What the Pipeline Does

1. Loads the generator config and resolves output paths.
2. Generates raw LMS-like tables for the one-course, 10-week prototype.
3. Builds `student_twin_snapshots` with `1 row = 1 student x 1 week`.
4. Validates generated tables against `packages/contracts/schema_versions/schema_v1.2.yaml`.
5. Runs a realism audit and writes JSON + Markdown reports.
6. Writes outputs and prints a concise summary.

## Comparison Reports

To compare two generated dataset runs:

```powershell
python -m src.compare --left C:\path\to\dataset_v1_2 --right C:\path\to\dataset_v1_3
```

This writes:

- `comparison_summary.json`
- `comparison_report.md`
- `key_metrics.csv`

under `data/artifacts/reports/comparisons/` by default.

## Testing

Run from `services/ml`:

```powershell
python -m pytest
```

If you want the same mode used during local verification in this repository:

```powershell
python -m pytest tests -v -p no:cacheprovider
```
