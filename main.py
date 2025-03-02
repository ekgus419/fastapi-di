from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from src.core.exception_handlers import validation_exception_handler, http_exception_handler, \
    general_exception_handler
from src.routers.v1.user.user_router import router as user_router
from src.routers.v1.auth.auth_router import router as auth_router
from src.core.container import container
from dependency_injector import providers
from src.config.logging_config import configure_logging

app = FastAPI()

# 전역 예외 핸들러 등록
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 로깅 설정 적용 (설정 파일에 따라 SQL 쿼리 예쁘게 출력)
configure_logging()

# 테이블 자동 생성 (실무에서는 Alembic 등의 마이그레이션 도구 사용 권장)
# Base.metadata.create_all(bind=engine)

# 애플리케이션 시작 시 리소스 초기화 및 wiring 적용
@app.on_event("startup")
async def startup_event():
    container.init_resources()
    container.wire(packages=["src.routers"])

# 애플리케이션 종료 시 리소스 정리
@app.on_event("shutdown")
async def shutdown_event():
    container.shutdown_resources()

# 미들웨어: 각 요청마다 새로운 DB 세션 생성 및 container의 db_session 공급자 override
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    session = container.db_session()  # 새로운 DB 세션 생성
    try:
        with container.db_session.override(providers.Object(session)):
            response = await call_next(request)
        return response
    finally:
        session.close()

# v1 버전 라우터
app.include_router(user_router, prefix="/v1")
app.include_router(auth_router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
