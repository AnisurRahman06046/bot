# app/webhook/handlers/button_handler.py

from utils import send_dynamic_whatsapp_message, send_dynamic_product_list


async def handle_button_reply(button_id: str, sender: str, shop):
    match button_id:
        case "browse_products":
            send_dynamic_product_list(sender, shop)
        case "view_cart":
            send_dynamic_whatsapp_message(sender, "🛒 Your cart is empty.", shop)
        case "place_order":
            send_dynamic_whatsapp_message(sender, "📦 You have no active orders.", shop)
        case _:
            send_dynamic_whatsapp_message(sender, "Unknown button option.", shop)
