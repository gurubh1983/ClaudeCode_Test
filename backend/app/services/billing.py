from fastapi import HTTPException
import stripe

from app.core.config import get_settings

PLAN_LIMITS = {"free": 10, "pro": 200, "elite": 2000}


def get_plan_limit(plan: str) -> int:
    return PLAN_LIMITS.get(plan, 10)


def create_checkout_session(plan: str, customer_email: str, success_url: str, cancel_url: str) -> str:
    settings = get_settings()
    stripe.api_key = settings.stripe_secret_key
    price_lookup = {
        "free": settings.stripe_price_free,
        "pro": settings.stripe_price_pro,
        "elite": settings.stripe_price_elite,
    }
    if plan not in price_lookup or not price_lookup[plan]:
        raise HTTPException(status_code=400, detail="Plan not configured")
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_lookup[plan], "quantity": 1}],
        customer_email=customer_email,
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url
