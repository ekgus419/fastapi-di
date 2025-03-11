from typing import Optional, List
from sqlalchemy.orm import Session
from src.entity.user_entity import UserEntity
from src.repository.base_repository import BaseRepository
from src.mapper.user_mapper import entity_to_domain, domain_to_entity
from src.domain.user_domain import UserDomain

class UserRepository(BaseRepository[UserEntity]):
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
        super().__init__(db, UserEntity)

    def get_all_users(
        self,
        page: int = 1,
        size: int = 10,
        sort_by: str = None,
        order: str = "asc",
        db: Session = None
    ) -> List[UserDomain]:
        """
        페이징 및 정렬을 적용하여 모든 사용자를 조회하는 메서드.
        :param page: 1-based 페이지 번호
        :param size: 한 페이지에 가져올 데이터 개수
        :param sort_by: 정렬할 컬럼명 (예: "seq", "username")
        :param order: 정렬 방식 ("asc" | "desc")
        :param db: (선택) 트랜잭션 세션
        :return: 조회된 사용자 목록 (UserDomain 객체 리스트)
        """
        db = db or self.db  # 🔥 주입된 db 세션이 있으면 사용, 없으면 기본 세션 사용
        user_entities = self.find_all(page=page, size=size, sort_by=sort_by, order=order)
        return [entity_to_domain(user) for user in user_entities]

    def count_users(self, db: Session = None) -> int:
        """
        전체 사용자 수를 반환하는 메서드.
        :param db: (선택) 트랜잭션 세션
        :return: 사용자 총 개수
        """
        db = db or self.db
        return self.count_all()

    def get_user_by_seq(self, user_seq: int, db: Session = None) -> Optional[UserDomain]:
        """
        사용자 seq를 기반으로 단일 사용자 조회.
        :param user_seq: 조회할 사용자 seq
        :param db: (선택) 트랜잭션 세션
        :return: UserDomain 객체 (없으면 None)
        """
        db = db or self.db
        entity = self.find_by_id(user_seq)
        return entity_to_domain(entity) if entity else None

    def get_user_by_username(self, username: str, db: Session = None) -> Optional[UserDomain]:
        """
        사용자명을 기반으로 사용자 조회. (커스텀 메서드)
        :param username: 조회할 사용자명
        :param db: (선택) 트랜잭션 세션
        :return: UserDomain 객체 (없으면 None)
        """
        db = db or self.db
        entity = db.query(self.entity).filter(self.entity.username == username).first()

        if entity:
            entity = db.merge(entity)
            db.refresh(entity)

        return entity_to_domain(entity) if entity else None

    def create_user(self, user_domain: UserDomain, hashed_password: str, db: Session = None) -> UserDomain:
        """
        새로운 사용자를 생성하는 메서드.
        :param user_domain: 저장할 UserDomain 객체
        :param hashed_password: 해싱된 비밀번호
        :param db: (선택) 트랜잭션 세션
        :return: 저장된 UserDomain 객체
        """
        db = db or self.db
        entity = domain_to_entity(user_domain, hashed_password)
        saved_entity = self.save(entity, db=db)
        return entity_to_domain(saved_entity)

    def update_password(self, user_seq: int, hashed_password: str, db: Session = None) -> bool:
        """
        특정 사용자의 비밀번호를 업데이트하는 메서드.
        :param user_seq: 비밀번호를 변경할 사용자 seq
        :param hashed_password: 해싱된 새 비밀번호
        :param db: (선택) 트랜잭션 세션
        :return: 업데이트 성공 여부 (True/False)
        """
        db = db or self.db
        updated = self.update(user_seq, password=hashed_password, db=db)
        return updated is not None

    def delete_user(self, user_seq: int, db: Session = None) -> bool:
        """
        특정 seq의 사용자를 삭제하는 메서드.
        :param user_seq: 삭제할 사용자 seq
        :param db: (선택) 트랜잭션 세션
        :return: 삭제 성공 여부 (True/False)
        """
        db = db or self.db
        return self.delete_by_id(user_seq, db=db)

    def soft_delete_user(self, user_seq: int, db: Session = None) -> bool:
        """
        특정 seq의 사용자를 논리 삭제하는 메서드.
        실제 데이터는 삭제하지 않고, delete_at 필드를 업데이트함.
        :param user_seq: 삭제할 사용자 seq
        :param db: (선택) 트랜잭션 세션
        :return: 삭제 성공 여부 (True/False)
        """
        db = db or self.db
        return self.soft_delete_by_id(user_seq, db=db)

    def update_refresh_token(self, user_seq: int, refresh_token: Optional[str], db: Session = None) -> bool:
        """
        사용자의 Refresh Token을 업데이트하는 메서드.
        (로그아웃 시에는 None으로 설정하여 토큰 무효화)
        :param user_seq: 업데이트할 사용자 seq
        :param refresh_token: 저장할 Refresh Token (None이면 로그아웃 처리)
        :param db: (선택) 트랜잭션 세션
        :return: 업데이트 성공 여부 (True/False)
        """
        db = db or self.db
        user = self.find_by_id(user_seq)
        if not user:
            return False
        updated = self.update(user_seq, current_refresh_token=refresh_token, db=db)
        return updated is not None
