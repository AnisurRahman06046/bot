from fastapi import FastAPI, Request
from config import VERIFY_TOKEN
from utils import (
    send_whatsapp_message,
    send_whatsapp_buttons,
    send_product_list
)
import json

app = FastAPI()

@app.get("/webhook")
async def verify_token(request: Request):
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params["hub.challenge"])
    return {"error": "Invalid verification"}

@app.post("/webhook")
async def receive_message(request: Request):
    print("testing.............................")
    body = await request.json()
    print("Incoming:", json.dumps(body, indent=2))

    try:
        messages = body["entry"][0]["changes"][0]["value"].get("messages")

        if messages:
            msg = messages[0]
            sender = msg["from"]
            msg_type = msg.get("type")

            # Handle text messages like "hi"
            if msg_type == "text":
                text = msg["text"]["body"].lower()
                print(f"Text from {sender}: {text}")

                if text in ["hi", "hello", "start"]:
                    send_whatsapp_buttons(sender)
                else:
                    send_whatsapp_message(sender, "Please type 'Hi' to get started.")

            # Handle interactive messages (button replies and list replies)
            elif msg_type == "interactive":
                interactive = msg["interactive"]
                if interactive["type"] == "button_reply":
                    button_id = interactive["button_reply"]["id"]
                    print(f"Button reply id: {button_id}")

                    if button_id == "browse_products":
                        send_product_list(sender)
                    elif button_id == "view_cart":
                        send_whatsapp_message(sender, "🛒 Your cart is currently empty.")
                    elif button_id == "place_order":
                        send_whatsapp_message(sender, "📦 You have no active orders.")
                    else:
                        send_whatsapp_message(sender, "Unknown button option.")

                elif interactive["type"] == "list_reply":
                    selected_id = interactive["list_reply"]["id"]
                    print(f"List reply: {selected_id}")

                    if selected_id == "airpods_pro":
                        send_whatsapp_message(sender, "🎧 You selected *AirPods Pro* - $249.")
                    elif selected_id == "samsung_watch":
                        send_whatsapp_message(sender, "⌚ You selected *Samsung Galaxy Watch* - $199.")
                    elif selected_id == "jbl_headphones":
                        send_whatsapp_message(sender, "🎶 You selected *JBL Tune 760NC* - $129.")
                    elif selected_id == "bose_qc45":
                        send_whatsapp_message(sender, "🎧 You selected *Bose QC 45* - $299.")
                    else:
                        send_whatsapp_message(sender, "❓ Unknown product selected.")

            else:
                # fallback for unsupported message types
                send_whatsapp_message(sender, "Sorry, I can only understand text and button clicks right now.")

    except Exception as e:
        print("Error handling message:", e)

    return {"status": "ok"}
