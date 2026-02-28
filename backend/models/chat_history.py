"""Chat history model for storing user and assistant messages."""

from sqlalchemy import Column, DateTime, Integer, String, Text, func

from backend.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    ai_reply = Column(Text, nullable=False)
    detected_deity = Column(String(100), nullable=True, index=True)
    detected_location = Column(String(100), nullable=True, index=True)
    travel_preference = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
