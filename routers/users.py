from loguru import logger
from fastapi import APIRouter, Depends, Body,  HTTPException, status
from app.auth import service as auth_service
from repositories.users import UsersRepository
from app.auth import get_user_from_token

from models.users import UserInDB, UserPublic, UserCreate

router = APIRouter(prefix="/users", tags=['users'])


@router.get('/me', response_model=UserPublic)
def me(this_user: UserInDB = Depends(get_user_from_token)):
    user = UserPublic(**this_user.__dict__)
    user.access_token = auth_service.create_token(user=this_user)
    return user


@router.post('/register', response_model=UserPublic, status_code=201)
def register(user: UserCreate = Body(..., embed=True), repo: UsersRepository = Depends()):
    logger.debug('API Register user')

    new_user = repo.find_by_email(user.email)
    if (new_user):
        raise HTTPException(
            status_code=400, detail="Пользователь с таким адресом уже зарегистрирован")

    new_user = repo.create(user)

    return new_user.__dict__


@router.post('/login', response_model=UserPublic)
def login(login: UserCreate = Body(..., embed=True), repo: UsersRepository = Depends()):
    logger.debug('API Login')

    user = repo.find_by_email(login.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с таким адресом не обнаружен")

    if auth_service.verify_password(password=login.password, salt=user.salt, hashed_pw=user.password):
        public = UserPublic(**user.__dict__)
        public.access_token = auth_service.create_token(user=user)
        return public
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
