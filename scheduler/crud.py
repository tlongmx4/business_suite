from sqlalchemy.orm import Session
from . import models, schemas


# ----- Business CRUD -----


def create_business(db: Session, business: schemas.BusinessCreate) -> models.Business:
    db_business = models.Business(
        name=business.name,
        open_hour=business.open_hour,
        close_hour=business.close_hour,
        owner_id=business.owner_id,
    )
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def get_business(db: Session, business_id: int) -> models.Business | None:
    return db.query(models.Business).filter(models.Business.id == business_id).first()


def get_businesses(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[models.Business]:
    return db.query(models.Business).offset(skip).limit(limit).all()


# ----- User CRUD -----


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True


# ----- Appointment CRUD -----


def create_appointment(
    db: Session,
    appointment: schemas.AppointmentCreate,
) -> models.Appointment:
    db_appointment = models.Appointment(
        business_id=appointment.business_id,
        staff_user_id=appointment.staff_user_id,
        title=appointment.title,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointments(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    business_id: int | None = None,
    staff_user_id: int | None = None,
) -> list[models.Appointment]:
    query = db.query(models.Appointment)

    if business_id is not None:
        query = query.filter(models.Appointment.business_id == business_id)

    if staff_user_id is not None:
        query = query.filter(models.Appointment.staff_user_id == staff_user_id)

    return query.offset(skip).limit(limit).all()


def get_appointment(db: Session, appointment_id: int) -> models.Appointment | None:
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )


def delete_appointment(db: Session, appointment_id: int) -> bool:
    db_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if not db_appointment:
        return False
    db.delete(db_appointment)
    db.commit()
    return True


def has_appointment_conflict(
    db: Session,
    staff_user_id: int,
    business_id: int,
    start_time,
    end_time,
) -> bool:
    """Check if this staff member has a conflicting appointment in this business."""
    conflict = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.business_id == business_id,
            models.Appointment.staff_user_id == staff_user_id,
            models.Appointment.start_time < end_time,
            models.Appointment.end_time > start_time,
        )
        .first()
    )
    return conflict is not None
