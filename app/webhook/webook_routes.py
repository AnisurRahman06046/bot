# app/webhook/webhook_routes.py

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.webhook.webhook_service import WebhookService

router = APIRouter()


@router.get("/webhook")
async def verify_token(request: Request, db: AsyncSession = Depends(get_async_db)):
    params = dict(request.query_params)
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    service = WebhookService(db)
    return await service.verify_token(token, challenge)


@router.post("/webhook")
async def receive_message(request: Request, db: AsyncSession = Depends(get_async_db)):
    body = await request.json()
    print("Incoming:", body)

    service = WebhookService(db)
    return await service.handle_webhook_message(body)
