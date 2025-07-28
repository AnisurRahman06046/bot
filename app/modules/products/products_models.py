from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(String, unique=True)  # From Bitcommerz
    merchant_id = Column(String)
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id"))
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
