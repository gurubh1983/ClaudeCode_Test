from fastapi import APIRouter

from app.api.v1 import auth, billing, scanner, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(scanner.router)
api_router.include_router(billing.router)
