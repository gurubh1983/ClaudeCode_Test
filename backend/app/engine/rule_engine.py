from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from app.engine import indicators, operators


@dataclass
class EvalContext:
    frame: pd.DataFrame


def resolve_operand(node, ctx: EvalContext):
    if isinstance(node, (int, float)):
        return node
    if isinstance(node, str):
        return ctx.frame[node]
    if isinstance(node, dict):
        kind = node.get("type")
        if kind == "field":
            return ctx.frame[node["name"]]
        if kind == "indicator":
            name = node["name"].lower()
            source = ctx.frame[node.get("source", "close")]
            period = int(node.get("period", 14))
            if name == "sma":
                return indicators.sma(source, period)
            if name == "ema":
                return indicators.ema(source, period)
            if name == "wma":
                return indicators.wma(source, period)
            if name == "rsi":
                return indicators.rsi(source, period)
            if name == "roc":
                return indicators.roc(source, period)
            if name == "mom":
                return indicators.mom(source, period)
            if name == "vwap":
                return indicators.vwap(ctx.frame)
            if name == "macd":
                comp = node.get("component", "macd")
                return indicators.macd(source)[comp]
        if kind == "value":
            return node["value"]
    return node


def evaluate(node: dict, ctx: EvalContext) -> pd.Series:
    op = node["operator"].lower()

    if op in {"and", "or"}:
        children = [evaluate(child, ctx) for child in node.get("children", [])]
        if not children:
            return pd.Series([False] * len(ctx.frame), index=ctx.frame.index)
        out = children[0]
        for child in children[1:]:
            out = out & child if op == "and" else out | child
        return out

    left = resolve_operand(node.get("left"), ctx)
    right = resolve_operand(node.get("right"), ctx)

    if op == ">":
        return left > right
    if op == "<":
        return left < right
    if op == ">=":
        return left >= right
    if op == "<=":
        return left <= right
    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    if op == "cross_above":
        return operators.cross_above(left, right)
    if op == "cross_below":
        return operators.cross_below(left, right)
    if op == "between":
        return operators.between(left, node["params"]["low"], node["params"]["high"])
    if op == "rising_for_n_bars":
        return operators.rising_for_n_bars(left, int(node["params"]["n"]))
    if op == "falling_for_n_bars":
        return operators.falling_for_n_bars(left, int(node["params"]["n"]))

    raise ValueError(f"Unsupported operator: {op}")
