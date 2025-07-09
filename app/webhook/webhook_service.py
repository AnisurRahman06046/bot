# app/webhook/webhook_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.Shop.shop_repository import ShopRepository
from utils import (
    send_dynamic_whatsapp_message,
    send_dynamic_buttons,
    send_dynamic_product_list,
)


class WebhookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.shop_repo = ShopRepository(db)

    async def verify_token(self, token: str, challenge: str) -> int | dict:
        if not token or not challenge:
            return {"error": "Missing token or challenge"}

        shop = await self.shop_repo.get_by_verify_token(token)
        if shop:
            return int(challenge)
        return {"error": "Invalid verification"}

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

            msg = messages[0]
            sender = msg["from"]
            msg_type = msg.get("type")

            if msg_type == "text":
                text = msg["text"]["body"].lower()
                if text in ["hi", "hello", "start"]:
                    send_dynamic_buttons(sender, shop)
                else:
                    send_dynamic_whatsapp_message(
                        sender, "Please type 'Hi' to get started.", shop
                    )

            elif msg_type == "interactive":
                interactive = msg["interactive"]
                if interactive["type"] == "button_reply":
                    button_id = interactive["button_reply"]["id"]
                    await self._handle_button_reply(button_id, sender, shop)

                elif interactive["type"] == "list_reply":
                    selected_id = interactive["list_reply"]["id"]
                    send_dynamic_whatsapp_message(
                        sender, f"You selected: {selected_id}", shop
                    )

        except Exception as e:
            print("Error in webhook service:", e)

        return {"status": "ok"}

    async def _handle_button_reply(self, button_id: str, sender: str, shop):
        if button_id == "browse_products":
            send_dynamic_product_list(sender, shop)
        elif button_id == "view_cart":
            send_dynamic_whatsapp_message(sender, "🛒 Your cart is empty.", shop)
        elif button_id == "place_order":
            send_dynamic_whatsapp_message(sender, "📦 You have no active orders.", shop)
        else:
            send_dynamic_whatsapp_message(sender, "Unknown button option.", shop)
