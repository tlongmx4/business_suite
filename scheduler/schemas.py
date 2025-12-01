from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ----- Business Schemas -----


class BusinessBase(BaseModel):
    name: str
    open_hour: int
    close_hour: int


class BusinessCreate(BusinessBase):
    # for now we accept owner_id explicitly;
    # later this will come from the authenticated user
    owner_id: int


class Business(BusinessBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ----- User Schemas -----


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# ----- Appointment Schemas -----


class AppointmentBase(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime


class AppointmentCreate(AppointmentBase):
    business_id: int
    staff_user_id: int  # was user_id


class Appointment(AppointmentBase):
    id: int
    business_id: int
    staff_user_id: int

    class Config:
        orm_mode = True
