from fastapi import Depends, HTTPException, status
from starlette.requests import Request
from schemas import UserModel  

def get_current_user(request: Request) -> UserModel:
    user = request.session.get("user")
    if user:
        return UserModel(**user)  
    else:
        return UserModel(is_authenticated=False, role=None)
