from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from src.dto.response.common_response import CommonResponse
import logging

async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content=CommonResponse(status="error", data=None, message=str(exc)).dict()
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    # HTTPException을 공통 응답 포맷으로 감싸서 반환
    return JSONResponse(
        status_code=exc.status_code,
        content=CommonResponse(status="error", data=None, message=exc.detail).dict()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 유효성 검사 오류를 처리 (예: 요청 데이터 오류)
    errors = {}
    for err in exc.errors():
        loc = ".".join(map(str, err.get("loc", [])))
        errors[loc] = err.get("msg")
    return JSONResponse(
        status_code=422,
        content=CommonResponse(status="fail", data=errors, message=None).dict()
    )

async def general_exception_handler(request: Request, exc: Exception):
    # 기타 예외에 대해 500 에러와 공통 응답 포맷 적용
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content=CommonResponse(status="error", data=None, message=str(exc)).dict()
    )