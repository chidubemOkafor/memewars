from requests import Session
from models.models import Campaign, Meme, User, Vote
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, asc, desc
import supabase
from fastapi import UploadFile
from main import logger
from util.helper import func_name

async def store_meme(file: UploadFile, camp_id: int, user_id: int, db: Session, title: str):
    isValidUser(user_id, db)
    
    isValidCampaign = db.query(Campaign).filter(Campaign.id == camp_id).first()
    if not isValidCampaign:
        logger.error(f"not campaign with that id for {func_name()}")
        return {"error": "not campaign with that id"}, 404

    if isValidCampaign.isEnded:
        logger.info(f"oops campaign has ending for {func_name()}")
        return {"message", "oops campaign has ending"}

    if not isValidCampaign.isPosting:
        logger.info(f"posting has been closed for campaign try voting for {func_name()}")
        return {"message", "posting has been closed for campaign try voting"}
    
    # check if the user has already uploaded a meme
    
    contents = await file.read()

    # with message brokers (rabbitMQ)
    #  |                |
    #  |                |
    #  V                V
    #  --------------------------------------------------------------------------            
    #  | first I check if the meme has been used before?                        |
    #  | this is where I check if the image is good with my image check service |
    #  --------------------------------------------------------------------------
    
    
    supabase.storage.from_("images_bucket").upload(
        f"uploads/{file.filename}", contents
    )
    logger.info(f"Meme uploaded successfully for {func_name()}")

    public_url = supabase.storage.from_("images_bucket").get_public_url(
        f"uploads/{file.filename}"
    )
    logger.info(f"Url fetched successfully for {func_name()}")

    new_meme = Meme(
        url=public_url,
        campaign_id=camp_id,
        user_id=user_id,
        title=title
    )

    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)

    logger.info(f"Meme created successfully for {func_name()}")

    return {
        "message": "meme uploaded successfully", 
        "meme": {
            "id": new_meme.id,
            "url": new_meme.url,
            "campaign_id" : new_meme.campaign_id,
            "user_id" : new_meme.user_id,
            "created_at" : new_meme.created_at,
            "updated_at" : new_meme.updated_at,
            "score": new_meme.score,
            "campaign" : new_meme.campaign,
            "user" : new_meme.user
        }
    }

def get_user_memes(user_id: int, db: Session):
    user: User = isValidUser(user_id, db)

    logger.info(f"fetched meme successfully for {user_id} for {func_name()}")

    return {
        "message": "fetched meme successfully",
        "meme": [
            {
                "id": m.id,
                "url": m.url,
                "created_at": m.created_at,
                "updated_at": m.updated_at,
                "score": m.score,
                "campaign_name": m.campaign.name,
                "campaign_id": m.campaign.id
            } 
            for m in user.memes
        ]
    }

def user_meme_rank(camp_id: int, user_id: int, db: Session):
    user = isValidUser(user_id, db)

    campaign = db.query(Campaign).filter(Campaign.id == camp_id).first()
    if not campaign:
        logger.error(f"Campaign not found for {func_name()}")
        return {"error": "Campaign not found"}, 404

    ranked_memes = (
        db.query(
            Meme.id,
            Meme.user_id,
            Meme.score,
            Meme.created_at,
            func.rank()
            .over(order_by=[desc(Meme.score), asc(Meme.created_at)])
            .label("rank")
        )
        .filter(Meme.campaign_id == camp_id)
        .subquery()
    )

    user_ranks = (
        db.query(ranked_memes.c.id,
                 ranked_memes.c.score,
                 ranked_memes.c.created_at,
                 ranked_memes.c.rank)
        .filter(ranked_memes.c.user_id == user_id)
        .all()
    )

    if not user_ranks:
        logger.error(f"User: {user.name} has no meme in this campaign for {func_name()}")
        return {"error": "User has no meme in this campaign"}, 404

    logger.info(f"User: {user.name} rank returned successfully for {func_name()}")
    return {
        "user_id": user_id,
        "campaign_id": camp_id,
        "memes": [
            {
                "meme_id": r.id,
                "score": r.score,
                "created_at": r.created_at,
                "rank": r.rank
            }
            for r in user_ranks
        ]
    }    

def get_meme(meme_id: int, db: Session):
    meme: Meme = db.query(Meme).filter(Meme.id == meme_id).first()

    if not meme:
        logger.error("No meme with that id")
        return {"error": "no meme with that id"}, 404
    
    logger.info("Meme fetched successfully")
    return {
        "message": "meme fetched successfully",
        "meme": {
            "id": meme.id,
            "url": meme.url,
            "campaign_id": meme.campaign_id,
            "user_id": meme.user_id,
            "created_at": meme.created_at,
            "updated_at": meme.updated_at,
            "score": meme.score,
            "campaign": meme.campaign,
            "user": meme.user
        }
    }

def handle_voting(user_id: int, meme_id: int, db: Session, voting_type: str):
    user = isValidUser(user_id, db)

    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if not meme:
        logger.error(f"no meme with that id for {func_name()}")
        return {"error": "no meme with that id"}, 404

    if meme.campaign.isEnded:
        logger.error(f"oops campaign has ended for {func_name()}")
        return {"error": "oops campaign has ended"}, 400
    
    if not meme.campaign.isVoting:
        logger.error(f"voting is not allowed yet for {func_name()}")
        return {"error": "voting is not allowed yet"}, 400

    if voting_type == "upvote":
        vote_value = 1
    elif voting_type == "downvote":
        vote_value = -1
    else:
        logger.error(f"invalid voting type for {func_name()}")
        return {"error": "invalid voting type"}, 400

    vote = Vote(user_id=user_id, meme_id=meme_id, vote=vote_value)
    meme.score += vote_value

    db.add(user)
    db.add(vote)
    db.add(meme)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.error(f"user has already voted on this meme for {func_name()}")
        return {"error": "user has already voted on this meme"}, 400

    db.refresh(meme)
    logger.info(f"vote recorded successfull for {func_name()}")
    return {"message": "vote recorded successfully", "score": meme.score}

def isValidUser(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"user id does not exist or does not belong to user for {func_name()}")
        return {"error": "user id does not exist or does not belong to user"}, 404
    return user