# app/webhook/webhook_routes.py

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.modules.Shop.shop_repository import ShopRepository
from utils import (
    send_dynamic_whatsapp_message,
    send_dynamic_buttons,
    send_dynamic_product_list,
)
import json

router = APIRouter()


@router.get("/webhook")
async def verify_token(request: Request, db: AsyncSession = Depends(get_async_db)):
    params = dict(request.query_params)
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if params.get("hub.mode") == "subscribe" and token and challenge:
        shop_repo = ShopRepository(db)
        shop = await shop_repo.get_by_verify_token(token)
        if shop:
            return int(challenge)

    return {"error": "Invalid verification"}


@router.post("/webhook")
async def receive_message(request: Request, db: AsyncSession = Depends(get_async_db)):
    body = await request.json()
    print("Incoming:", json.dumps(body, indent=2))

    try:
        value = body["entry"][0]["changes"][0]["value"]
        phone_number_id = value.get("metadata", {}).get("phone_number_id")

        shop_repo = ShopRepository(db)
        shop = await shop_repo.get_by_phone_number_id(phone_number_id)
        if not shop:
            return {"error": "Unregistered shop"}

        messages = value.get("messages")
        if messages:
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
                    if button_id == "browse_products":
                        send_dynamic_product_list(sender, shop)
                    elif button_id == "view_cart":
                        send_dynamic_whatsapp_message(
                            sender, "🛒 Your cart is empty.", shop
                        )
                    elif button_id == "place_order":
                        send_dynamic_whatsapp_message(
                            sender, "📦 You have no active orders.", shop
                        )
                    else:
                        send_dynamic_whatsapp_message(
                            sender, "Unknown button option.", shop
                        )

                elif interactive["type"] == "list_reply":
                    selected_id = interactive["list_reply"]["id"]
                    send_dynamic_whatsapp_message(
                        sender, f"You selected: {selected_id}", shop
                    )

    except Exception as e:
        print("Error handling message:", e)

    return {"status": "ok"}
