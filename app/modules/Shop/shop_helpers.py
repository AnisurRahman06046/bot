# app/modules/shop/shop_helpers.py
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

BITCOMMERZ_TOKEN_URL = "https://commerzly.onrender.com/api/v1/oauth/token"
# BITCOMMERZ_CLIENT_ID = "client_36p8h5dtz"
# BITCOMMERZ_CLIENT_SECRET = "secret_bxcamenj31a"
# REDIRECT_URI = "https://b5ebcda3abe2.ngrok-free.app/register"
# from app.core.config import settings

from app.modules.botConfig.bot_repository import BotAppRepository


async def get_bitcommerz_tokens(code: str, db: AsyncSession) -> dict | None:

    repo = BotAppRepository(db)
    botApp = await repo.get_app()
    payload = {
        "grant_type": "authorization_code",
        "client_id": botApp.bot_clinetId,
        "client_secret": botApp.bot_secretKey,
        "code": code,
        "redirect_uri": botApp.redirect_url,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(BITCOMMERZ_TOKEN_URL, json=payload)
        if response.status_code == 200:
            return response.json()
        return None
