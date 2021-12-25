from typing import Literal
from uuid import UUID
import uuid

from pydantic import BaseModel, EmailStr


class SpeedsterBase(BaseModel):
    name: str
    email: EmailStr
    gender: Literal["male", "female", "other"]
    velocity_km_per_hout: float
    height_in_cm: float
    weight_in_kg: float


class SpeedsterCreate(SpeedsterBase):
    password: str


class Speedster(SpeedsterBase):
    id: UUID

    class Config:
        orm_mode = True
