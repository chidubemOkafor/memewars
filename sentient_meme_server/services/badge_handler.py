from fastapi import Depends
from models.dependency import get_db
from models.models import User, Campaign
from requests import Session
from logger_conf import logger


def handle_first_upload(user_id: int):
    db: Session = Depends(get_db) # this is used to query the db

    user = fetch_user(user_id, db)

    # check if we only have one upload for the user
    if len(user.memes) == 1:
        print("you now have first_upload badge")
        # this is where i send the badge to the user
    # user_id 
    # this checks if the upload is the first or not
    
def handle_first_vote(user_id: int):
    db: Session = Depends(get_db)

    user = fetch_user(user_id, db)

    if len(user.votes) == 1:
        print("you now have first_vote badge")

def handle_early_bird(user_id: int, camp_id: int):
    # is_repeatable
    db: Session = Depends(get_db)

    user = fetch_user(user_id, db)
    campaign = fetch_campaign(camp_id, db)

    # check if the badge already exists
    user.user_badges

    



def fetch_campaign(camp_id: int, db: Session):
    campaign = db.query(Campaign).filter(Campaign.id == camp_id).first()
    if not campaign:
        logger.error("no campaign for this exists")
        print("no campaign for this exists")
    
    return campaign


def fetch_user(user_id: int, db: Session):
    user: User = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error("not user")
        print("not user")

    return user

