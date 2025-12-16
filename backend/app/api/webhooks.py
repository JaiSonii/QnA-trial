from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.services.webhook_service import WebhookService
from app.api.deps import get_current_admin
from pydantic import BaseModel

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

class WebhookCreate(BaseModel):
    url: str
    description: str | None = None

def get_service(session: Session = Depends(db.get_session)):
    return WebhookService(session)

@router.post("/", dependencies=[Depends(get_current_admin)])
def register_webhook(
    webhook_data: WebhookCreate, 
    service: WebhookService = Depends(get_service)
):
    """
    Register a new URL to receive updates.
    """
    return service.register_webhook(webhook_data.url, webhook_data.description)

@router.get("/", dependencies=[Depends(get_current_admin)])
def list_webhooks(service: WebhookService = Depends(get_service)):
    return service.get_all_webhooks()