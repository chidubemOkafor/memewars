import os
from urllib.parse import urlencode
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from models.models import User
import secrets
import base64
import hashlib
load_dotenv()

CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
REDIRECT_URI = os.getenv("TWITTER_REDIRECT_URI")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")

print(f"redirect uri: {REDIRECT_URI}")

session_store = {}

def get_login_url():
    state = secrets.token_urlsafe(16)
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode("utf-8")

    session_store[state] = {"code_verifier": code_verifier}

    query = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "tweet.read users.read offline.access",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"https://twitter.com/i/oauth2/authorize?{urlencode(query)}"

def generate_access_token(code: str, state: str):
    import requests

    if state not in session_store:
        raise ValueError("Invalid state")

    code_verifier = session_store[state]["code_verifier"]
    del session_store[state]

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()

    token_url = "https://api.twitter.com/2/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",    
        "Authorization": f"Basic {b64_credentials} "
    }
    data = {
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        raise ValueError("Failed to obtain access token")

    return response.json()

def create_user(
        twitter_id: str, 
        access_token: str, 
        refresh_token: str, 
        username: str, 
        display_name: str, 
        profile_image_url: str, 
        token_expires_at, 
        scope: str, 
        token_type: str,
        db: Session
        ):

    if isinstance(token_expires_at, int):
        token_expires_at = datetime.now() + timedelta(seconds=token_expires_at)

    user = db.query(User).filter(User.twitter_id == twitter_id).first()
    if user:
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.username = username
        user.display_name = display_name
        user.profile_image_url = profile_image_url
        user.token_expires_at = token_expires_at
        user.scope = scope
        user.token_type = token_type
        user.updated_at = datetime.now() 
    
    else:
        user = User(
            twitter_id=twitter_id,
            access_token=access_token,
            refresh_token=refresh_token,
            username=username,
            display_name=display_name,
            profile_image_url=profile_image_url,
            token_expires_at=token_expires_at,
            scope=scope,
            token_type=token_type
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def generate_token(payload: dict, db: Session):
    ACCESS_SECRET = os.getenv("ACCESS_SECRET")

    import jwt
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=2)
    access_token = jwt.encode(payload, ACCESS_SECRET, algorithm="HS256")
    refresh_token = secrets.token_urlsafe(64)
    refresh_expiry = datetime.now(timezone.utc) + timedelta(days=30)

    db.query(User).filter(User.id == payload["user_id"]).update(
        { 
            "app_refresh_token": refresh_token,
            "app_refresh_token_expires_at": refresh_expiry 
        }
    )
    db.commit()
    db.close()

    return access_token


    

    
    
