from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import stripe

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import Invoice, Subscription, User
from app.schemas.billing import CheckoutRequest
from app.services.billing import create_checkout_session, get_plan_limit

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get('/plan')
async def get_plan(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    sub = (await db.execute(select(Subscription).where(Subscription.user_id == user.id))).scalar_one_or_none()
    plan = sub.plan if sub else "free"
    return {"plan": plan, "status": sub.status if sub else "active", "daily_scan_limit": get_plan_limit(plan)}


@router.post('/checkout')
async def checkout(payload: CheckoutRequest, user: User = Depends(get_current_user)):
    url = create_checkout_session(payload.plan, user.email, payload.success_url, payload.cancel_url)
    return {"checkout_url": url}


@router.get('/invoices')
async def invoices(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Invoice).where(Invoice.user_id == user.id))).scalars().all()
    return [{"id": r.id, "amount": r.amount_paid, "url": r.hosted_invoice_url, "created_at": r.created_at} for r in rows]


@router.post('/webhook')
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    settings = get_settings()
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    event = stripe.Webhook.construct_event(payload=payload, sig_header=sig, secret=settings.stripe_webhook_secret)
    if event["type"] == "invoice.paid":
        invoice = event["data"]["object"]
        customer_id = invoice.get("customer")
        sub = (await db.execute(select(Subscription).where(Subscription.stripe_customer_id == customer_id))).scalar_one_or_none()
        if sub:
            db.add(Invoice(
                user_id=sub.user_id,
                stripe_invoice_id=invoice["id"],
                amount_paid=invoice.get("amount_paid", 0),
                currency=invoice.get("currency", "usd"),
                hosted_invoice_url=invoice.get("hosted_invoice_url"),
            ))
            await db.commit()
    return {"ok": True}
