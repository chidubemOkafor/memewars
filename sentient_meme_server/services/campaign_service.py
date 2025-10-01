from sqlalchemy.orm import Session
from models.models import Campaign, Meme
from sqlalchemy import desc, asc
from datetime import datetime

def create_campaign(name: str, description: str, start_date: datetime, db: Session):
    existing_campaign = db.query(Campaign).filter(Campaign.name == name).first()

    if existing_campaign and existing_campaign.isActive:
        return { "message": "this campaign already exists and is active" }, 404
    
    new_campaign = Campaign(
        name=name,
        description=description,
        start_date=start_date,
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

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
    campaign = db.query(Campaign).filter(Campaign.id == camp_id).first()

    if not campaign:
        return {"error": "Campaign not found"}, 404

    if campaign.isActive:
        return {"message": "You cannot delete an active campaign"}

    db.delete(campaign)
    db.commit()

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

    return {
        "message": "successfully fetched campaigns",
        "campaigns": [
            {
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
            for c in campaigns
        ],
    }

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
    campaign = db.query(Campaign).filter(Campaign.id == camp_id).first()
    if not campaign:
        return {"error": "Campaign not found"},404
    c = campaign
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



    

