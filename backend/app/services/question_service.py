from sqlmodel import Session, select
from app.models.question import Question, QuestionStatus
from app.schemas.question import QuestionCreate

class QuestionService:
    def __init__(self, session: Session):
        self.session = session

    def create_question(self, question_data: QuestionCreate, user_id: int | None = None):
        question = Question(
            content=question_data.content,
            user_id=user_id
        )
        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def get_all_questions(self):
        statement = select(Question).order_by(
            (Question.status == QuestionStatus.ESCALATED).desc(),
            Question.created_at.desc()
        )
        return self.session.exec(statement).all() #type: ignore

    def mark_answered(self, question_id: int, answer_text: str):
        question = self.session.get(Question, question_id)
        if question:
            question.status = QuestionStatus.ANSWERED
            question.answer = answer_text
            self.session.add(question)
            self.session.commit()
            self.session.refresh(question)
        return question