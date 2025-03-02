from typing import Type, TypeVar, Generic, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text, desc, asc

# 제네릭 타입 변수 T (SQLAlchemy ORM 모델 타입)
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    공통적인 데이터 접근 로직을 제공하는 추상 클래스.
    모든 엔티티 리포지토리는 이 클래스를 상속받아 공통 기능을 재사용함.
    """

    def __init__(self, db: Session, model: Type[T]):
        """
        :param db: SQLAlchemy 세션
        :param model: ORM 모델 클래스
        """
        self.db = db
        self.model = model

    def find_all(
            self,
            page: int = 1,
            size: int = 10,
            sort_by: Optional[str] = None,
            order: str = "asc"
    ) -> List[T]:
        """
        페이징 및 정렬을 지원하는 목록 조회 메서드.
        :param page: 페이지 번호 (1-based index)
        :param size: 한 페이지에 가져올 데이터 개수
        :param sort_by: 정렬할 컬럼명
        :param order: "asc" (오름차순) 또는 "desc" (내림차순)
        :return: 조회된 엔티티 목록
        """
        query = self.db.query(self.model)

        # 정렬 적용
        if sort_by:
            sort_attr = getattr(self.model, sort_by, None)
            if sort_attr is not None:
                query = query.order_by(desc(sort_attr)) if order.lower() == "desc" else query.order_by(asc(sort_attr))

        # 페이징 적용
        skip = (page - 1) * size
        return query.offset(skip).limit(size).all()

    def find_by_id(self, id: int) -> Optional[T]:
        """
        ID를 기반으로 엔티티를 조회하는 메서드.
        :param id: 조회할 엔티티의 ID
        :return: 해당 ID의 엔티티 (없으면 None)
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def count_all(self) -> int:
        """
        전체 엔티티 개수를 반환하는 메서드.
        :return: 엔티티 개수
        """
        return self.db.query(self.model).count()

    def save(self, entity: T) -> T:
        """
        엔티티를 데이터베이스에 저장하는 메서드.
        :param entity: 저장할 엔티티 객체
        :return: 저장된 엔티티
        """
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, id: int, **kwargs) -> Optional[T]:
        """
        특정 ID의 엔티티를 업데이트하는 메서드.
        :param id: 업데이트할 엔티티의 ID
        :param kwargs: 변경할 필드 값들
        :return: 업데이트된 엔티티 (없으면 None)
        """
        entity = self.find_by_id(id)
        if not entity:
            return None
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_by_id(self, id: int) -> bool:
        """
        특정 ID의 엔티티를 삭제하는 메서드.
        :param id: 삭제할 엔티티의 ID
        :return: 삭제 성공 여부
        """
        entity = self.find_by_id(id)
        if not entity:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True

    def exists_by_id(self, id: int) -> bool:
        """
        특정 ID의 엔티티 존재 여부를 확인하는 메서드.
        :param id: 확인할 ID
        :return: 존재 여부 (True/False)
        """
        return self.find_by_id(id) is not None

    def find_by_native_query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        네이티브 SQL 쿼리를 실행하는 메서드.
        :param sql: 실행할 SQL 문자열
        :param params: 바인딩할 파라미터
        :return: 쿼리 결과 리스트
        """
        result = self.db.execute(text(sql), params or {})
        return result.fetchall()
