from datetime import datetime
from pydantic import BaseModel

class UserResponseDto(BaseModel):
    seq: int
    username: str
    email: str
    type: str
    status: str
    current_refresh_token: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True, # ORM 모델에서 데이터를 읽어올 때 사용
    }
