from sqlalchemy import Column, Integer, String
from src.entity.base_entity import Base


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    password = Column(String(128), nullable=False)
    # Refresh Token 저장 컬럼: 로그아웃 시 값을 지워서 해당 토큰을 무효화
    current_refresh_token = Column(String(512), nullable=True)
