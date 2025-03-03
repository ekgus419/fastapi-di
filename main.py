from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from src.core.exception_handlers import register_exception_handlers
from src.routers.v1.user.user_router import router as user_router
from src.routers.v1.auth.auth_router import router as auth_router
from src.core.container import container
from dependency_injector import providers
from src.config.logging_config import configure_logging

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    애플리케이션 시작 및 종료 시 실행할 리소스 초기화 및 정리.
    """
    container.init_resources()
    container.wire(packages=["src.routers"])
    yield  # FastAPI 앱 실행 (요청을 처리하는 동안 대기)
    container.shutdown_resources()

app = FastAPI(lifespan=lifespan)

# 예외 핸들러 등록
register_exception_handlers(app)

# 로깅 설정 적용
configure_logging()

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
