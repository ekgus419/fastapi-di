from src.repository.user.user_repository import UserRepository
from src.utils.security import verify_password  # 평문 vs 해시 비교 함수
from src.utils.jwt_token_provider import JwtTokenProvider  # 토큰 생성/검증 유틸리티
from src.exception.auth_exceptions import UnauthorizedException
from src.exception.user_exceptions import UserNotFoundException
from src.service.base_service import BaseService
from src.core.transaction import Transactional  # 트랜잭션 데코레이터 추가
from typing import Dict


class AuthService(BaseService):
    """
    사용자 인증 및 JWT 토큰 관리를 담당하는 서비스 클래스.
    로그인, 토큰 재발급, 로그아웃 기능을 제공함.
    """

    def __init__(self, user_repository: UserRepository):
        """
        AuthService의 생성자.
        :param user_repository: 사용자 데이터를 관리하는 UserRepository 인스턴스
        """
        self.user_repository = user_repository

    @Transactional
    def login(self, username: str, password: str, db=None) -> Dict[str, str]:
        """
        사용자 로그인 처리 및 JWT Access Token / Refresh Token 발급.
        :param username: 사용자명
        :param password: 입력된 비밀번호 (평문)
        :param db: 트랜잭션 세션
        :return: {"access_token": str, "refresh_token": str}
        :raises UserNotFoundException: 사용자가 존재하지 않을 경우
        :raises HTTPUnauthorizedException: 비밀번호가 일치하지 않을 경우
        """
        user_domain = self.user_repository.get_user_by_username(username, db=db)

        if not user_domain:
            raise UserNotFoundException()

        # password 검증
        if not user_domain.password or not verify_password(password, user_domain.password):
            raise UnauthorizedException(detail="Invalid credentials")

        access_token = JwtTokenProvider.generate_access_token(user_domain.username)
        refresh_token = JwtTokenProvider.generate_refresh_token(user_domain.username)

        self.user_repository.update_refresh_token(user_domain.seq, refresh_token, db=db)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_access_token(self, refresh_token: str, db=None) -> str:
        """
        Refresh Token을 사용하여 새로운 Access Token을 발급하는 메서드.
        :param refresh_token: 클라이언트가 제공한 Refresh Token
        :param db: 트랜잭션 세션
        :return: 새로 발급된 Access Token (str)
        :raises UnauthorizedException: Refresh Token이 유효하지 않을 경우
        :raises UserNotFoundException: 해당 사용자 정보를 찾을 수 없을 경우
        """

        # 토큰 검증 및 사용자 이름 추출
        payload = JwtTokenProvider.validate_token(refresh_token)
        username = payload.get("sub")
        if not username:
            raise UnauthorizedException(detail="Invalid refresh token: subject missing")

        # Entity 변환 없이 Domain 반환
        user_domain = self.user_repository.get_user_by_username(username, db=db)
        if not user_domain:
            raise UserNotFoundException()

        # 저장된 refresh token과 비교
        if user_domain.current_refresh_token != refresh_token:
            raise UnauthorizedException(detail="Refresh token is invalid or has been logged out")

        # 새로운 Access Token 생성
        new_access_token = JwtTokenProvider.generate_access_token(user_domain.username)
        return new_access_token

    @Transactional
    def logout(self, username: str, refresh_token: str, db=None):
        """
        사용자 로그아웃 처리 (Refresh Token 무효화).
        :param username: 로그아웃할 사용자명
        :param refresh_token: 현재 사용 중인 Refresh Token
        :param db: 트랜잭션 세션
        :raises UserNotFoundException: 사용자가 존재하지 않을 경우
        :raises HTTPUnauthorizedException: Refresh Token이 저장된 것과 다를 경우
        """

        # 로그아웃 시, 사용자 테이블의 refresh token 값을 삭제하여 블랙리스트 효과
        # Entity 변환 없이 Domain 반환
        user_domain = self.user_repository.get_user_by_username(username, db=db)

        if not user_domain:
            raise UserNotFoundException()

        # 저장된 refresh token과 비교하여 일치하는 경우에만 삭제
        if user_domain.current_refresh_token != refresh_token:
            raise UnauthorizedException(detail="Refresh token mismatch")

        self.user_repository.update_refresh_token(user_domain.seq, None, db=db)
