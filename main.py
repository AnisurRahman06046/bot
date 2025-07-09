# from fastapi import FastAPI, Request
# from config import VERIFY_TOKEN
# from utils import send_whatsapp_message, send_whatsapp_buttons, send_product_list
# import json

# app = FastAPI()


# @app.get("/webhook")
# async def verify_token(request: Request):
#     params = dict(request.query_params)
#     if (
#         params.get("hub.mode") == "subscribe"
#         and params.get("hub.verify_token") == VERIFY_TOKEN
#     ):
#         return int(params["hub.challenge"])
#     return {"error": "Invalid verification"}


# @app.post("/webhook")
# async def receive_message(request: Request):
#     print("testing.............................")
#     body = await request.json()
#     print("Incoming:", json.dumps(body, indent=2))

#     try:
#         messages = body["entry"][0]["changes"][0]["value"].get("messages")

#         if messages:
#             msg = messages[0]
#             sender = msg["from"]
#             msg_type = msg.get("type")

#             # Handle text messages like "hi"
#             if msg_type == "text":
#                 text = msg["text"]["body"].lower()
#                 print(f"Text from {sender}: {text}")

#                 if text in ["hi", "hello", "start"]:
#                     send_whatsapp_buttons(sender)
#                 else:
#                     send_whatsapp_message(sender, "Please type 'Hi' to get started.")

#             # Handle interactive messages (button replies and list replies)
#             elif msg_type == "interactive":
#                 interactive = msg["interactive"]
#                 if interactive["type"] == "button_reply":
#                     button_id = interactive["button_reply"]["id"]
#                     print(f"Button reply id: {button_id}")

#                     if button_id == "browse_products":
#                         send_product_list(sender)
#                     elif button_id == "view_cart":
#                         send_whatsapp_message(
#                             sender, "🛒 Your cart is currently empty."
#                         )
#                     elif button_id == "place_order":
#                         send_whatsapp_message(sender, "📦 You have no active orders.")
#                     else:
#                         send_whatsapp_message(sender, "Unknown button option.")

#                 elif interactive["type"] == "list_reply":
#                     selected_id = interactive["list_reply"]["id"]
#                     print(f"List reply: {selected_id}")

#                     if selected_id == "airpods_pro":
#                         send_whatsapp_message(
#                             sender, "🎧 You selected *AirPods Pro* - $249."
#                         )
#                     elif selected_id == "samsung_watch":
#                         send_whatsapp_message(
#                             sender, "⌚ You selected *Samsung Galaxy Watch* - $199."
#                         )
#                     elif selected_id == "jbl_headphones":
#                         send_whatsapp_message(
#                             sender, "🎶 You selected *JBL Tune 760NC* - $129."
#                         )
#                     elif selected_id == "bose_qc45":
#                         send_whatsapp_message(
#                             sender, "🎧 You selected *Bose QC 45* - $299."
#                         )
#                     else:
#                         send_whatsapp_message(sender, "❓ Unknown product selected.")

#             else:
#                 # fallback for unsupported message types
#                 send_whatsapp_message(
#                     sender,
#                     "Sorry, I can only understand text and button clicks right now.",
#                 )

#     except Exception as e:
#         print("Error handling message:", e)

#     return {"status": "ok"}


from fastapi import FastAPI, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.modules.Shop.shop_repository import ShopRepository
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from utils import (
    send_dynamic_whatsapp_message,
    send_dynamic_buttons,
    send_dynamic_product_list,
)
from app.modules.Shop.shop_schemas import ShopCreate
from app.modules.Shop.shop_routes import router as shop_router
from fastapi import HTTPException
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(shop_router)


@app.get("/webhook")
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


@app.post("/webhook")
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
