from fastapi import FastAPI, Request
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

# v1 버전 라우터
app.include_router(user_router, prefix="/v1/users")
app.include_router(auth_router, prefix="/v1/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
