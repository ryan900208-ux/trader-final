# GitHub Actions Paper Trading Update

This workflow updates Google Sheets paper trading records automatically:

```text
.github/workflows/update-paper.yml
```

Schedule:

```text
15:55 Asia/Taipei, Monday-Friday
```

It reads/writes these Google Sheet tabs:

```text
state
trades
daily_snapshots
```

## Required GitHub Secrets

Open your GitHub repository:

```text
Settings > Secrets and variables > Actions > New repository secret
```

Add:

```text
GOOGLE_SHEET_ID
```

Value:

```text
1hQKOnYSsRdyFI_S56YolbTb4cr57VevPEt8LvhmCjs4
```

Add:

```text
GCP_SERVICE_ACCOUNT_JSON
```

Value: paste the entire service account JSON file contents.

## First Run

After adding secrets:

```text
Actions > Update Fixed8 Paper Trading > Run workflow
```

If it succeeds, Google Sheets will update automatically every trading day.
