from typing import Optional, List
from sqlalchemy.orm import Session
from src.model.user_model import UserModel
from src.repository.base_repository import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    """
    사용자(User) 엔티티의 데이터 접근을 담당하는 리포지토리 클래스.
    공통적인 CRUD 기능은 BaseRepository에서 상속받고,
    사용자 관련 추가 기능을 여기에 정의함.
    """

    def __init__(self, db: Session):
        """
        UserRepository의 생성자.
        :param db: SQLAlchemy 세션 객체
        """
        super().__init__(db, UserModel)

    def get_all_users(
        self,
        page: int = 1,
        size: int = 10,
        sort_by: str = None,
        order: str = "asc"
    ) -> List[UserModel]:
        """
        페이징 및 정렬을 적용하여 모든 사용자를 조회하는 메서드.
        :param page: 1-based 페이지 번호
        :param size: 한 페이지에 가져올 데이터 개수
        :param sort_by: 정렬할 컬럼명 (예: "id", "username")
        :param order: 정렬 방식 ("asc" | "desc")
        :return: 조회된 사용자 목록
        """
        return self.find_all(page=page, size=size, sort_by=sort_by, order=order)

    def count_users(self) -> int:
        """
        전체 사용자 수를 반환하는 메서드.
        :return: 사용자 총 개수
        """
        return self.count_all()

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        사용자 ID를 기반으로 단일 사용자 조회.
        :param user_id: 조회할 사용자 ID
        :return: UserModel 객체 (없으면 None)
        """
        return self.find_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """
        사용자명을 기반으로 사용자 조회. (커스텀 메서드)
        :param username: 조회할 사용자명
        :return: UserModel 객체 (없으면 None)
        """
        return self.db.query(self.model).filter(self.model.username == username).first()

    def create_user(self, user_model: UserModel) -> UserModel:
        """
        새로운 사용자를 생성하는 메서드.
        :param user_model: 저장할 UserModel 객체
        :return: 저장된 UserModel 객체
        """
        return self.save(user_model)

    def update_password(self, user_id: int, hashed_password: str) -> bool:
        """
        특정 사용자의 비밀번호를 업데이트하는 메서드.
        :param user_id: 비밀번호를 변경할 사용자 ID
        :param hashed_password: 해싱된 새 비밀번호
        :return: 업데이트 성공 여부 (True/False)
        """
        updated = self.update(user_id, password=hashed_password)
        return updated is not None

    def delete_user(self, user_id: int) -> bool:
        """
        특정 ID의 사용자를 삭제하는 메서드.
        :param user_id: 삭제할 사용자 ID
        :return: 삭제 성공 여부 (True/False)
        """
        return self.delete_by_id(user_id)

    def update_refresh_token(self, user_id: int, refresh_token: Optional[str]) -> bool:
        """
        사용자의 Refresh Token을 업데이트하는 메서드.
        (로그아웃 시에는 None으로 설정하여 토큰 무효화)
        :param user_id: 업데이트할 사용자 ID
        :param refresh_token: 저장할 Refresh Token (None이면 로그아웃 처리)
        :return: 업데이트 성공 여부 (True/False)
        """
        user = self.find_by_id(user_id)
        if not user:
            return False
        user.current_refresh_token = refresh_token
        self.db.commit()
        self.db.refresh(user)
        return True