from fastapi import APIRouter, HTTPException, Depends, Query, status
from dependency_injector.wiring import inject, Provide

from src.core.container import Container
from src.dto.response.paginated_response import PaginatedResponse
from src.service.user.user_service import UserService
from src.dto.request.user.user_create_request import UserCreateRequest
from src.dto.request.user.password_update_request import PasswordUpdateRequest
from src.dto.response.user.user_response import UserResponse
from src.dto.response.common_response import CommonResponse

# 사용자 관리 관련 API 엔드포인트를 정의하는 APIRouter
router = APIRouter(
    prefix="/users",
    # dependencies=[Depends(get_current_username)]  # 인증이 필요할 경우 활성화 가능
)

@router.get("/users/paged")
@inject
def get_users_paged(
    page: int = Query(1, ge=1, description="현재 페이지 (1-based)"),
    size: int = Query(10, ge=1, description="페이지 크기"),
    sort_by: str | None = Query(None, description="정렬 기준 컬럼명 (예: 'id', 'username')"),
    order: str = Query("asc", regex="^(asc|desc)$", description="정렬 순서 (asc 또는 desc)"),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    페이징 및 정렬 기능을 지원하는 사용자 목록 조회 엔드포인트.
    :param page: 현재 페이지 (1부터 시작)
    :param size: 페이지 크기 (한 페이지당 사용자 수)
    :param sort_by: 정렬 기준 컬럼 (예: 'id', 'username')
    :param order: 정렬 방향 ("asc" | "desc")
    :param user_service: UserService 의존성 주입
    :return: 사용자 목록과 페이지네이션 정보
    """
    entities, total_items = user_service.get_users_with_paging(page, size, sort_by, order)

    # UserEntity -> UserResponse 변환
    user_responses = [UserResponse.model_validate(e) for e in entities]

    # 전체 페이지 수 계산
    total_pages = (total_items + size - 1)

    return CommonResponse(
        status="success",
        data=PaginatedResponse(
            items=user_responses,
            total=total_items,
            page=page,
            size=size,
            total_pages=total_pages
        ),
        message=None
    )

@router.get("/{user_id}", response_model=CommonResponse[UserResponse])
@inject
def get_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    특정 사용자 ID를 기반으로 사용자 정보를 조회하는 엔드포인트.
    :param user_id: 조회할 사용자 ID
    :param user_service: UserService 의존성 주입
    :return: CommonResponse[UserResponse] (사용자 정보)
    :raises HTTPException: 사용자가 존재하지 않을 경우 404 오류 반환
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return CommonResponse(status="success", data=user, message=None)

@router.post("/", response_model=CommonResponse[UserResponse], status_code=status.HTTP_201_CREATED)
@inject
def create_user(
    request: UserCreateRequest,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    새 사용자를 생성하는 엔드포인트.
    :param request: UserCreateRequest (username, email, full_name, password 포함)
    :param user_service: UserService 의존성 주입
    :return: CommonResponse[UserResponse] (생성된 사용자 정보)
    """
    user = user_service.create_user(
        username=request.username,
        email=request.email,
        full_name=request.full_name,
        password=request.password
    )
    return CommonResponse(status="success", data=user, message=None)

@router.patch("/{user_id}/password", response_model=CommonResponse[None], status_code=status.HTTP_200_OK)
@inject
def update_password(
    user_id: int,
    request: PasswordUpdateRequest,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    특정 사용자의 비밀번호를 변경하는 엔드포인트.
    :param user_id: 비밀번호를 변경할 사용자 ID
    :param request: PasswordUpdateRequest (새 비밀번호 포함)
    :param user_service: UserService 의존성 주입
    :return: CommonResponse[None] (비밀번호 변경 성공 메시지)
    """
    user_service.update_password(user_id, request.password)
    return CommonResponse(status="success", data=None, message="Password updated successfully")

@router.delete("/{user_id}", response_model=CommonResponse[None], status_code=status.HTTP_200_OK)
@inject
def delete_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    특정 사용자를 삭제하는 엔드포인트.
    :param user_id: 삭제할 사용자 ID
    :param user_service: UserService 의존성 주입
    :return: CommonResponse[None] (삭제 성공 메시지)
    """
    user_service.delete_user(user_id)
    return CommonResponse(status="success", data=None, message="User deleted successfully")
