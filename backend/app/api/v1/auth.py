import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import Subscription, User
from app.schemas.auth import ResetPasswordConfirm, ResetPasswordRequest, TokenResponse, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = (await db.execute(select(User).where(User.email == payload.email))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(email=payload.email, hashed_password=get_password_hash(payload.password), full_name=payload.full_name)
    db.add(user)
    await db.flush()
    db.add(Subscription(user_id=user.id, plan="free", status="active"))
    await db.commit()
    return TokenResponse(access_token=create_access_token(user.email))


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == payload.email))).scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email))


@router.post("/password-reset/request")
async def request_password_reset(payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == payload.email))).scalar_one_or_none()
    if user:
        user.reset_token = secrets.token_urlsafe(32)
        await db.commit()
    return {"message": "If email exists, a reset token has been generated."}


@router.post("/password-reset/confirm")
async def confirm_password_reset(payload: ResetPasswordConfirm, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.reset_token == payload.token))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid reset token")
    user.hashed_password = get_password_hash(payload.new_password)
    user.reset_token = None
    await db.commit()
    return {"message": "Password updated"}
