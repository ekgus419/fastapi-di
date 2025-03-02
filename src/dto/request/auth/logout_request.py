from pydantic import BaseModel, Field

class LogoutRequest(BaseModel):
    username: str = Field(..., example="john_doe")
    refresh_token: str = Field(..., description="로그아웃할 때 사용된 refresh token")
