from requests import Session
from sqlalchemy import asc, desc, func

from models.models import User, Meme
from main import logger
from util.helper import func_name

def get_user(user_id: int, db: Session):
    user: User = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"user not found func: {func_name()}")
        return {"error": "user not found"}, 404

    ranked_memes = (
        db.query(
            Meme.id,
            Meme.url,
            Meme.title,
            Meme.score,
            Meme.created_at,
            Meme.campaign_id,
            func.rank().over(
                partition_by=Meme.campaign_id,
                order_by=[desc(Meme.score), asc(Meme.created_at)]
            ).label("position")
        )
        .filter(Meme.user_id == user.id)
        .all()
    )

    ranked_memes = sorted(
        ranked_memes,
        key=lambda m: (-m.score, m.created_at)
    )

    podiums = sum(1 for meme in ranked_memes if meme.position <= 3)

    return {
        "message": "successfully returned user",
        "user": {
            "profile_image": user.profile_image_url,
            "username": f"@{user.username}",
            "total_memes_voted_for": user.votes_length,
            "total_vote_earned": len(user.votes),
            "amount_of_uploaded_meme": len(user.memes),
            "podiums": podiums,
            "average_votes_per_meme": get_average_meme_score(user),
            "badges": 0,
            "memes": [{
                "meme_id": meme.id,
                "meme_url": meme.url,
                "meme_title": meme.title,
                "meme_score": f"{meme.score} votes",
                "position": meme.position
            } for meme in ranked_memes]
        }
    }


def get_average_meme_score(user: User):
    if not user.memes:
        return 0  

    total_score = sum(meme.score for meme in user.memes)
    return total_score / len(user.meme)


