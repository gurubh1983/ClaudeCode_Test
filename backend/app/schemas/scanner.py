from datetime import datetime
from pydantic import BaseModel, Field


class RuleNode(BaseModel):
    operator: str
    left: dict | float | int | str | None = None
    right: dict | float | int | str | None = None
    value: float | int | None = None
    children: list["RuleNode"] = Field(default_factory=list)
    params: dict = Field(default_factory=dict)


RuleNode.model_rebuild()


class ScanRequest(BaseModel):
    name: str = "Realtime Option Scan"
    timeframe: str = "5m"
    rule_ast: RuleNode
    symbols: list[str] | None = None
    strike_filter: dict = Field(default_factory=dict)
    expiry_filter: dict = Field(default_factory=dict)
    option_type: str = "both"


class ScanResult(BaseModel):
    symbol: str
    expiry: str
    strike: float
    option_type: str
    ltp: float
    timestamp: datetime


class BacktestRequest(BaseModel):
    timeframe: str
    from_ts: str
    to_ts: str
    rule_ast: RuleNode
    symbols: list[str] | None = None
