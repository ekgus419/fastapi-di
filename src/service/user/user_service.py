from typing import Tuple, List
from src.dto.request.user.user_create_request_dto import UserCreateRequestDto
from src.exception.user_exceptions import UserNotFoundException, UserAlreadyExistsException
from src.repository.user.user_repository import UserRepository
from src.service.base_service import BaseService
from src.utils.security import hash_password
from src.domain.user_domain import UserDomain
from src.core.transaction import Transactional  # 트랜잭션 데코레이터 추가


class UserService(BaseService):
    """
    사용자 관련 비즈니스 로직을 처리하는 서비스 클래스.
    데이터 접근 로직은 UserRepository를 통해 수행하며,
    도메인 로직을 적용하여 사용자 관리 기능을 제공함.
    """

    def __init__(self, user_repository: UserRepository):
        """
        UserService의 생성자.
        :param user_repository: 사용자 데이터 접근을 위한 UserRepository 인스턴스
        """
        self.user_repository = user_repository

    def get_users_with_paging(
        self,
        page: int,
        size: int,
        sort_by: str | None,
        order: str
    ) -> Tuple[List[UserDomain], int]:
        """
        페이징 및 정렬을 적용하여 사용자 목록을 조회하는 메서드.
        :param page: 1-based 페이지 번호
        :param size: 한 페이지에 가져올 데이터 개수
        :param sort_by: 정렬할 컬럼명 (예: "seq", "username")
        :param order: 정렬 방식 ("asc" | "desc")
        :return: (조회된 사용자 리스트, 전체 사용자 수)
        """
        user_domains = self.user_repository.get_all_users(page, size, sort_by, order)
        total_count = self.user_repository.count_users()
        return user_domains, total_count

    def get_user_by_seq(self, user_seq: int) -> UserDomain:
        """
        특정 사용자 seq를 기반으로 사용자 정보를 조회하는 메서드.
        :param user_seq: 조회할 사용자 seq
        :return: UserDomain 객체
        :raises UserNotFoundException: 사용자가 존재하지 않는 경우 예외 발생
        """
        user_domain = self.user_repository.get_user_by_seq(user_seq)
        if user_domain is None:
            raise UserNotFoundException()
        return user_domain

    @Transactional
    def create_user(self, user_create_request: UserCreateRequestDto, db=None) -> UserDomain:
        """
        새로운 사용자를 생성하는 메서드.
        :param user_create_request: user (username, email, password)
        :param db: 트랜잭션 세션
        :return: 생성된 사용자 정보 (UserDomain)
        :raises UserAlreadyExistsException: 동일한 username이 이미 존재하는 경우 예외 발생
        """

        # 유저가 이미 존재하는지 확인
        existing_user = self.user_repository.get_user_by_username(user_create_request.username, db=db)
        if existing_user:
            raise UserAlreadyExistsException()

        hashed_password = hash_password(user_create_request.password)
        user_create_request.type = user_create_request.type or 100
        user_create_request.status = user_create_request.status or 100

        user_domain = UserDomain(
            seq=0,
            username=user_create_request.username,
            email=user_create_request.email,
            type=user_create_request.type,
            status=user_create_request.status,
            current_refresh_token=None,
        )

        # Repository에서 저장 후 Domain 반환
        return self.user_repository.create_user(user_domain, hashed_password, db=db)

    @Transactional
    def update_password(self, user_seq: int, new_password: str, db=None) -> bool:
        """
        사용자의 비밀번호를 변경하는 메서드.
        :param user_seq: 비밀번호를 변경할 사용자 seq
        :param new_password: 변경할 새 비밀번호 (평문)
        :param db: 트랜잭션 세션
        :return: 비밀번호 변경 성공 여부 (True/False)
        :raises UserNotFoundException: 해당 사용자가 존재하지 않는 경우 예외 발생
        """
        hashed_password = hash_password(new_password)
        result = self.user_repository.update_password(user_seq, hashed_password, db=db)
        if not result:
            raise UserNotFoundException()
        return True

    @Transactional
    def delete_user(self, user_seq: int, db=None) -> bool:
        """
        특정 사용자를 삭제하는 메서드.
        :param user_seq: 삭제할 사용자 seq
        :param db: 트랜잭션 세션
        :return: 삭제 성공 여부 (True/False)
        :raises UserNotFoundException: 해당 사용자가 존재하지 않는 경우 예외 발생
        """
        result = self.user_repository.delete_user(user_seq, db=db)
        if not result:
            raise UserNotFoundException()
        return True

    @Transactional
    def soft_delete_user(self, user_seq: int, db=None) -> bool:
        """
        특정 사용자 삭제시 delete_at 에 값 추가하는 메서드.
        :param user_seq: 삭제할 사용자 seq
        :param db: 트랜잭션 세션
        :return: 삭제 성공 여부 (True/False)
        :raises UserNotFoundException: 해당 사용자가 존재하지 않는 경우 예외 발생
        """
        result = self.user_repository.soft_delete_user(user_seq, db=db)
        if not result:
            raise UserNotFoundException()
        return True