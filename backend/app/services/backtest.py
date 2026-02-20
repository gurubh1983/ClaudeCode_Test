import pandas as pd

from app.engine.rule_engine import EvalContext, evaluate


def run_backtest(rule_ast: dict, candles: pd.DataFrame) -> dict:
    mask = evaluate(rule_ast, EvalContext(candles))
    signals = candles[mask]
    total = len(signals)
    win_ratio = 0.0
    if total > 1:
        future_ret = signals["close"].shift(-1) - signals["close"]
        win_ratio = float((future_ret > 0).mean() * 100)
    return {
        "signals": signals.index.astype(str).tolist(),
        "total_signals": total,
        "win_ratio": round(win_ratio, 2),
    }
