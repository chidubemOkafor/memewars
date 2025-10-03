from sqlalchemy.orm import Session
from models.models import Campaign, Meme, Vote
from sqlalchemy import desc, asc, func
from datetime import datetime
from scheduler.shedule import schedule_campaign
from main import logger
from util.helper import func_name


def create_campaign(name: str, description: str, start_date: datetime, db: Session):
    existing_campaign = db.query(Campaign).filter(Campaign.name == name).first()

    if existing_campaign and existing_campaign.isActive:
        logger.error(f"this campaign already exists and is active  funct: {func_name()}")
        return { "message": "this campaign already exists and is active" }, 404
    
    new_campaign = Campaign(
        name=name,
        description=description,
        start_date=start_date,
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    # schedule
    logger.info(f"Campaign Scheduled func: {func_name()}")
    schedule_campaign(new_campaign)

    logger.info(f"Campaign created Successfully func: {func_name()}")
    return {
        "message": "campaign created successfully",
        "campaign": {
            "id": new_campaign.id,
            "name": new_campaign.name,
            "description": new_campaign.description,
            "start_date": new_campaign.start_date,
            "isVoting": new_campaign.isVoting,
            "isPosting": new_campaign.isPosting,
            "isEnded": new_campaign.isEnded
        }
    }


def delete_campaign(camp_id: int, db: Session):
    campaign = fetch_camp(camp_id, db)

    if campaign.isActive:
        logger.warning(f"you cannot delete an active campaign func: {func_name()}")
        return {"message": "You cannot delete an active campaign"}

    db.delete(campaign)
    db.commit()

    logger.info(f"Campaign deleted successfully func: {func_name()}")
    return {"message": "Campaign deleted successfully"}

def get_active_campaigns(isPosting, isVoting, isEnded, isUpcoming, db: Session):
    query = db.query(Campaign)

    if isPosting is not None:
        query = query.filter(Campaign.isPosting == isPosting)

    if isVoting is not None:
        query = query.filter(Campaign.isVoting == isVoting)

    if isEnded is not None:
        query = query.filter(Campaign.isEnded == isEnded)

    if isUpcoming is not None:
        if isUpcoming:
            query = query.filter(Campaign.start_date > datetime.now())
        else:
            query = query.filter(Campaign.start_date <= datetime.now())
        
    campaigns = query.all()

    logger.info(f"successfully fetched campaigns func: {func_name()}")
    return {
        "message": "successfully fetched campaigns",
        "campaigns": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "start_date": c.start_date,
                "isPosting": c.isPosting,
                "submissions": len(c.memes),
                "votes": votes(db, c.id),
                "isVoting": c.isVoting,
                "isEnded": c.isEnded,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            }
            for c in campaigns
        ],
    }

def votes(db: Session, campaign_id: int):
    total_votes = (
        db.query(func.count(Vote.id))
        .join(Meme, Meme.id == Vote.meme_id)
        .filter(Meme.campaign_id == campaign_id)
        .scalar()
    )
    return total_votes

def get_campaign_ranking(db: Session, campaign_id: int, page: int = 1, per_page: int = 10):
    if page < 1:
        return {
            "error": "page cannot be less than 1"
        }
    
    offset = (page - 1) * per_page

    memes = (
        db.query(Meme)
        .filter(Meme.campaign_id == campaign_id)
        .order_by(desc(Meme.score), asc(Meme.created_at))
        .offset(offset)
        .limit(per_page)
        .all()
    )

    total_memes = db.query(Meme).filter(Meme.campaign_id == campaign_id).count()
    total_pages = (total_memes + per_page - 1) // per_page

    ranked_memes = []
    for idx, m in enumerate(memes, start=offset + 1):
        ranked_memes.append({
            "rank": idx,
            "id": m.id,
            "url": m.url,
            "score": m.score,
            "created_at": m.created_at,
        })

    return {
        "message": "ranking fetched successfully",
        "campaign_id": campaign_id,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_memes": total_memes,
        "memes": ranked_memes
    }

def get_campaign(camp_id: int, db: Session):
    c = fetch_camp(camp_id, db)
    return {
        "message": "Campaign fetched successfully",
        "campaign": {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "start_date": c.start_date,
                "isPosting": c.isPosting,
                "isVoting": c.isVoting,
                "isEnded": c.isEnded,
                "created_at": c.created_at,
                "updated_at": c.updated_at
        }
    }

def get_active_camp_entries(camp_id: int, db: Session):
    campaign = fetch_camp(camp_id, db)

    if campaign.start_date < datetime.now():
        logger.warning(f"campaign is not active yet func: {func_name()}")
        return {
            "error": "campaign is not active yet"
        }, 409

    return { 
        "message": "Successfully fetched memes for campaign",
        "memes": [{
        "id": meme.id,
        "url": meme.url,
        "creator": meme.user.username,
        "score": meme.score
        } for meme in campaign.memes]
    }
    
# helper fetch Campaign
def fetch_camp(camp_id: int, db: Session):
    campaign = db.query(Campaign).filter(Campaign.id == camp_id).first()
    if not campaign:
        logger.error(f"Campaign not found func: {func_name()}")
        return {"error": "Campaign not found"},404
    
    return campaign