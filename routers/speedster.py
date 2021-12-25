from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from pydantic.tools import parse_obj_as
from schemes.speedster import Speedster, SpeedsterCreate
from repositories.speedster import SpeedsterRepository

router = APIRouter(prefix="/speedsters", tags=['speedsters'])


@router.post('/', response_model=Speedster, status_code=status.HTTP_201_CREATED)
def create(spedster: SpeedsterCreate, repo: SpeedsterRepository = Depends()):
    db_speedster = repo.create(spedster)
    return Speedster.from_orm(db_speedster)


@router.get('/', response_model=List[Speedster], status_code=status.HTTP_200_OK)
def all(repo: SpeedsterRepository = Depends()):
    db_speedster = repo.all()
    return parse_obj_as(List[Speedster], db_speedster)
