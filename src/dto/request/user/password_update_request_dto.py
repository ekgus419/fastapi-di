from pydantic import BaseModel, Field

class PasswordUpdateRequestDto(BaseModel):
    password: str = Field(..., min_length=6, description="새 비밀번호")
