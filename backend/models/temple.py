"""Temple SQLAlchemy model."""

from sqlalchemy import Column, Integer, String, Text

from backend.database import Base


class Temple(Base):
    __tablename__ = "temples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    deity = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
