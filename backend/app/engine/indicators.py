import numpy as np
import pandas as pd


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period).mean()


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def wma(series: pd.Series, period: int) -> pd.Series:
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda x: (x * weights).sum() / weights.sum(), raw=True)


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0).rolling(period).mean()
    down = -delta.clip(upper=0).rolling(period).mean()
    rs = up / down.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    m = ema(series, fast) - ema(series, slow)
    s = ema(m, signal)
    return pd.DataFrame({"macd": m, "signal": s, "hist": m - s})


def vwap(df: pd.DataFrame) -> pd.Series:
    pv = (df["close"] * df["volume"]).cumsum()
    vol = df["volume"].cumsum().replace(0, np.nan)
    return pv / vol


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    tr = np.maximum.reduce([
        (df["high"] - df["low"]).values,
        (df["high"] - df["close"].shift()).abs().values,
        (df["low"] - df["close"].shift()).abs().values,
    ])
    return pd.Series(tr, index=df.index).rolling(period).mean()


def roc(series: pd.Series, period: int = 12) -> pd.Series:
    return series.pct_change(periods=period) * 100


def mom(series: pd.Series, period: int = 10) -> pd.Series:
    return series.diff(period)
