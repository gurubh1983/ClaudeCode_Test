from __future__ import annotations

import asyncio
from datetime import datetime
import json

import httpx
import pyotp
import websockets


class AngelOneClient:
    def __init__(self, api_key: str, client_code: str, pin: str, totp_secret: str):
        self.api_key = api_key
        self.client_code = client_code
        self.pin = pin
        self.totp_secret = totp_secret
        self.jwt_token: str | None = None
        self.feed_token: str | None = None
        self.base = "https://apiconnect.angelone.in/rest"

    async def login(self) -> None:
        totp = pyotp.TOTP(self.totp_secret).now()
        payload = {"clientcode": self.client_code, "password": self.pin, "totp": totp}
        headers = {"X-PrivateKey": self.api_key}
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(f"{self.base}/auth/angelbroking/user/v1/loginByPassword", json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()["data"]
            self.jwt_token = data["jwtToken"]
            self.feed_token = data["feedToken"]

    async def get_candles(self, exchange: str, symboltoken: str, interval: str, from_date: str, to_date: str) -> list:
        return await self._post("/secure/angelbroking/historical/v1/getCandleData", {
            "exchange": exchange,
            "symboltoken": symboltoken,
            "interval": interval,
            "fromdate": from_date,
            "todate": to_date,
        })

    async def get_option_chain(self, symbol: str, expiry: str | None = None) -> dict:
        payload = {"name": symbol}
        if expiry:
            payload["expirydate"] = expiry
        return await self._post("/secure/angelbroking/order/v1/getOptionGreek", payload)

    async def get_ltp(self, exchange: str, tradingsymbol: str, symboltoken: str) -> dict:
        return await self._post("/secure/angelbroking/order/v1/getLtpData", {
            "exchange": exchange,
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
        })

    async def _post(self, path: str, payload: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "X-PrivateKey": self.api_key,
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(f"{self.base}{path}", json=payload, headers=headers)
            r.raise_for_status()
            return r.json().get("data", {})

    async def stream_ticks(self, tokens: list[str]):
        if not self.feed_token:
            await self.login()
        backoff = 1
        while True:
            try:
                async with websockets.connect("wss://smartapisocket.angelone.in/smart-stream", ping_interval=20) as ws:
                    request = {
                        "action": 1,
                        "params": {"mode": 3, "tokenList": [{"exchangeType": 1, "tokens": tokens}]},
                    }
                    await ws.send(json.dumps(request))
                    async for message in ws:
                        yield {"timestamp": datetime.utcnow().isoformat(), "raw": message}
                backoff = 1
            except Exception:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30)
