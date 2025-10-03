from fastapi import APIRouter, Depends
from services.campaign_service import create_campaign, delete_campaign, get_active_campaigns, get_campaign
from sqlalchemy.orm import Session
from models.dependency import get_db
from datetime import datetime
from typing import Optional


router = APIRouter()

#   name = payload["name"]
#     description = payload["description"]
#     start_date = payload["start_date"]

@router.post("/")
async def create(name: str, description: str, start_date: datetime,  db: Session = Depends(get_db)):
    try:
        campaign = create_campaign(name, description, start_date, db)

        print(campaign)
        return campaign
        
    except Exception as e:
        print(f"error: {e}")

@router.delete("/")
async def delect_camp(camp_id: str, db: Session = Depends(get_db)):
    try:
        campaign = delete_campaign(camp_id, db)

        print(campaign)
        return campaign
    
    except Exception as e:
        print(f"error: {e}")

#  filters -> active, posting, voting, ended, upcoming
#  active is when either the posting and the voting is true
#  posting is when only the posting is true
#  voting is when only the voting is true
#  ended is when the campain has ended
# upcoming only the campaing this not active

@router.get("")
async def get_campaigns(
        isPosting: Optional[bool] = None,
        isVoting: Optional[bool] = None,
        isEnded: Optional[bool] = None,
        isUpcoming: Optional[bool] = None,
        db: Session = Depends(get_db)):
    try: 
        campaigns = get_active_campaigns(isPosting, isVoting, isEnded, isUpcoming, db)
        return campaigns
    except Exception as e:
        print(f"error: {e}")

@router.get("/get_campaign")
async def get_s_campaign(camp_id: int, db: Session = Depends(get_db)):
    try: 
        campaigns = get_campaign(camp_id, db)
        return campaigns
    except Exception as e:
        print(f"error: {e}")

# async def get_active_camp_entries():
#     try:

#     except  Exception as e:
#         print(f"error: {e}")