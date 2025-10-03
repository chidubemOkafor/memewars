from fastapi import APIRouter, Depends
from requests import Session
from models.models import Badge
from models.dependency import get_db
from services.badge_services import create_badge_for_admin

router = APIRouter()

# @router.get("")
# def get_profile(user_id: int, db: Session = Depends(get_db)):

@router.post("/create_badge")
def create_badge():
    user_id: int = 0
    
