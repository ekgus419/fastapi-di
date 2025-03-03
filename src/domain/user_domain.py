from dataclasses import dataclass
from typing import Optional

from pydantic import EmailStr


@dataclass
class UserDomain:
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
