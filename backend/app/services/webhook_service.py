import httpx
from sqlmodel import Session, select
from app.models.webhook import Webhook
from typing import Optional

class WebhookService:
    def __init__(self, session: Optional[Session] = None):
        self.session = session

    def register_webhook(self, url: str, description: Optional[str] = None) -> Webhook:
        if not self.session:
            raise ValueError("Session required for registration")
        webhook = Webhook(url=url, description=description)
        self.session.add(webhook)
        self.session.commit()
        self.session.refresh(webhook)
        return webhook

    def get_all_webhooks(self):
        if not self.session:
            return []
        return self.session.exec(select(Webhook)).all()

    @staticmethod
    async def send_notifications(webhook_urls: list[str], question_data: dict):
        """
        Sends HTTP POST requests to the list of URLs. 
        Does NOT depend on a database session.
        """
        payload = {
            "event": "question.answered",
            "data": question_data
        }

        async with httpx.AsyncClient() as client:
            for url in webhook_urls:
                try:
                    await client.post(url, json=payload, timeout=5.0)
                    print(f"Webhook sent to {url}")
                except Exception as e:
                    print(f"Failed to send webhook to {url}: {e}")