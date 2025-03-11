import jwt
from datetime import timedelta
from src.core.settings import settings
from src.exception.token_exceptions import (
    TokenExpiredException, InvalidTokenException, InvalidTokenSubjectMissingException
)
from src.utils.time_provider import TimeProvider  # ✅ TimeProvider 호출

class JwtTokenProvider:
    """
    JwtTokenProvider는 JWT 생성, 검증, 사용자 정보 추출 등을 담당
    """

    @staticmethod
    def generate_access_token(username: str) -> str:
        now_utc = TimeProvider.get_utc_now()
        expire = now_utc + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

        payload = {
            "sub": username,
            "iat": TimeProvider.to_timestamp(now_utc),
            "exp": TimeProvider.to_timestamp(expire),
            "scope": "access"
        }

        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def generate_refresh_token(username: str) -> str:
        now_utc = TimeProvider.get_utc_now()
        expire = now_utc + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION_MINUTES)

        payload = {
            "sub": username,
            "iat": TimeProvider.to_timestamp(now_utc),
            "exp": TimeProvider.to_timestamp(expire),
            "scope": "refresh"
        }

        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def validate_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            # 토큰 만료 예외 처리
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            # 일반적인 JWT 오류 처리
            raise InvalidTokenException()

    @staticmethod
    def get_username_from_token(token: str) -> str:
        payload = JwtTokenProvider.validate_token(token)
        username = payload.get("sub")
        if not username:
            raise InvalidTokenSubjectMissingException()
        return username
