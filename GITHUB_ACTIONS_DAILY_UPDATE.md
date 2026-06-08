# GitHub Actions Daily Signal Update

This repository includes:

```text
.github/workflows/update-signals.yml
```

It runs:

```text
python scripts/run_today_model_signals.py
```

Schedule:

```text
15:45 Asia/Taipei, Monday-Friday
```

It commits updated files under:

```text
outputs/today_model_signals/*.csv
```

## First Run

After pushing to GitHub:

1. Open the repository on GitHub.
2. Go to **Actions**.
3. Choose **Update Fixed8 Signals**.
4. Click **Run workflow**.

If it succeeds, Streamlit will read the updated signal files from GitHub.

## Permissions

The workflow needs:

```yaml
permissions:
  contents: write
```

This is already included.

If commit fails, check repository settings:

```text
Settings > Actions > General > Workflow permissions
```

Choose:

```text
Read and write permissions
```

## Notes

yfinance can occasionally rate-limit requests. The app now tolerates missing symbols and uses the cached prices when available.
