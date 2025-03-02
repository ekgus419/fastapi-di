# fastapi-di

## 프로젝트 구조 개요

```
fastapi-boot-rms/
├── src/
│   ├── config/                      # 로깅, provider 설정 등
│   ├── core/                        # 핵심 설정 (settings, database, container 등)
│   ├── dto/                         # Request/Response DTO
│   ├── entity/                      # 도메인 엔티티 (DB 의존성 없는 순수 객체)
│   ├── exception/                   # 예외 정의
│   ├── mapper/                      # ORM 모델 <-> 도메인 엔티티 변환
│   ├── model/                       # SQLAlchemy ORM 모델 + base.py (ORM 베이스 클래스)
│   │   └── base.py                  # from sqlalchemy.ext.declarative import declarative_base
│   ├── repository/                  # 데이터 접근 (BaseRepository 상속)
│   ├── routers/                     # FastAPI 라우터 (API 엔드포인트)
│   ├── service/                     # 비즈니스 로직 (BaseService 상속 가능)
│   └── utils/                       # 유틸 함수 (보안, 토큰, 의존성 등)
├── alembic/                         # Alembic 마이그레이션
├── http/                            # API 기능 테스트
├── main.py                          # FastAPI 실행 진입점
└── requirements.txt                 # 의존성 목록
```

**설계 특징**

*   Spring Boot 스타일의 계층 구조 (Model → Repository → Service → Router).
*   **Domain Entity + Mapper 필수**: DB 의존성 제거, 순수 비즈니스 로직 분리.
*   **BaseRepository** (필수 상속)로 공통 CRUD 로직을 재사용.
*   **Base**(SQLAlchemy 베이스 클래스)는 `model/base.py`에 위치.
*   예외 처리, DTO, DI, 마이그레이션(Alembic) 등을 일관되게 적용.
*   회원 CRUD 와 로그인/로그아웃 기능을 구현.
