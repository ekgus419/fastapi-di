from sqlalchemy import Column, Integer, String, DateTime
from src.entity.base_entity import Base
from src.utils.time_provider import get_kst_time


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    password = Column(String(128), nullable=False)
    # Refresh Token 저장 컬럼: 로그아웃 시 값을 지워서 해당 토큰을 무효화
    current_refresh_token = Column(String(512), nullable=True)
    type = Column(String(3), default='100', nullable=False, comment='회원 유형 (예: 100: employee, 200: agency)')
    status = Column(String(3), default='100', nullable=False, comment='회원 상태 (예: 100: active, 200: inactive)')
    created_at = Column(DateTime, default=get_kst_time(), comment='회원 등록일')
    updated_at = Column(DateTime, default=get_kst_time(), onupdate=get_kst_time(),comment='회원 수정일')
    deleted_at = Column(DateTime, nullable=True, comment='회원 삭제일 (삭제되지 않은 경우 NULL)')
