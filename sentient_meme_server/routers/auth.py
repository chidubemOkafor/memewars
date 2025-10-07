from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional 
from services.auth_service import get_login_url, generate_access_token, create_user, generate_token
from types_1 import RoleEnum
from x.x_functions import get_x_user_details
from models.dependency import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

@router.get("")
async def login():
    return {"url": get_login_url()}

@router.get("/callback")
async def auth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db),
    response: Response = None
):
    CREATOR_USERNAME = os.getenv("CREATOR_USERNAME")
    try:
        if not code:
            return {"error": "Missing code"}
        if not state:
            return {"error": "Missing state"}

        token_data = generate_access_token(code, state)

        user_data = get_x_user_details(token_data["access_token"])

        created_user = create_user(
            twitter_id=user_data["data"]["id"],
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            username=user_data["data"]["username"],
            display_name=user_data["data"]["name"],
            profile_image_url=user_data["data"].get("profile_image_url", ""),
            token_expires_at=datetime.now() + timedelta(seconds=token_data["expires_in"]),
            scope=token_data["scope"],
            token_type=token_data["token_type"],
            db=db,
            role = RoleEnum.CREATOR if user_data["data"]["username"] == CREATOR_USERNAME else RoleEnum.USER
        )
        
        access_token = generate_token(
            {"user_id": created_user.id, "role": created_user.role.value},
            db=db
        )

        print(access_token)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,
            secure=True,
            samesite="Strict",
            max_age=7200
        )

        return {"message": "Logged in!"}
    except Exception as e:
        print(f"error: {e}")

    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiY3JlYXRvciIsImV4cCI6MTc1OTY4Njc4Mn0.KRgqwhHlwi-mpbNcsd3e77xbYSu4b1FaLFfdKTUMVv0