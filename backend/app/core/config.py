from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "StrikeGenius.ai"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    access_token_expire_minutes: int = 60 * 24

    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@db:5432/strikegenius", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")

    stripe_secret_key: str = Field(default="", alias="STRIPE_SECRET_KEY")
    stripe_webhook_secret: str = Field(default="", alias="STRIPE_WEBHOOK_SECRET")
    stripe_price_free: str = ""
    stripe_price_pro: str = ""
    stripe_price_elite: str = ""

    angel_client_id: str = ""
    angel_pin: str = ""
    angel_totp_secret: str = ""
    angel_api_key: str = ""
    angel_client_code: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
