from uuid import uuid4

from app.databases import Model

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


from pydantic import BaseModel, EmailStr
from typing import Optional


class AccessToken(BaseModel):
    token: str
    type: str


class UserInDB(Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    salt = Column(String)


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    password: str
    salt: str


class UserPublic(UserBase):
    access_token: Optional[AccessToken]
