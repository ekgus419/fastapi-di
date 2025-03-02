from fastapi import HTTPException

class HTTPUnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=401, detail=detail)

class HTTPInvalidRefreshTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid refresh token")
