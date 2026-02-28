"""Temple request and response schemas."""

from pydantic import BaseModel


class TempleBase(BaseModel):
    name: str
    city: str
    state: str
    deity: str
    description: str | None = None


class TempleCreate(TempleBase):
    pass


class TempleRead(TempleBase):
    id: int

    class Config:
        from_attributes = True
