# app/modules/shop/shop_routes.py

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from .shop_repository import ShopRepository
from .shop_schemas import ShopCreate

router = APIRouter()


@router.get("/register")
async def serve_register_form():
    return FileResponse("static/register_shop.html")


@router.post("/shops")
async def register_shop(
    shop_data: ShopCreate, db: AsyncSession = Depends(get_async_db)
):
    repo = ShopRepository(db)
    shop = await repo.create_shop(
        name=shop_data.name,
        phone_number_id=shop_data.phone_number_id,
        access_token=shop_data.access_token,
    )
    return {
        "id": str(shop.id),
        "verify_token": shop.verify_token,
        "message": "Shop registered successfully",
    }
