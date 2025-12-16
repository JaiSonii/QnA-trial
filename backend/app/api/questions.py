from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.models.question import Question, QuestionStatus, Reply
from app.schemas.question import QuestionCreate, QuestionResponse, ReplyCreate, ReplyResponse
from app.services.question_service import QuestionService
from app.services.ws_service import manager
from app.services.rag_service import rag_service
from app.services.webhook_service import WebhookService 
from app.api.deps import get_current_admin  
from fastapi.concurrency import run_in_threadpool
from app.models.user import User 
from app.api.deps import get_current_user_optional
from typing import Optional

router = APIRouter(prefix="/questions", tags=["Questions"])

def get_service(session: Session = Depends(db.get_session)):
    return QuestionService(session)

def get_webhook_service(session: Session = Depends(db.get_session)):
    return WebhookService(session)

@router.post("/", response_model=QuestionResponse)
async def submit_question(
    q_data: QuestionCreate, 
    background_tasks: BackgroundTasks,
    service: QuestionService = Depends(get_service),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else None
    new_q = await run_in_threadpool(service.create_question, q_data, user_id)
    
    await manager.broadcast({
        "type": "NEW_QUESTION",
        "data": new_q.model_dump(mode="json")
    })
    
    suggestion = await run_in_threadpool(rag_service.generate_answer, new_q.content)
    new_q.answer = f"(AI Suggestion): {suggestion}"

    def save_answer():
        service.session.add(new_q)
        service.session.commit()
        service.session.refresh(new_q)
    await run_in_threadpool(save_answer)
    
    return new_q

@router.post("/{question_id}/reply", response_model=ReplyResponse)
async def post_reply(
    question_id: int,
    reply_data: ReplyCreate,
    session: Session = Depends(db.get_session),
):
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    new_reply = Reply(
        question_id=question_id, 
        content=reply_data.content,
        is_admin=False 
    )
    session.add(new_reply)
    session.commit()
    session.refresh(new_reply)

    await manager.broadcast({
        "type": "NEW_REPLY",
        "data": {
            "question_id": question_id,
            "reply_content": new_reply.content
        }
    })
    
    return new_reply

@router.get("/", response_model=list[QuestionResponse])
def get_questions(service: QuestionService = Depends(get_service)):
    return service.get_all_questions()

@router.patch("/{question_id}/answer", response_model=QuestionResponse)
def mark_question_answered(
    question_id: int, 
    answer_text: str,
    background_tasks: BackgroundTasks,
    _ = Depends(get_current_admin), 
    service: QuestionService = Depends(get_service),
    webhook_service: WebhookService = Depends(get_webhook_service) # <--- Fixed Dependency
):
    updated_q = service.mark_answered(question_id, answer_text)
    
    if not updated_q:
        raise HTTPException(status_code=404, detail="Question not found")
        
    webhooks = webhook_service.get_all_webhooks()
    urls = [w.url for w in webhooks]

    q_data = {
        "id": updated_q.id,
        "content": updated_q.content,
        "answer": updated_q.answer,
        "answered_at": updated_q.created_at.isoformat()
    }

    if urls:
        background_tasks.add_task(WebhookService.send_notifications, urls, q_data)

    return updated_q


@router.patch("/{question_id}/status", response_model=QuestionResponse)
def update_status(
    question_id: int, 
    status: QuestionStatus,
    _ = Depends(get_current_admin), 
    session: Session = Depends(db.get_session)
):
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    question.status = status
    session.add(question)
    session.commit()
    session.refresh(question)
    return question

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)