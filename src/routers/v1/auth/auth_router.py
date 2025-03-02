from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.dto.request.auth.login_request import LoginRequest
from src.dto.request.auth.logout_request import LogoutRequest
from src.dto.request.auth.refresh_token_request import RefreshTokenRequest
from src.dto.response.auth.token_response import TokenResponse
from src.dto.response.common_response import CommonResponse
from src.service.auth.auth_service import AuthService
from src.core.container import Container

# 인증 관련 엔드포인트를 정의하는 APIRouter
router = APIRouter(prefix="/auth")


@router.post("/login", response_model=CommonResponse[TokenResponse], status_code=status.HTTP_200_OK)
@inject
def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    사용자 로그인 엔드포인트.
    - 사용자 인증을 수행하고, Access Token 및 Refresh Token을 발급함.

    :param payload: LoginRequest (username, password 포함)
    :param auth_service: AuthService 의존성 주입
    :return: CommonResponse[TokenResponse] (Access Token 및 Refresh Token 반환)
    """
    tokens = auth_service.login(payload.username, payload.password)
    return CommonResponse(
        status="success",
        data=TokenResponse(access_token=tokens["access_token"], refresh_token=tokens["refresh_token"]),
        message=None
    )


@router.post("/refresh", response_model=CommonResponse[TokenResponse], status_code=status.HTTP_200_OK)
@inject
def refresh_token(
    payload: RefreshTokenRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    Refresh Token을 사용하여 새로운 Access Token을 발급하는 엔드포인트.

    :param payload: RefreshTokenRequest (refresh_token 포함)
    :param auth_service: AuthService 의존성 주입
    :return: CommonResponse[TokenResponse] (새로운 Access Token과 기존 Refresh Token 반환)
    """
    # Refresh Token 검증 및 새로운 Access Token 생성
    new_access_token = auth_service.refresh_access_token(payload.refresh_token)
    tokens = {"access_token": new_access_token, "refresh_token": payload.refresh_token}

    return CommonResponse(
        status="success",
        data=TokenResponse(access_token=tokens["access_token"], refresh_token=tokens["refresh_token"]),
        message="Token refreshed successfully"
    )


@router.post("/logout", response_model=CommonResponse[None], status_code=status.HTTP_200_OK)
@inject
def logout(
    payload: LogoutRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    사용자 로그아웃 엔드포인트.
    - 로그아웃 시, 저장된 Refresh Token을 삭제하여 세션을 무효화함.

    :param payload: LogoutRequest (username, refresh_token 포함)
    :param auth_service: AuthService 의존성 주입
    :return: CommonResponse[None] (로그아웃 성공 메시지 반환)
    """
    # 로그아웃 시, 클라이언트는 username과 refresh token을 전달해야 함
    auth_service.logout(payload.username, payload.refresh_token)

    return CommonResponse(
        status="success",
        data=None,
        message="Logged out successfully"
    )
