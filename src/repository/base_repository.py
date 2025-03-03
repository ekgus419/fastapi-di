from typing import Type, TypeVar, Generic, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text, desc, asc, inspect, delete, exists
from sqlalchemy.sql.expression import ColumnElement
from src.entity.base_entity import Base  # SQLAlchemy Base 클래스

# T가 항상 SQLAlchemy의 Base를 상속하는 모델이 되도록 제한
T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    """
    공통적인 데이터 접근 로직을 제공하는 추상 클래스.
    모든 엔티티 리포지토리는 이 클래스를 상속받아 공통 기능을 재사용함.
    """

    def __init__(self, db: Session, entity: Type[T]):
        """
        :param db: SQLAlchemy 세션
        :param entity: ORM 모델 클래스 (Base를 상속해야 함)
        """
        self.db = db
        self.entity = entity

        # 기본 키가 존재하는지 체크
        primary_keys = inspect(self.entity).primary_key
        if not primary_keys:
            raise ValueError(f"{self.entity.__name__} 모델에 기본 키가 없습니다.")

        # 기본 키 컬럼을 SQLAlchemy InstrumentedAttribute로 변환
        # 기본 키의 이름 가져오기
        primary_key_name = primary_keys[0].name
        # SQLAlchemy 컬럼 객체로 변환
        self.primary_key: ColumnElement = getattr(self.entity, primary_key_name)

    def find_all(
        self,
        page: int = 1,
        size: int = 10,
        sort_by: Optional[str] = None,
        order: str = "asc"
    ) -> List[T]:
        """
        페이징 및 정렬을 지원하는 목록 조회 메서드.
        """
        query = self.db.query(self.entity)

        # 정렬 컬럼 유효성 체크
        if sort_by:
            entity_columns = {column.name for column in inspect(self.entity).c}
            if sort_by not in entity_columns:
                raise ValueError(f"정렬할 컬럼 '{sort_by}'가 존재하지 않습니다. 사용 가능한 컬럼: {entity_columns}")

            sort_attr = getattr(self.entity, sort_by)
            query = query.order_by(desc(sort_attr) if order.lower() == "desc" else asc(sort_attr))

        return query.offset((page - 1) * size).limit(size).all()

    def find_by_id(self, entity_id: int) -> Optional[T]:
        """
        ID를 기반으로 엔티티를 조회하는 메서드.
        """
        return self.db.query(self.entity).filter(self.primary_key == entity_id).first()

    def count_all(self) -> int:
        """
        전체 엔티티 개수를 반환하는 메서드.
        """
        return self.db.query(self.entity).count()

    def save(self, entity: T) -> T:
        """
        엔티티를 데이터베이스에 저장하는 메서드.
        """
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, entity_id: int, **kwargs) -> Optional[T]:
        """
        특정 ID의 엔티티를 업데이트하는 메서드.
        """
        entity = self.db.query(self.entity).filter(self.primary_key == entity_id).first()
        if not entity:
            return None

        # 존재하는 필드만 업데이트
        entity_columns = {column.name for column in inspect(self.entity).c}
        valid_data = {key: value for key, value in kwargs.items() if key in entity_columns}

        for key, value in valid_data.items():
            setattr(entity, key, value)

        try:
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_by_id(self, entity_id: int) -> bool:
        """
        특정 ID의 엔티티를 삭제하는 메서드.
        """
        stmt = delete(self.entity).where(self.primary_key == entity_id)
        try:
            result = self.db.execute(stmt)
            self.db.commit()
            return bool(result.rowcount)
        except Exception as e:
            self.db.rollback()
            raise e

    def exists_by_id(self, entity_id: int) -> bool:
        """
        특정 ID의 엔티티 존재 여부를 확인하는 메서드.
        """
        return self.db.query(self.entity).filter(self.primary_key == entity_id).first() is not None

    def find_by_native_query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        네이티브 SQL 쿼리를 실행하는 메서드.
        """
        result = self.db.execute(text(sql), params or {}).mappings().all()
        return [dict(row) for row in result]
