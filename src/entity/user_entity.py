from sqlalchemy import Column, Integer, String, DateTime, func
from src.entity.base_entity import Base

class UserEntity(Base):
    __tablename__ = "users"

    seq = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    # Refresh Token 저장 컬럼: 로그아웃 시 값을 지워서 해당 토큰을 무효화
    current_refresh_token = Column(String(512), nullable=True)
    type = Column(String(3), default='100', nullable=False)
    status = Column(String(3), default='100', nullable=False)
    # DB의 현재 시간 사용
    created_at = Column(DateTime, default=func.now())
    # 업데이트 시 자동 반영
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True, comment='회원 삭제일 (삭제되지 않은 경우 NULL)')
