from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy에서 ORM을 사용할 때, 테이블을 정의하고 매핑하기 위한 기반 클래스를 생성하는 함수
Base = declarative_base()


# Alembic이 인식하도록 하기 위해 Base.metadata에 모델을 반영
from src.entity.user_entity import UserEntity
