# Fixed8 v0.1 Paper Trading

Fixed8 is a Taiwan stock screening and paper-trading web app.

Current frozen model:

- Train: 2020-07-01 to 2024-10-03
- Validate: 2025-01-01 onward
- Main model: `fund_ml_85_15`
- Observation model: `fund_final_ml`
- Entry: signal day close, next trading day open
- Exit: market bear, stop loss 15%, below MA120, max holding 252 bars
- Positioning: max 5 stocks, 20% equity per position

## Run

```powershell
$env:PYTHONPATH="$PWD\src;$PWD\scripts"
streamlit run streamlit_app.py
```

The site displays the latest signal and paper-trading files. Daily updates are handled by GitHub Actions.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md).
