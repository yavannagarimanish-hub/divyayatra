"""Service layer for devotional chat orchestration.

Responsibilities:
- parse user intent (AI logic)
- fetch relevant temples from database
- craft devotional response text
- persist chat history
"""

from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.ai.chatbot_engine import (
    DevotionalIntent,
    build_follow_up_question,
    detect_devotional_intent,
)
from backend.models.chat_history import ChatHistory
from backend.models.temple import Temple
from backend.schemas.chat import ChatResponse, SuggestedTemple


class ChatService:
    """Application service implementing the chatbot workflow."""

    def __init__(self, db: Session):
        self.db = db

    def process_message(self, message: str) -> ChatResponse:
        """Process message end-to-end and return API response model."""

        intent = detect_devotional_intent(message)
        temples = self._find_relevant_temples(intent)

        reply = self._build_reply(intent=intent, temples=temples)
        next_question = build_follow_up_question(intent)

        self._store_chat_history(
            user_message=message,
            ai_reply=reply,
            intent=intent,
        )

        return ChatResponse(
            reply=reply,
            suggested_temples=[
                SuggestedTemple(
                    id=temple.id,
                    name=temple.name,
                    city=temple.city,
                    state=temple.state,
                    deity=temple.deity,
                )
                for temple in temples
            ],
            next_question=next_question,
        )

    def _find_relevant_temples(self, intent: DevotionalIntent) -> list[Temple]:
        """Find temples matching detected devotional intent."""

        query = self.db.query(Temple)

        if intent.deity:
            query = query.filter(Temple.deity.ilike(f"%{intent.deity}%"))

        if intent.location:
            query = query.filter(
                or_(
                    Temple.city.ilike(f"%{intent.location}%"),
                    Temple.state.ilike(f"%{intent.location}%"),
                )
            )

        temples = query.order_by(Temple.name).limit(5).all()

        # Graceful fallback: if strict filters return empty set, show popular
        # devotional options so chat can continue helpfully.
        if not temples:
            temples = self.db.query(Temple).order_by(Temple.name).limit(5).all()

        return temples

    def _build_reply(self, intent: DevotionalIntent, temples: list[Temple]) -> str:
        """Generate human-friendly devotional response text."""

        if not temples:
            return (
                "I could not find temples in the current database yet, "
                "but I can still help you plan your yatra once temples are added."
            )

        opening = "Jai Shri Ram! "
        if intent.deity:
            opening = f"Blessings! I found options aligned with your devotion to {intent.deity}. "

        location_context = ""
        if intent.location:
            location_context = f"These are relevant for {intent.location}. "

        preference_context = ""
        if intent.travel_preference:
            preference_context = (
                f"I also noted your {intent.travel_preference} travel preference. "
            )

        top_names = ", ".join(t.name for t in temples[:3])
        return f"{opening}{location_context}{preference_context}Top suggestions include: {top_names}."

    def _store_chat_history(self, user_message: str, ai_reply: str, intent: DevotionalIntent) -> None:
        """Persist chat exchange for conversation history and analytics."""

        history_row = ChatHistory(
            user_message=user_message,
            ai_reply=ai_reply,
            detected_deity=intent.deity,
            detected_location=intent.location,
            travel_preference=intent.travel_preference,
        )
        self.db.add(history_row)
        self.db.commit()
