from pydantic import BaseModel, Field

class PasswordUpdateRequest(BaseModel):
    password: str = Field(..., min_length=6, description="새 비밀번호")
