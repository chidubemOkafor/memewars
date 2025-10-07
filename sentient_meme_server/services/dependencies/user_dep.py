from typing import Dict
from fastapi import Depends, HTTPException, Request, status
from dotenv import load_dotenv
import jwt
import os

from types_1 import ROLE_PERMISSIONS

load_dotenv()

SECRET_KEY = os.getenv("ACCESS_SECRET")
ALGORITHM = "HS256"

def decode_access_token(access_token: str):
    try:
        return jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def get_user(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = decode_access_token(access_token)
    user_id = payload.get("user_id")
    role = payload.get("role")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return {"user_id": user_id, "role": role}

def require_permission(action: str):
    def dependency(user=Depends(get_user)):
        if action not in ROLE_PERMISSIONS.get(user["role"], []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user
    return dependency
