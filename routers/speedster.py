from fastapi import APIRouter, Depends, HTTPException, status

from schemes.speedster import SpeedsterBase, SpeedsterCreate
from repositories.speedster import SpeddsterRepository

router = APIRouter(prefix="/speedsters", tags=['speedsters'])


@router.post('/', response_model=SpeedsterBase, status_code=status.HTTP_201_CREATED)
def create(spedster: SpeedsterCreate, repo: SpeddsterRepository = Depends()):
    db_speedster = repo.create(spedster)
    return SpeedsterBase.from_orm(db_speedster)
