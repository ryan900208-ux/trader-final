from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

os.environ.setdefault("FIXED8_DATA_DIR", str(ROOT / "outputs"))
os.environ.setdefault("FIXED8_PRICE_CACHE_DIR", str(ROOT / "work" / "price_cache"))

try:
    from google_sheets_store import configured as sheets_configured
    from google_sheets_store import sync_from_google_sheets
    from paper_trading_v01 import OUTPUT_DIR as PAPER_DIR
    from paper_trading_v01 import dashboard_payload
except Exception as import_error:
    st.error("Fixed8 module import failed")
    st.exception(import_error)
    st.stop()


st.set_page_config(page_title="Fixed8 v0.1", layout="wide")


def main() -> None:
    try:
        if not _authorized():
            _login()
            return

        _sync_from_remote()
        st.title("Fixed8 v0.1 Paper Trading")
        st.caption("Main model: defensive fund_ml_85_15. Observation model: aggressive fund_final_ml.")
        st.info("Signals and paper-trading records are updated by GitHub Actions. This app only displays the latest files.")
        st.write("Google Sheets: " + ("enabled" if sheets_configured(st.secrets) else "not configured"))

        try:
            payload = dashboard_payload()
        except FileNotFoundError:
            st.warning("No signal files found yet. Wait for GitHub Actions to update outputs/today_model_signals.")
            return

        _metrics(payload)
        tab_signal, tab_portfolio, tab_records, tab_setup = st.tabs(
            ["Signals", "Portfolio", "Records", "Setup"]
        )
        with tab_signal:
            _signals(payload)
        with tab_portfolio:
            _portfolio(payload)
        with tab_records:
            _records(payload)
        with tab_setup:
            _setup_notes()
    except Exception as exc:
        st.error("Fixed8 app runtime error")
        st.exception(exc)


def _authorized() -> bool:
    password = _secret("fixed8_password") or os.environ.get("FIXED8_PASSWORD")
    if not password:
        return True
    return st.session_state.get("fixed8_authed") is True


def _login() -> None:
    st.title("Fixed8")
    password = _secret("fixed8_password") or os.environ.get("FIXED8_PASSWORD")
    supplied = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        if supplied == password:
            st.session_state["fixed8_authed"] = True
            st.rerun()
        st.error("Wrong password")


def _sync_from_remote() -> None:
    try:
        sync_from_google_sheets(st.secrets, PAPER_DIR)
    except Exception as exc:
        st.warning(f"Google Sheets read failed. Showing local files instead: {exc}")


def _metrics(payload: dict) -> None:
    cols = st.columns(6)
    cols[0].metric("Latest date", payload["latest_date"])
    cols[1].metric("Market", payload["market_regime"])
    cols[2].metric("Equity", _money(payload["equity"]))
    cols[3].metric("Return", f"{payload['total_return_pct']:.2f}%")
    cols[4].metric("Cash", _money(payload["cash"]))
    cols[5].metric("Candidates", payload["candidate_rows"])


def _signals(payload: dict) -> None:
    st.subheader("Defensive buy signals")
    st.dataframe(_signal_frame(payload["defensive_top"]), use_container_width=True, hide_index=True)

    st.subheader("Aggressive observation signals")
    st.dataframe(_signal_frame(payload["aggressive_top"]), use_container_width=True, hide_index=True)

    st.subheader("Pending orders")
    pending = pd.DataFrame(payload["pending_orders"])
    st.dataframe(pending, use_container_width=True, hide_index=True) if not pending.empty else st.info("No pending orders")

    st.subheader("Sell signals")
    exits = pd.DataFrame(payload["exit_signals"])
    st.dataframe(exits, use_container_width=True, hide_index=True) if not exits.empty else st.info("No sell signals")


def _portfolio(payload: dict) -> None:
    st.subheader("Current positions")
    positions = pd.DataFrame(payload["positions"])
    if positions.empty:
        st.info("No current positions.")
    else:
        st.dataframe(positions, use_container_width=True, hide_index=True)

    st.subheader("Equity curve")
    snapshots = pd.DataFrame(payload["snapshots"])
    if snapshots.empty:
        st.info("No snapshots yet")
    else:
        st.line_chart(snapshots.set_index("date")["equity"])
        st.dataframe(snapshots, use_container_width=True, hide_index=True)


def _records(payload: dict) -> None:
    st.subheader("Closed trades")
    trades = pd.DataFrame(payload["trades"])
    if trades.empty:
        st.info("No closed trades yet")
    else:
        st.dataframe(trades, use_container_width=True, hide_index=True)
        st.download_button("Download trades CSV", trades.to_csv(index=False).encode("utf-8-sig"), "fixed8_trades.csv")


def _setup_notes() -> None:
    st.markdown(
        """
### Automation

Daily signal files are updated by:

```text
.github/workflows/update-signals.yml
```

Google Sheets paper-trading records are updated by:

```text
.github/workflows/update-paper.yml
```

Required GitHub repository secrets:

```text
GOOGLE_SHEET_ID
GCP_SERVICE_ACCOUNT_JSON
```

Required Streamlit secret for login:

```toml
fixed8_password = "your-password"
```
"""
    )


def _signal_frame(rows: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    columns = [
        "symbol",
        "name",
        "Close",
        "fundamental_score",
        "final_score",
        "stable_ensemble_score",
        "rs20_rank_pct",
        "ret20",
        "ret60",
        "rsi14",
        "volume_ratio",
    ]
    return frame[[column for column in columns if column in frame]]


def _secret(key: str) -> str | None:
    try:
        return st.secrets[key]
    except Exception:
        return None


def _money(value: float) -> str:
    return f"{float(value):,.0f}"


if __name__ == "__main__":
    main()
