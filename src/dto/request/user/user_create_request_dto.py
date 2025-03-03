from pydantic import BaseModel, EmailStr, Field

class UserCreateRequestDto(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    full_name: str | None = None
    password: str = Field(..., min_length=6, description="비밀번호")
