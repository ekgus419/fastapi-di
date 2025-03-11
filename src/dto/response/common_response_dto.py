from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

DataT = TypeVar("DataT")

class CommonResponseDto(BaseModel, Generic[DataT]):
    status: str
    data: Optional[DataT] = None
    message: Optional[str] = None
