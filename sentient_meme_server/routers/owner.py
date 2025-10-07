from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from models.models import Badge
from models.dependency import get_db
from models.schemas import BadgeCreate
from services.badge_services import create_badge_for_creator
from services.dependencies.user_dep import require_permission
from logger_conf import logger

router = APIRouter()

@router.post("/create_badge")
def create_badge(
    payload: BadgeCreate,
    db: Session = Depends(get_db),
    user = Depends(require_permission("create_badge"))
    ):
    try:
        return create_badge_for_creator(payload.name, payload.description, payload.rarity, payload.category, payload.requirements, payload.badge_image, db)
    
    except Exception as e:
        logger.exception(f"Error creating badge: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the badge."
        )
    
