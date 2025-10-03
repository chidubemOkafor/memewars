from apscheduler.schedulers.background import BackgroundScheduler
from models.models import Campaign
from models.database import SessionLocal
from sqlalchemy.orm import Session
from datetime import timedelta
from main import logger

scheduler = BackgroundScheduler()
scheduler.start()

def end_campaign(camp_id: int):
    db = SessionLocal()
    try:
        camp = db.query(Campaign).filter(Campaign.id == camp_id).first()
        if camp:
            camp.isVoting = False
            camp.isEnded = True
            # TODO: award badges to winner
            db.commit()
    finally:
        db.close()

def start_voting(camp_id: int):
    db = SessionLocal()
    try:
        camp = db.query(Campaign).filter(Campaign.id == camp_id).first()
        if camp:
            # if no memes/art posted, end immediately
            if len(camp.memes) == 0:
                logger.info(f"ended reason: not enough memes created for {function.__name__}")
                print("ended with not meme created")
                camp.isEnded = True
                
            else:
                camp.isPosting = False
                camp.isVoting = True
                db.commit()

                logger.info(f"end campaign job awaited for {camp.start_date + timedelta(days=4)} for {function.__name__}")
                scheduler.add_job(
                    end_campaign,
                    "date",
                    run_date=camp.start_date + timedelta(days=4),
                    args=[camp.id]
                )
    finally:
        db.close()

def start_campaign(camp_id: int):
    db = SessionLocal()
    try:
        camp = db.query(Campaign).filter(Campaign.id == camp_id).first()
        if camp and not camp.isPosting:
            camp.isPosting = True
            db.commit()

            logger.info(f"start voting job awaited for {camp.start_date + timedelta(days=2)} for {function.__name__}")
            scheduler.add_job(
                start_voting,
                "date",
                run_date=camp.start_date + timedelta(days=2),
                args=[camp.id]
            )
    finally:
        db.close()

def schedule_campaign(camp: Campaign):
    logger.info(f"start campaign job awaited for {camp.start_date} for {function.__name__}")
    scheduler.add_job(
        start_campaign,
        "date",
        run_date=camp.start_date,
        args=[camp.id]
    )
