from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponseDto(BaseModel, Generic[T]):
    items: List[T]
    total: int              # 전체 아이템 수
    page: int               # 현재 페이지 (1-based)
    size: int               # 페이지 크기(한 페이지당 아이템 수)
    total_pages: int        # 전체 페이지 수
