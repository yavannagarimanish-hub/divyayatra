"""Temple API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.temple import Temple
from backend.schemas.temple import TempleCreate, TempleRead

router = APIRouter(prefix="/temples", tags=["temples"])


@router.get("/", response_model=list[TempleRead])
def list_temples(db: Session = Depends(get_db)):
    return db.query(Temple).order_by(Temple.name).all()


@router.post("/", response_model=TempleRead, status_code=status.HTTP_201_CREATED)
def create_temple(payload: TempleCreate, db: Session = Depends(get_db)):
    temple = Temple(**payload.model_dump())
    db.add(temple)
    db.commit()
    db.refresh(temple)
    return temple


@router.get("/{temple_id}", response_model=TempleRead)
def get_temple(temple_id: int, db: Session = Depends(get_db)):
    temple = db.query(Temple).filter(Temple.id == temple_id).first()
    if temple is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temple not found")
    return temple
