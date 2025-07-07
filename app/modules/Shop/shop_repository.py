from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
        self, name: str, phone_number_id: str, access_token: str, verify_token: str
    ):
        new_shop = Shop(
            name=name,
            phone_number_id=phone_number_id,
            access_token=access_token,
            verify_token=verify_token,
        )
        self.db.add(new_shop)
        await self.db.commit()
        await self.db.refresh(new_shop)
        return new_shop
