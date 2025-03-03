from src.domain.user_domain import UserDomain
from src.entity.user_entity import UserEntity

def entity_to_domain(user_model: UserEntity) -> UserDomain:
    """
    (ORM 엔티티 → 도메인 객체 변환)
    ORM Entity를 도메인 객체로 변환합니다.
    Entity는 ORM(SQLAlchemy)에서 직접 사용하는 데이터베이스 모델이며,
    Domain은 비즈니스 로직을 수행하는 도메인 객체입니다.
    도메인 계층에서 데이터베이스 종속성을 줄이기 위해 Domain으로 변환하여 사용합니다.
    """
    return UserDomain(
        id=user_model.id,
        username=user_model.username,
        email=user_model.email,
        full_name=user_model.full_name
    )

def domain_to_entity(user_entity: UserDomain, password: str) -> UserEntity:
    """
    (도메인 객체 → ORM 엔티티 변환)
    Doamin 객체를 ORM Entity로 변환합니다.
    단, Domain 객체에는 보안상 비밀번호 정보가 없으므로,
    추가 파라미터로 해시된 비밀번호(password)를 받아서 적용합니다.
    """
    return UserEntity(
        username=user_entity.username,
        email=user_entity.email,
        full_name=user_entity.full_name,
        password=password
    )