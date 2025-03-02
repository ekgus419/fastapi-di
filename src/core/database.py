from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.settings import settings

DATABASE_URL = (
    f"mysql+mysqldb://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
)

# settings.SQL_ECHO 값을 echo 옵션에 전달
engine = create_engine(DATABASE_URL, echo=settings.SQL_ECHO)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
