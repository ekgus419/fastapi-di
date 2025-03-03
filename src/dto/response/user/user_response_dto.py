from pydantic import BaseModel

class UserResponseDto(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None

    model_config = {
        "from_attributes": True, # ORM 모델에서 데이터를 읽어올 때 사용
    }
