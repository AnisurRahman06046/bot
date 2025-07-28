# app/webhook/handlers/button_handler.py

from utils import send_dynamic_whatsapp_message, send_dynamic_product_list
from app.modules.merchant.handlers.product_handlers import fetch_products
from app.modules.products.product_repository import ProductRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db


async def handle_button_reply(button_id: str, sender: str, shop):
    match button_id:
        case "browse_products":
            db: AsyncSession = await get_async_db().__anext__()  # Inject DB
            product_repo = ProductRepository(db)
            # products = await fetch_products(
            #     shop.merchant_id, shop.bitcommerz_access_token
            # )
            products = await product_repo.get_products_by_shop(shop.id)
            if products:
                product_data = [
                    {
                        "id": p.product_id,
                        "name": p.name,
                        "price": p.price,
                        "short_description": p.description,
                    }
                    for p in products
                ]
                send_dynamic_product_list(sender, shop, product_data)
            else:
                send_dynamic_whatsapp_message(
                    sender, "⚠️ Unable to fetch products right now.", shop
                )
        case "view_cart":
            send_dynamic_whatsapp_message(sender, "🛒 Your cart is empty.", shop)
        case "place_order":
            send_dynamic_whatsapp_message(sender, "📦 You have no active orders.", shop)
        case _:
            send_dynamic_whatsapp_message(sender, "Unknown button option.", shop)
