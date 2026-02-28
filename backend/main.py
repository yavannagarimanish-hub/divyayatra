"""FastAPI entrypoint for DivyaYatra backend."""

from fastapi import FastAPI

from backend.database import Base, engine
from backend.models import ChatHistory, Temple  # noqa: F401 - required for metadata discovery
from backend.routes.chat import router as chat_router
from backend.routes.temples import router as temple_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DivyaYatra API", version="0.1.0")


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


app.include_router(temple_router)
app.include_router(chat_router)
