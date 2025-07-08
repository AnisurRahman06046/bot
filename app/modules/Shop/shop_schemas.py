from pydantic import BaseModel


class ShopCreate(BaseModel):
    name: str
    phone_number_id: str
    access_token: str
    # verify_token: str
