from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.modules.Shop.shop_routes import router as shop_router
from app.webhook.webook_routes import router as webhook_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(shop_router)
app.include_router(webhook_router)
