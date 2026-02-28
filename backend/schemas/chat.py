"""Pydantic schemas for chatbot interactions."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat payload from the user."""

    message: str = Field(min_length=1, max_length=2000)


class SuggestedTemple(BaseModel):
    """Lightweight temple projection sent back in AI responses."""

    id: int
    name: str
    city: str
    state: str
    deity: str


class ChatResponse(BaseModel):
    """Response contract for chatbot endpoint."""

    reply: str
    suggested_temples: list[SuggestedTemple]
    next_question: str
