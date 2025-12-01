from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import schemas, crud

router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Business)
def create_business(
    business: schemas.BusinessCreate,
    db: Session = Depends(get_db),
):
    # (later we'll enforce that owner_id == current_user.id)
    db_business = crud.create_business(db=db, business=business)
    return db_business


@router.get("/", response_model=list[schemas.Business])
def read_businesses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.get_businesses(db=db, skip=skip, limit=limit)


@router.get("/{business_id}", response_model=schemas.Business)
def read_business(
    business_id: int,
    db: Session = Depends(get_db),
):
    db_business = crud.get_business(db=db, business_id=business_id)
    if db_business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return db_business
