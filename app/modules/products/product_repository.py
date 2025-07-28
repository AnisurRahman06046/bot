# app/modules/product/product_repository.py

from .products_models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_insert(self, shop_id, merchant_id, product_list: list[dict]):
        for p in product_list:
            product = Product(
                product_id=p.get("id"),
                merchant_id=merchant_id,
                shop_id=shop_id,
                name=p.get("name"),
                price=p.get("price", 0.0),
                description=p.get("description", ""),
                status=p.get("status", "active"),
                created_at=datetime.utcnow(),
            )
            self.db.add(product)

        await self.db.commit()

    async def get_products_by_shop(self, shop_id):
        result = await self.db.execute(
            select(Product).where(Product.shop_id == shop_id).limit(10)
        )
        return result.scalars().all()
