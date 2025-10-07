from fastapi import APIRouter, Depends
from requests import Session
from models.models import Badge
from models.dependency import get_db
from services.badge_services import create_badge_for_creator
from services.dependencies.user_dep import require_permission
from types_1 import CategoryEnum, RarityEnum

router = APIRouter()

# @router.get("")
# def get_profile(user_id: int, db: Session = Depends(get_db)):

# name: str, description: str, rarity: str, category: str, requirements: str, badge_image: str, db: Session

@router.post("/create_badge")
def create_badge(
    name: str, 
    description: str, 
    rarity: RarityEnum, 
    category: CategoryEnum, 
    requirements: str, 
    badge_image: str, 
    db: Session = Depends(get_db),
    user = Depends(require_permission("create_badge"))
    ):
    try:
        create_badge_for_creator(name, description, rarity, category, requirements, badge_image, db)
    
    except Exception as e:
        print(f"error {e}")
    
