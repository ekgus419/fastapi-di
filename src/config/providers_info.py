"""
BaseRepository는 직접 인스턴스화해서 사용하지 않고,
구체적인 Repository(예: UserRepository)가 상속받아 사용하는 추상적인 기본 클래스이기 때문에,
providers_info에 따로 등록하지 않는다.
Providers_info에는 실제 DI 컨테이너를 통해 인스턴스를 생성할 구체적인 클래스들만 등록한다.
"""

PROVIDERS_INFO = {
    "user_repository": {
        "module": "src.repository.user.user_repository",   # 모듈 경로
        "class": "UserRepository",                         # 클래스명
        "dependencies": {
            "db": "db_session"                             # 의존성: 컨테이너에 정의된 db_session provider 참조
        },
    },
    "user_service": {
        "module": "src.service.user.user_service",
        "class": "UserService",
        "dependencies": {
            "user_repository": "user_repository",          # 의존성: 자동 등록된 user_repository provider 참조
        },
    },
    "auth_service": {
        "module": "src.service.auth.auth_service",
        "class": "AuthService",
        "dependencies": {
            "user_repository": "user_repository"
        },
    },
}
