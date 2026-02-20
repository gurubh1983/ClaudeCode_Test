from fastapi import APIRouter, Depends, HTTPException
import pandas as pd

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.integrations.angelone import AngelOneClient
from app.models.user import User
from app.schemas.scanner import BacktestRequest, ScanRequest
from app.services.backtest import run_backtest
from app.services.scanner import apply_strike_filters, run_scan_on_chain

router = APIRouter(prefix="/scanner", tags=["scanner"])


@router.post('/run')
async def run_scan(payload: ScanRequest, user: User = Depends(get_current_user)):
    settings = get_settings()
    if not all([settings.angel_api_key, settings.angel_client_code, settings.angel_pin, settings.angel_totp_secret]):
        raise HTTPException(status_code=400, detail="Angel One credentials are required")

    angel = AngelOneClient(settings.angel_api_key, settings.angel_client_code, settings.angel_pin, settings.angel_totp_secret)
    await angel.login()

    symbols = payload.symbols or ["NIFTY", "BANKNIFTY", "FINNIFTY"]
    chain = []
    for symbol in symbols:
        chain_data = await angel.get_option_chain(symbol)
        option_greeks = chain_data.get("optionGreeks", [])
        for item in option_greeks:
            candles = item.get("candles", [])
            if not candles:
                continue
            chain.append({
                "symbol": symbol,
                "expiry": item.get("expiryDate", ""),
                "strike": item.get("strikePrice", 0),
                "option_type": item.get("optionType", "CE"),
                "ltp": item.get("ltp", 0),
                "moneyness": item.get("moneyness", "ATM"),
                "candles": candles,
            })

    if not chain:
        raise HTTPException(status_code=424, detail="No option-chain candles available from broker for selected scope")

    filtered = apply_strike_filters(chain, payload.strike_filter, payload.option_type)
    return {"results": run_scan_on_chain(payload.rule_ast.model_dump(), filtered)}


@router.post('/backtest')
async def backtest(payload: BacktestRequest, user: User = Depends(get_current_user)):
    settings = get_settings()
    angel = AngelOneClient(settings.angel_api_key, settings.angel_client_code, settings.angel_pin, settings.angel_totp_secret)
    await angel.login()
    symbol = (payload.symbols or ["NIFTY"])[0]
    historical = await angel.get_candles("NSE", symbol, payload.timeframe, payload.from_ts, payload.to_ts)
    if not historical:
        raise HTTPException(status_code=424, detail="No historical candles available for backtest")
    candles = pd.DataFrame(historical, columns=["timestamp", "open", "high", "low", "close", "volume"])
    return run_backtest(payload.rule_ast.model_dump(), candles)
