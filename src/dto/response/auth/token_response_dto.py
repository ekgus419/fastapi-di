from pydantic import BaseModel

class TokenResponseDto(BaseModel):
    access_token: str
    refresh_token: str
