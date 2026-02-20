from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    plan: str
    success_url: str
    cancel_url: str


class PlanResponse(BaseModel):
    plan: str
    status: str
    daily_scan_limit: int
