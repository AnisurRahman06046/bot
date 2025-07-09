# app/webhook/webhook_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.Shop.shop_repository import ShopRepository
from app.webhook.handlers.message_handler import MessageHandler


class WebhookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.shop_repo = ShopRepository(db)

    async def verify_token(self, token: str, challenge: str) -> int | dict:
        if not token or not challenge:
            return {"error": "Missing token or challenge"}

        shop = await self.shop_repo.get_by_verify_token(token)
        return int(challenge) if shop else {"error": "Invalid verification"}

    async def handle_webhook_message(self, body: dict) -> dict:
        try:
            value = body["entry"][0]["changes"][0]["value"]
            phone_number_id = value.get("metadata", {}).get("phone_number_id")
            shop = await self.shop_repo.get_by_phone_number_id(phone_number_id)
            if not shop:
                return {"error": "Unregistered shop"}

            messages = value.get("messages")
            if not messages:
                return {"status": "No messages"}

            handler = MessageHandler(shop)
            await handler.handle(messages[0])

        except Exception as e:
            print("⚠️ Error in webhook service:", e)

        return {"status": "ok"}
