from pydantic import BaseModel, Field

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="리프레시 토큰")