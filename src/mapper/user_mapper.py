from src.domain.user_domain import UserDomain
from src.entity.user_entity import UserEntity

def entity_to_domain(user_entity: UserEntity) -> UserDomain:
    """
    (ORM 엔티티 → 도메인 객체 변환)
    ORM Entity를 도메인 객체로 변환합니다.
    Entity는 ORM(SQLAlchemy)에서 직접 사용하는 데이터베이스 모델이며,
    Domain은 비즈니스 로직을 수행하는 도메인 객체입니다.
    도메인 계층에서 데이터베이스 종속성을 줄이기 위해 Domain으로 변환하여 사용합니다.
    """
    return UserDomain(
        seq=user_entity.seq,
        username=user_entity.username,
        email=user_entity.email,
        type=user_entity.type,
        status=user_entity.status,
        password = user_entity.password,
        current_refresh_token=user_entity.current_refresh_token,
        created_at=user_entity.created_at,
        updated_at=user_entity.updated_at,
        deleted_at=user_entity.deleted_at

    )

def domain_to_entity(user_domain: UserDomain, password: str) -> UserEntity:
    """
    (도메인 객체 → ORM 엔티티 변환)
    Doamin 객체를 ORM Entity로 변환합니다.
    단, Domain 객체에는 보안상 비밀번호 정보가 없으므로,
    추가 파라미터로 해시된 비밀번호(password)를 받아서 적용합니다.
    """
    return UserEntity(
        username=user_domain.username,
        email=user_domain.email,
        type=user_domain.type,
        status=user_domain.status,
        password=password,
        current_refresh_token=user_domain.current_refresh_token,
        created_at=user_domain.created_at,
        updated_at=user_domain.updated_at
    )