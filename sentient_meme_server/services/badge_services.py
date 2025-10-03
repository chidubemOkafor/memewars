from typing import Optional
from requests import Session
from models.models import Badge, User
from logger_conf import logger
from util.helper import func_name
from models.schemas import BadgeSchema
# a way to create the badges by the admin
# a place to store the badges craeated by the admin a badge table
# functions so the user can check if he has the badge
# def create_badge():

def create_badge_for_admin(name: str, description: str, rarity: str, category: str, requirements: str, badge_image: str, db: Session):
    # db.query(Badge)
    badge = db.query(Badge).filter(Badge.name == name).first()
    if badge:
        logger.error(f"badge with name already exists func: {func_name()}")
        return {"error": "badge with name already exists"}, 409
    
    new_badge = Badge(
        name,
        description,
        rarity,
        category,
        requirements,
        badge_image
    )

    db.add(new_badge)
    db.commit()
    db.refresh(new_badge)

    logger.info(f"created badge successfully now add logic func: {func_name()}")
    return {
        "message": "created badge successfully now add logic"
    }

def delete_badge(badge_id: int, db: Session):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        logger.error(f"badge with name does not found func: {func_name()}")
        return {"error": "badge with name does not found"}, 404

    db.delete(badge)
    db.commit()

    logger.info(f"badge removed successfully not remove logic func: {func_name()}")
    return {
        "message":"badge removed successfully not remove logic"
    }

def get_badges(category: Optional[str], db: Session):
    query = db.query(Badge)
    
    if category:
        query = query.filter(Badge.category == category)
    
    badges = query.all()

    badges_list = [
        BadgeSchema.model_validate(badge).model_dump()
        for badge in badges
    ]

    return {
        "message": "Successfully returned badges",
        "badges": badges_list
    }

