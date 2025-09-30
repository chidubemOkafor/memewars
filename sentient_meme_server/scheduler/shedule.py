from apscheduler.schedulers.background import BackgroundScheduler
from models.models import Campaign
from models.database import SessionLocal
from sqlalchemy.orm import Session
from datetime import timedelta

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
            if not camp.has_memes:  # pseudo-field, adapt to your logic
                camp.isEnded = True
            else:
                camp.isPosting = False
                camp.isVoting = True
                db.commit()

                # schedule voting end (4 days after start_date)
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

            scheduler.add_job(
                start_voting,
                "date",
                run_date=camp.start_date + timedelta(days=2),
                args=[camp.id]
            )
    finally:
        db.close()

def schedule_campaign(camp: Campaign):
    scheduler.add_job(
        start_campaign,
        "date",
        run_date=camp.start_date,
        args=[camp.id]
    )
