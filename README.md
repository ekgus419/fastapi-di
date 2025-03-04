# fastapi-di

## 프로젝트 구조 개요

```
fastapi-di/
├── alembic/                         # Alembic 마이그레이션
├── http/                            # API 기능 테스트
├── src/
│   ├── config/                      # 로깅, provider 설정 등
│   ├── core/                        # 핵심 설정 (settings, database, container 등)
│   ├── domain/                      # 도메인 (DB 의존성 없는 순수 객체)
│   ├── dto/                         # Request/Response DTO
│   ├── entity/                      # SQLAlchemy ORM 모델 + base.py (ORM 베이스 클래스)
│   ├── env/                         # 설정 파일 모음
│   ├── exception/                   # 예외 정의
│   ├── mapper/                      # ORM 모델 <-> 도메인 엔티티 변환
│   ├── repository/                  # 데이터 접근 (BaseRepository 상속)
│   ├── routers/                     # FastAPI 라우터 (API 엔드포인트)
│   ├── service/                     # 비즈니스 로직 (BaseService 상속 가능)
│   ├── tests/                       # 테스트 모음
│   └── utils/                       # 유틸 함수 (보안, 토큰, 의존성 등)
├── alembic.ini                      # alembic 설정 파일
├── main.py                          # FastAPI 실행 진입점
└── requirements.txt                 # 프로젝트 의존성 목록
```
