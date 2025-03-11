from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from src.dto.response.common_response_dto import CommonResponseDto
import logging

def register_exception_handlers(app: FastAPI):
    """FastAPI 애플리케이션에 전역 예외 핸들러를 등록하는 함수"""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """HTTPException을 공통 응답 포맷으로 감싸서 반환"""
        return JSONResponse(
            status_code=exc.status_code,
            content=CommonResponseDto(status="error", data=None, message=exc.detail).model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """유효성 검사 오류 처리 (예: 요청 데이터 오류)"""
        errors = { ".".join(map(str, err.get("loc", []))): err.get("msg") for err in exc.errors() }
        return JSONResponse(
            status_code=422,
            content=CommonResponseDto(status="fail", data=errors, message=None).model_dump()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """기타 예외에 대해 500 에러와 공통 응답 포맷 적용"""
        logging.error(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=500,
            content=CommonResponseDto(status="error", data=None, message=str(exc)).model_dump()
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """전역 예외 핸들러 - 모든 예외를 처리"""
        logging.error(f"Unhandled error (Global): {exc}")
        return JSONResponse(
            status_code=500,
            content=CommonResponseDto(status="error", data=None, message="Internal Server Error").model_dump()
        )
