from typing import Tuple, List

from pydantic import EmailStr

from src.exception.user_exceptions import UserNotFoundException, UserAlreadyExistsException
from src.repository.user.user_repository import UserRepository
from src.mapper.user_mapper import entity_to_domain, domain_to_entity
from src.utils.security import hash_password
from src.domain.user_domain import UserDomain


class UserService:
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
        :param sort_by: 정렬할 컬럼명 (예: "id", "username")
        :param order: 정렬 방식 ("asc" | "desc")
        :return: (조회된 사용자 리스트, 전체 사용자 수)
        """
        user_entity = self.user_repository.get_all_users(page, size, sort_by, order)
        total_count = self.user_repository.count_users()
        user_domain = [entity_to_domain(m) for m in user_entity]
        return user_domain, total_count

    def get_user_by_id(self, user_id: int) -> UserDomain:
        """
        특정 사용자 ID를 기반으로 사용자 정보를 조회하는 메서드.
        :param user_id: 조회할 사용자 ID
        :return: UserEntity 객체
        :raises UserNotFoundException: 사용자가 존재하지 않는 경우 예외 발생
        """
        model = self.user_repository.get_user_by_id(user_id)
        if model is None:
            raise UserNotFoundException()
        return entity_to_domain(model)

    def create_user(self, username: str, email: EmailStr, full_name: str | None, password: str) -> UserDomain:
        """
        새로운 사용자를 생성하는 메서드.
        :param username: 사용자명
        :param email: 이메일 주소
        :param full_name: 전체 이름 (선택 사항)
        :param password: 비밀번호 (평문)
        :return: 생성된 사용자 정보 (UserEntity)
        :raises UserAlreadyExistsException: 동일한 username이 이미 존재하는 경우 예외 발생
        """

        # 유저가 이미 존재하는지 확인
        existing_user = self.user_repository.get_user_by_username(username)
        if existing_user:
            raise UserAlreadyExistsException()

        hashed = hash_password(password)

        # 도메인 생성
        user_domain = UserDomain(
            id=0,  # ID는 DB에서 자동 할당
            username=username,
            email=email,
            full_name=full_name
        )

        # 도메인 객체를 ORM Entity 로 변환
        new_entity = domain_to_entity(user_domain, hashed)
        created_entity = self.user_repository.create_user(new_entity)

        # Entity 를 도메인 객체로 변환하여 반환
        return entity_to_domain(created_entity)

    def update_password(self, user_id: int, new_password: str) -> bool:
        """
        사용자의 비밀번호를 변경하는 메서드.
        :param user_id: 비밀번호를 변경할 사용자 ID
        :param new_password: 변경할 새 비밀번호 (평문)
        :return: 비밀번호 변경 성공 여부 (True/False)
        :raises UserNotFoundException: 해당 사용자가 존재하지 않는 경우 예외 발생
        """
        hashed = hash_password(new_password)
        result = self.user_repository.update_password(user_id, hashed)
        if not result:
            raise UserNotFoundException()
        return True

    def delete_user(self, user_id: int) -> bool:
        """
        특정 사용자를 삭제하는 메서드.
        :param user_id: 삭제할 사용자 ID
        :return: 삭제 성공 여부 (True/False)
        :raises UserNotFoundException: 해당 사용자가 존재하지 않는 경우 예외 발생
        """
        result = self.user_repository.delete_user(user_id)
        if not result:
            raise UserNotFoundException()
        return True