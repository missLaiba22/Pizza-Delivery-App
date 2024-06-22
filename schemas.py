from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: bool = False
    is_active: bool = True


class LoginModel(BaseModel):
    username: str
    password: str


class UserModel(BaseModel):
    username: str
    email: str
    is_staff: bool
    is_active: bool
    role: str
    user_id: str  # Add user_id field


class OrderCreate(BaseModel):
    flavor: str
    crust: str
    size: str
    user_id: Optional[str] = None  


class OrderUpdate(BaseModel):
    flavor: Optional[str]
    crust: Optional[str]
    size: Optional[str]
    

class OrderStatusUpdate(BaseModel):
    status: str
