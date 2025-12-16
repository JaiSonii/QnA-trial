from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import db
from app.api import auth, questions, webhooks
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_tables()
    yield

def create_app()->FastAPI:
    app = FastAPI(title="Hemut Trial Q&A", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(questions.router)
    app.include_router(webhooks.router)

    @app.get("/")
    def root():
        return {"message": "Hemut Q&A API is running"}
    
    return app