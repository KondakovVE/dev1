from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, ValidationError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
import bcrypt
import jwt
from passlib.context import CryptContext

from models.users import UserInDB, AccessToken
from repositories.users import UsersRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTCreds(BaseModel):
    email: EmailStr


class JWTMeta(BaseModel):
    iss: str
    aud: str
    iat: float
    exp: float


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """
    pass


class AuthService:
    def get_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str):
        return pwd_context.hash(password+salt)

    def verify_password(self, *, password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password+salt, hash=hashed_pw)

    def get_user_id_from_token(self, *, token: str
                               ) -> Optional[str]:
        from app.dependencies import get_token_settings

        settings = get_token_settings()
        try:
            decoded_token = jwt.decode(token, str(
                settings.secret_key), audience=settings.token_audience, algorithms=[settings.token_algorithm])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=401,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload.email

    def create_token(self, *, user) -> AccessToken:
        from app.dependencies import get_token_settings

        settings = get_token_settings()

        if not user:
            return None

        jwt_meta = JWTMeta(
            iss=settings.iss,
            aud=settings.token_audience,
            iat=datetime.timestamp(datetime.now()),
            exp=datetime.timestamp(
                datetime.now()+timedelta(minutes=settings.token_expire_minutes))
        )

        jwt_cred = JWTCreds(email=user.email)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_cred.dict()
        )

        token = jwt.encode(
            token_payload.dict(), settings.secret_key, algorithm=settings.token_algorithm)

        return AccessToken(type="bearer", token=token)


service = AuthService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/users/login/token/")


async def get_user_from_token(
    *,
    token: AccessToken = Depends(oauth2_scheme),
        repo: UsersRepository = Depends()) -> Optional[UserInDB]:
    logger.debug('get user from token')
    try:
        email = service.get_user_id_from_token(token=token)
        user = repo.find_by_email(email=email)
    except Exception as e:
        raise e

    return user
