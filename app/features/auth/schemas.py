from pydantic import BaseModel 
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    username: str
    email: str
    phone: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str 
    refresh_token: str
    token_type: str 
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str   
class VerifyEmailRequest(BaseModel):
    email: str 

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str 
class RefreshTokenRequest(BaseModel):
    refresh_token: str