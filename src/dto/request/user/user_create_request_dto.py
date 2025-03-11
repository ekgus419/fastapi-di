from pydantic import BaseModel, EmailStr, Field

class UserCreateRequestDto(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, description="비밀번호")
    type: str = Field("100", description="회원 유형")
    status: str = Field("100", description="회원 상태")
