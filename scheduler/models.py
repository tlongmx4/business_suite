from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    # simple business hours for now (0–23)
    open_hour = Column(Integer, nullable=False, default=9)
    close_hour = Column(Integer, nullable=False, default=17)

    # who owns/created this business
    owner_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # relationships
    owner = relationship("User", back_populates="businesses_owned")
    appointments = relationship("Appointment", back_populates="business")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # businesses this user owns
    businesses_owned = relationship("Business", back_populates="owner")

    # appointments this user is assigned to (staff)
    appointments = relationship("Appointment", back_populates="staff_user")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    # which business this appointment belongs to
    business_id = Column(Integer, ForeignKey("businesses.id"), index=True, nullable=False)

    # which user (staff) this appointment is for
    staff_user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    title = Column(String, index=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    business = relationship("Business", back_populates="appointments")
    staff_user = relationship("User", back_populates="appointments")
