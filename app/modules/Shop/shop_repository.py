# app/modules/shop/shop_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import secrets
from .shop_models import Shop


class ShopRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_verify_token(self, token: str):
        result = await self.db.execute(select(Shop).where(Shop.verify_token == token))
        return result.scalars().first()

    async def get_by_phone_number_id(self, phone_number_id: str):
        result = await self.db.execute(
            select(Shop).where(Shop.phone_number_id == phone_number_id)
        )
        return result.scalars().first()

    async def create_shop(
        self, name: str, phone_number_id: str, access_token: str, merchant_id: str
    ):
        verify_token = secrets.token_urlsafe(16)
        new_shop = Shop(
            name=name,
            phone_number_id=phone_number_id,
            access_token=access_token,
            verify_token=verify_token,
            merchant_id=merchant_id,
        )
        self.db.add(new_shop)
        await self.db.commit()
        await self.db.refresh(new_shop)
        return new_shop

    async def update_bitcommerz_tokens(self, shop_id, token_data: dict):
        await self.db.execute(
            update(Shop)
            .where(Shop.id == shop_id)
            .values(
                # merchant_id=token_data["merchant_id"],
                bitcommerz_access_token=token_data["access_token"],
                bitcommerz_refresh_token=token_data["refresh_token"],
                bitcommerz_token_expires_in=token_data["expires_in"],
            )
        )
        await self.db.commit()
