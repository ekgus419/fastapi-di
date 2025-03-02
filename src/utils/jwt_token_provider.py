import jwt
from datetime import datetime, timedelta
from src.core.settings import settings
from fastapi import HTTPException, status

class JwtTokenProvider:
    """
    JwtTokenProvider는 JWT 생성, 검증, 사용자 정보 추출 등을 담당
    """
    @staticmethod
    def generate_access_token(username: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
        payload = {"sub": username, "exp": expire, "scope": "access"}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return token

    @staticmethod
    def generate_refresh_token(username: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION_MINUTES)
        payload = {"sub": username, "exp": expire, "scope": "refresh"}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return token

    @staticmethod
    def validate_token(token: str) -> dict:
        try:
            # jwt.decode가 만료되면 jwt.ExpiredSignatureError 발생
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            # token이 만료된 경우
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.PyJWTError:
            # 기타 JWT 관련 오류 발생시도 동일하게 처리
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    @staticmethod
    def get_username_from_token(token: str) -> str:
        payload = JwtTokenProvider.validate_token(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: subject missing")
        return username
