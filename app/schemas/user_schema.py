from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.enums import Role
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserLogin(UserBase):
    password: str = Field(..., min_length = 8)

class UserRegister(UserBase):
    username: str = Field(..., min_length = 2, max_length=30)
    password: str = Field(..., min_length = 8, max_length= 72)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
    email: EmailStr
    role: Role
    created_at: datetime

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=2, max_length=30)
    email: EmailStr | None = None

class PasswordUpdate(BaseModel):
    current_password: str = Field(min_length=8, max_length=72)
    new_password: str = Field(min_length=8, max_length=72)

class UserLoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
    role: Role
    access_token: str
    token_type: str = "bearer"

class UserRegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
