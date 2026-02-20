import pandas as pd

from app.engine.rule_engine import EvalContext, evaluate


def test_rsi_rule_evaluates_series():
    df = pd.DataFrame({"close": [100 + i for i in range(30)], "volume": [1000] * 30})
    rule = {
        "operator": ">",
        "left": {"type": "indicator", "name": "RSI", "period": 14, "source": "close"},
        "right": {"type": "value", "value": 50},
    }
    out = evaluate(rule, EvalContext(df))
    assert len(out) == len(df)
