from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.dto.request.auth.login_request_dto import LoginRequestDto
from src.dto.request.auth.refresh_token_request_dto import RefreshTokenRequestDto
from src.dto.request.auth.logout_request_dto import LogoutRequestDto
from src.dto.response.auth.token_response_dto import TokenResponseDto
from src.dto.response.common_response_dto import CommonResponseDto
from src.service.auth.auth_service import AuthService
from src.core.container import Container

# 인증 관련 엔드포인트를 정의하는 APIRouter
router = APIRouter()


@router.post("/tokens", response_model=CommonResponseDto[TokenResponseDto], status_code=status.HTTP_200_OK)
@inject
def issue_tokens(
    payload: LoginRequestDto,
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    # 🔑 로그인 API (Access & Refresh Token 발급)

    사용자의 인증 정보를 확인하고, **Access Token 및 Refresh Token**을 발급합니다.

    ## 📝 Args:
    - **`payload`** (`LoginRequestDto`):
      - 로그인 요청 데이터
      - **포함 필드:** `username`, `password`
    - **`auth_service`** (`AuthService`):
      - 인증 서비스 **의존성 주입**

    ## 📤 Returns:
    - **`CommonResponseDto[TokenResponseDto]`**
      - **발급된 Access Token 및 Refresh Token 반환**
    """
    tokens = auth_service.login(payload.username, payload.password)
    return CommonResponseDto(
        status="success",
        data=TokenResponseDto(access_token=tokens["access_token"], refresh_token=tokens["refresh_token"]),
        message=None
    )


@router.put("/tokens", response_model=CommonResponseDto[TokenResponseDto], status_code=status.HTTP_200_OK)
@inject
def refresh_access_token(
    payload: RefreshTokenRequestDto,
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    # 🔄 Refresh Token을 사용한 새로운 Access Token 발급 API

    유효한 **Refresh Token**을 제공하면 새로운 **Access Token**을 생성합니다.

    ## 📝 Args:
    - **`payload`** (`RefreshTokenRequestDto`):
      - **Refresh Token 요청 데이터**
    - **`auth_service`** (`AuthService`):
      - 인증 서비스 **의존성 주입**

    ## 📤 Returns:
    - **`CommonResponseDto[TokenResponseDto]`**
      - **새로운 Access Token 및 기존 Refresh Token 반환**
    """
    new_access_token = auth_service.refresh_access_token(payload.refresh_token)
    return CommonResponseDto(
        status="success",
        data=TokenResponseDto(access_token=new_access_token, refresh_token=payload.refresh_token),
        message="Token refreshed successfully"
    )


@router.patch("/tokens", response_model=CommonResponseDto[None], status_code=status.HTTP_200_OK)
@inject
def revoke_tokens(
    payload: LogoutRequestDto,
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    # 🚪 로그아웃 API (Refresh Token 폐기)

    사용자의 **Refresh Token**을 삭제하여 인증을 **무효화**합니다.

    ## 📝 Args:
    - **`payload`** (`LogoutRequestDto`):
      - 로그아웃 요청 데이터
      - **포함 필드:** `username`, `refresh_token`
    - **`auth_service`** (`AuthService`):
      - 인증 서비스 **의존성 주입**

    ## 📤 Returns:
    - **`CommonResponseDto[None]`**
      - **로그아웃 성공 메시지 반환**
    """
    auth_service.logout(payload.username, payload.refresh_token)
    return CommonResponseDto(
        status="success",
        data=None,
        message="Logged out successfully"
    )
