from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    SQL_ECHO: bool = False
    LOG_SQL_PRETTY: bool = False

    # JWT 관련 설정
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1
    JWT_REFRESH_EXPIRATION_MINUTES: int = 1440

    class Config:
        # 순서대로 로드되며, 이후 파일의 값이 우선합니다.
        env_file = ["src/env/.env.common", "src/env/.env.dev"]

settings = Settings()
