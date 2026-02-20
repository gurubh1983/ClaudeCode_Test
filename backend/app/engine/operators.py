import pandas as pd


def cross_above(left: pd.Series, right: pd.Series) -> pd.Series:
    return (left > right) & (left.shift(1) <= right.shift(1))


def cross_below(left: pd.Series, right: pd.Series) -> pd.Series:
    return (left < right) & (left.shift(1) >= right.shift(1))


def rising_for_n_bars(series: pd.Series, n: int) -> pd.Series:
    return series.diff().rolling(n).apply(lambda x: all(v > 0 for v in x), raw=False).fillna(0).astype(bool)


def falling_for_n_bars(series: pd.Series, n: int) -> pd.Series:
    return series.diff().rolling(n).apply(lambda x: all(v < 0 for v in x), raw=False).fillna(0).astype(bool)


def between(series: pd.Series, low: float, high: float) -> pd.Series:
    return (series >= low) & (series <= high)


def highest(series: pd.Series, n: int) -> pd.Series:
    return series.rolling(n).max()


def lowest(series: pd.Series, n: int) -> pd.Series:
    return series.rolling(n).min()


def slope(series: pd.Series, n: int) -> pd.Series:
    return (series - series.shift(n)) / n


def percentage_change(series: pd.Series, n: int) -> pd.Series:
    return series.pct_change(n) * 100
