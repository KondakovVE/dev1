from sqlalchemy.orm import Session
from fastapi import Depends
from app.dependencies import get_db
from models.users import UserInDB, UserCreate, UserPublic


class UsersRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def find_by_email(self, email: str) -> UserInDB:
        query = self.db.query(UserInDB)
        return query.filter(UserInDB.email == email).first()

    def create(self, user: UserCreate) -> UserPublic:
        from app.auth import service as auth_service
        db_user = UserInDB(**user.dict())

        salt = auth_service.get_salt()
        hashed_password = auth_service.hash_password(
            password=user.password, salt=salt)

        db_user.salt = salt
        db_user.password = hashed_password

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        new_user = UserPublic(**db_user.__dict__)
        new_user.access_token = auth_service.create_token(user=db_user)

        return db_user
