from sqlalchemy import Column, String, Integer
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Shop(Base):
    __tablename__ = "shops"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone_number_id = Column(String, unique=True, nullable=False)
    access_token = Column(String, nullable=False)
    merchant_id = Column(String, nullable=False)
    verify_token = Column(String, unique=True, nullable=False)
    # Optional fields for Bitcommerz tokens
    bitcommerz_access_token = Column(String, nullable=True)
    bitcommerz_refresh_token = Column(String, nullable=True)
    bitcommerz_token_expires_in = Column(Integer, nullable=True)
