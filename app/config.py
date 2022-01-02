from pydantic import BaseSettings
from pydantic.main import BaseModel


class DBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


class TokenSettings(BaseSettings):
    iss: str
    token_type: str
    token_audience: str
    token_expire_minutes: int
    token_algorithm: str
    secret_key: str

    class Config:
        env_prefix = "JWT_"
        env_file = ".env"
