from fastapi import Depends
from models.dependency import get_db
from models.models import Badge, Meme, User, Campaign, UserBadge, UserBadgeProgress, Vote
from requests import Session
from logger_conf import logger
from datetime import datetime, timedelta, timezone

# for vote
def handle_vote_badges(user_id: int, db: Session):
    latest_vote = fetch_latest_vote_by_user(user_id, db)
    if not latest_vote:
        return
    
    badges = [
        ("Voter", 50),
        ("Super Voter", 500),
        ("First Vote", 1)
    ]

    badges = filter_badges_array(user_id, db, badges)
    vote_count = db.query(Vote).filter(Vote.user_id == user_id).count()

    for badge_name, goal in badges:
            handle_badge_tracking_and_awarding(user_id, badge_name, vote_count, goal, db)

    db.commit()

# for meme
def handle_upload_badges(user_id, db: Session):
    latest_meme = fetch_latest_meme_by_user(user_id, db)
    if not latest_meme:
        return
    
    badges = [
        ("First Upload", 1),
        ("Early Bird", 1),
        ("Uploader", 10),
        ("Super Uploader", 100)
    ]

    badges = filter_badges_array(user_id, db, badges)
    meme_count = db.query(Meme).filter(Meme.user_id == user_id).count()

    for badge_name, goal in badges:
        if badge_name == "Early Bird":
            if latest_meme and (latest_meme.created_at - latest_meme.campaign.created_at < timedelta(hours=24)):
                handle_badge_tracking_and_awarding(user_id, badge_name, meme_count, goal, db)
        
        else:
            handle_badge_tracking_and_awarding(user_id, badge_name, meme_count, goal, db)
    
    db.commit()


# Champion	            👑	EPIC	    PERFORMANCE	Win 5 campaigns.
def handle_champion_badge(user_id: int, db: Session):
    # user need to have a total of 5 campaign wins
    

# for meme and vote
def handle_campainer_badge(user_id: int, db: Session):
    badges = filter_badges_array(user_id, db, [("Campaigner", 10)])
    if len(badges) == 0:
        return
    
    posted_campaigns = db.query(Meme.campaign_id).filter(Meme.user_id == user_id)
    voted_campaigns = (
        db.query(Meme.campaign_id)
        .join(Vote, Vote.meme_id == Meme.id)
        .filter(Vote.user_id == user_id)
    )

    both_campaigns = posted_campaigns.intersect(voted_campaigns).distinct().all()
    campaign_count = len(both_campaigns)

    handle_badge_tracking_and_awarding(user_id, badges[0][0], campaign_count, badges[0][1], db)
    
    db.commit()


def handle_badge_tracking_and_awarding(user_id: int, badge_name: str,current_value: int, goal: int, db: Session, commit: bool = False):
    badge = fetch_badge(db, badge_name)
    progress = (
        db.query(UserBadgeProgress)
        .filter(UserBadgeProgress.user_id == user_id, UserBadgeProgress.badge_id == badge.id)
        .first()
    )

    if not progress:
        progress = UserBadgeProgress(user_id=user_id, badge_id=badge.id, goal=goal, progress=0)
        db.add(progress)

    new_progress = min(current_value, goal)
    if progress.progress != new_progress:
        progress.progress = new_progress

    if progress.progress >= goal and not progress.completed:
        progress.completed = True
        set_badge(user_id, badge, db)

    if commit:
        db.commit()
    return {"message": f"Progress updated: {progress.progress}/{progress.goal}"}


def fetch_campaign(camp_id: int, db: Session):
    campaign = db.query(Campaign).filter(Campaign.id == camp_id).first()
    if not campaign:
        logger.error("no campaign for this exists")
        print("no campaign for this exists")
    
    return campaign

def fetch_badge(db: Session, name: str):
    return db.query(Badge).filter(Badge.name == name).first()

def fetch_latest_meme_by_user(user_id: int, db: Session):
    latest_meme = (
        db.query(Meme)
        .filter(Meme.user_id == user_id)
        .order_by(Meme.created_at.desc())
        .first()
    )
    return latest_meme

def filter_badges_array(user_id: int, db: Session, badges: list[tuple[str, int]]):
    user_badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
    user_badge_names = {ub.badge.name for ub in user_badges}

    new_badges = [b for b in badges if b[0] not in user_badge_names]

    return new_badges

def fetch_latest_vote_by_user(user_id:int, db: Session):
    latest_vote = (
        db.query(Vote)
        .filter(Vote.user_id == user_id)
        .order_by(Vote.created_at.desc()) 
        .first()
    )

    return latest_vote

def set_badge(user_id: int, badge: Badge, db: Session):

    new_user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
    db.add(new_user_badge)

    return {"message": f"{badge.name} badge awarded successfully!"}

def fetch_user(user_id: int, db: Session):
    user: User = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error("not user")
        print("not user")

    return user

