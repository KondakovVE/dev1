from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from fastapi import Depends

from models.speedster import Speedster
from app.dependencies import get_db
from schemes.speedster import SpeedsterCreate


class SpeedsterRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find(self, uuid: UUID) -> Speedster:
        query = self.db.query(Speedster)
        return query.filter(Speedster.id == uuid).first()

    def find_by_email(self, email: str) -> Speedster:
        query = self.db.query(Speedster)
        return query.filter(Speedster.email == email).first()

    def all(self) -> List[Speedster]:
        query = self.db.query(Speedster)
        return query.all()

    def create(self, speedster: SpeedsterCreate) -> Speedster:
        db_speedster = Speedster(**speedster.dict())

        self.db.add(db_speedster)
        self.db.commit()
        self.db.refresh(db_speedster)

        return db_speedster
