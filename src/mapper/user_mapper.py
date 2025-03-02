from src.entity.user_entity import UserEntity
from src.model.user_model import UserModel

def model_to_entity(user_model: UserModel) -> UserEntity:
    """
    ORM 모델을 도메인 엔티티로 변환합니다.
    Model은 ORM(SQLAlchemy)에서 직접 사용하는 데이터베이스 모델이며,
    Entity는 비즈니스 로직을 수행하는 도메인 객체입니다.
    도메인 계층에서 데이터베이스 종속성을 줄이기 위해 Entity로 변환하여 사용합니다.
    """
    return UserEntity(
        id=user_model.id,
        username=user_model.username,
        email=user_model.email,
        full_name=user_model.full_name
    )

def entity_to_model(user_entity: UserEntity, password: str) -> UserModel:
    """
    도메인 엔티티를 ORM 모델로 변환합니다.
    단, domain entity에는 보안상 비밀번호 정보가 없으므로,
    추가 파라미터로 해시된 비밀번호(password)를 받아서 적용합니다.
    """
    return UserModel(
        username=user_entity.username,
        email=user_entity.email,
        full_name=user_entity.full_name,
        password=password
    )