# app/webhook/handlers/message_handler.py

from utils import send_dynamic_whatsapp_message, send_dynamic_buttons
from app.webhook.handlers.button_handler import handle_button_reply


class MessageHandler:
    def __init__(self, shop):
        self.shop = shop

    async def handle(self, msg: dict):
        msg_type = msg.get("type")
        sender = msg.get("from")

        if msg_type == "text":
            return await self._handle_text(msg, sender)
        elif msg_type == "interactive":
            return await self._handle_interactive(msg, sender)

    async def _handle_text(self, msg, sender: str):
        text = msg["text"]["body"].lower()
        if text in ["hi", "hello", "start"]:
            send_dynamic_buttons(sender, self.shop)
        else:
            send_dynamic_whatsapp_message(
                sender, "Please type 'Hi' to get started.", self.shop
            )

    async def _handle_interactive(self, msg, sender: str):
        interactive = msg["interactive"]
        if interactive["type"] == "button_reply":
            button_id = interactive["button_reply"]["id"]
            await handle_button_reply(button_id, sender, self.shop)
        elif interactive["type"] == "list_reply":
            selected_id = interactive["list_reply"]["id"]
            send_dynamic_whatsapp_message(
                sender, f"You selected: {selected_id}", self.shop
            )
