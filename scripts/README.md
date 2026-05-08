# Scripts

Repository-level automation for local research workflows.

Full technical guide:
[docs/operations/research-data-workflows.md](../docs/operations/research-data-workflows.md)

## Research Data Commands

Dry-run rebuildable data cleanup:

```powershell
.\scripts\Reset-RebuildableData.ps1
```

Apply rebuildable data cleanup:

```powershell
.\scripts\Reset-RebuildableData.ps1 -Apply
```

Generate synthetic data with a named preset:

```powershell
.\scripts\Generate-Dataset.ps1 -Preset large -Seed 123
```

Refresh the UI seed payload and SQLite app store:

```powershell
.\scripts\Refresh-UiSeed.ps1
```

Run reset, generation, and UI seed refresh together:

```powershell
.\scripts\Rebuild-ResearchData.ps1 -Preset large -Seed 123 -Apply
```

## Presets

| Preset | Students | Weeks | Groups |
| --- | ---: | ---: | ---: |
| `small` | 48 | 10 | 2 |
| `default` | 120 | 10 | 3 |
| `large` | 500 | 12 | 8 |
| `xlarge` | 1500 | 14 | 16 |

## Safety

- Cleanup is dry-run by default.
- Use `-Apply` to delete rebuildable data.
- Scripts refuse to delete outside the repository root.
- Scripts preserve `data/artifacts/experiments/**`.
- UI seed refresh does not rerun experiments or validate new hypotheses.
