from pydantic import BaseModel, Field

class RefreshTokenRequestDto(BaseModel):
    refresh_token: str = Field(..., description="리프레시 토큰")