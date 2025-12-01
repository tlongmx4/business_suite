from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import schemas, crud

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Appointment)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
):
    # Check for appointment conflicts for this staff member and time range
    if crud.has_appointment_conflict(
        db=db,
        staff_user_id=appointment.staff_user_id,
        business_id=appointment.business_id,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
    ):
        raise HTTPException(
            status_code=409,
            detail="This staff member already has an overlapping appointment in that time slot.",
        )

    return crud.create_appointment(db=db, appointment=appointment)


@router.get("/", response_model=list[schemas.Appointment])
def read_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_appointments(db=db, skip=skip, limit=limit)


@router.get("/{appointment_id}", response_model=schemas.Appointment)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment(db=db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_appointment(db=db, appointment_id=appointment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"detail": "Appointment deleted"}
