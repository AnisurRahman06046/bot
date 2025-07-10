# # app/modules/shop/shop_routes.py

# from fastapi import APIRouter, Depends
# from fastapi.responses import FileResponse
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.database import get_async_db
# from .shop_repository import ShopRepository
# from .shop_schemas import ShopCreate

# router = APIRouter()


# @router.get("/register")
# async def serve_register_form():
#     return FileResponse("static/register_shop.html")


# @router.post("/shops")
# async def register_shop(
#     shop_data: ShopCreate, db: AsyncSession = Depends(get_async_db)
# ):
#     repo = ShopRepository(db)
#     shop = await repo.create_shop(
#         name=shop_data.name,
#         phone_number_id=shop_data.phone_number_id,
#         access_token=shop_data.access_token,
#     )
#     return {
#         "id": str(shop.id),
#         "verify_token": shop.verify_token,
#         "message": "Shop registered successfully",
#     }


# app/modules/shop/shop_routes.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from .shop_repository import ShopRepository
from .shop_schemas import RegisterWithBitcommerz
from .shop_helpers import get_bitcommerz_tokens

router = APIRouter()


@router.get("/register")
async def serve_register_form():
    return FileResponse("static/register_shop.html")


@router.post("/shops")
async def register_shop_with_bitcommerz(
    data: RegisterWithBitcommerz, db: AsyncSession = Depends(get_async_db)
):
    # 1. Call Bitcommerz token exchange
    token_data = await get_bitcommerz_tokens(data.code, db)
    if not token_data:
        raise HTTPException(status_code=400, detail="Bitcommerz token exchange failed")

    # 2. Create Shop
    repo = ShopRepository(db)
    shop = await repo.create_shop(
        name=data.name,
        phone_number_id=data.phone_number_id,
        access_token=data.access_token,
        merchant_id=token_data["merchant_id"],
    )

    # 3. Save Bitcommerz tokens
    await repo.update_bitcommerz_tokens(
        shop.id,
        {
            # "merchant_id": token_data["merchant_id"],
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data["expires_in"],
        },
    )

    return {
        "id": str(shop.id),
        "verify_token": shop.verify_token,
        "message": "Shop registered successfully",
    }
