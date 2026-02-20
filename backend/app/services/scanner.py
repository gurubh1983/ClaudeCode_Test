from datetime import datetime
import pandas as pd

from app.engine.rule_engine import EvalContext, evaluate


def apply_strike_filters(options: list[dict], strike_filter: dict, option_type: str) -> list[dict]:
    out = options
    if option_type in {"CE", "PE"}:
        out = [o for o in out if o.get("option_type") == option_type]
    moneyness = strike_filter.get("moneyness")
    if moneyness:
        out = [o for o in out if o.get("moneyness") == moneyness]
    return out


def run_scan_on_chain(rule_ast: dict, option_chain: list[dict]) -> list[dict]:
    hits = []
    for opt in option_chain:
        candles = pd.DataFrame(opt.get("candles", []))
        if candles.empty:
            continue
        mask = evaluate(rule_ast, EvalContext(frame=candles))
        if bool(mask.iloc[-1]):
            hits.append(
                {
                    "symbol": opt["symbol"],
                    "expiry": opt["expiry"],
                    "strike": opt["strike"],
                    "option_type": opt["option_type"],
                    "ltp": float(opt.get("ltp", candles["close"].iloc[-1])),
                    "timestamp": datetime.utcnow(),
                }
            )
    return hits
