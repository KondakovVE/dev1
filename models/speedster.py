from uuid import uuid4

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID

from app.databases import Model


class Speedster(Model):
    __tablename__ = "speedsters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    velocity_km_per_hout = Column(Float)
    height_in_cm = Column(Float)
    weight_in_kg = Column(Float)
