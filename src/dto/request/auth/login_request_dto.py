from pydantic import BaseModel, Field

class LoginRequestDto(BaseModel):
    username: str = Field(..., example="john_doe")
    password: str = Field(..., min_length=6, example="secret123")
