from fastapi import Depends

from models.database import SessionLocal
from models.dependency import get_db
from models.models import Badge

badges = [
  {
    "name": "First Vote",
    "description": "Awarded for casting your first vote.",
    "rarity": "COMMON",
    "category": "ACHIEVEMENT",
    "requirements": "Cast your first vote.",
    "badge_image": "👍"
  },
  {
    "name": "Early Bird",
    "description": "Awarded for uploading a meme within 24 hours of a campaign starting.",
    "rarity": "UNCOMMON",
    "category": "PARTICIPATION",
    "requirements": "Upload a meme within 24 hours of a campaign starting.",
    "badge_image": "🐦"
  },
  {
    "name": "Commenter",
    "description": "Awarded for leaving your first comment.",
    "rarity": "COMMON",
    "category": "SOCIAL",
    "requirements": "Leave your first comment.",
    "badge_image": "💬"
  },
  {
    "name": "Uploader",
    "description": "Awarded for uploading 10 memes.",
    "rarity": "UNCOMMON",
    "category": "PARTICIPATION",
    "requirements": "Upload 10 memes.",
    "badge_image": "📸"
  },
  {
    "name": "Super Uploader",
    "description": "Awarded for uploading 100 memes.",
    "rarity": "RARE",
    "category": "PARTICIPATION",
    "requirements": "Upload 100 memes.",
    "badge_image": "🚀"
  },
  {
    "name": "Voter",
    "description": "Awarded for casting 50 votes.",
    "rarity": "UNCOMMON",
    "category": "PARTICIPATION",
    "requirements": "Cast 50 votes.",
    "badge_image": "🗳️"
  },
  {
    "name": "Super Voter",
    "description": "Awarded for casting 500 votes.",
    "rarity": "RARE",
    "category": "PARTICIPATION",
    "requirements": "Cast 500 votes.",
    "badge_image": "🔥"
  },
  {
    "name": "Campaigner",
    "description": "Awarded for participating in 10 different campaigns.",
    "rarity": "UNCOMMON",
    "category": "PARTICIPATION",
    "requirements": "Participate in 10 different campaigns.",
    "badge_image": "🏁"
  },
  {
    "name": "On the Podium",
    "description": "Awarded for placing in the top 3 of any campaign.",
    "rarity": "UNCOMMON",
    "category": "PERFORMANCE",
    "requirements": "Place in top 3 of any campaign.",
    "badge_image": "🥉"
  },
  {
    "name": "Winner Winner",
    "description": "Awarded for winning your first campaign.",
    "rarity": "RARE",
    "category": "PERFORMANCE",
    "requirements": "Win 1 campaign.",
    "badge_image": "🥇"
  },
  {
    "name": "Champion",
    "description": "Awarded for winning 5 campaigns.",
    "rarity": "EPIC",
    "category": "PERFORMANCE",
    "requirements": "Win 5 campaigns.",
    "badge_image": "👑"
  },
  {
    "name": "Consistent Performer",
    "description": "Awarded for maintaining an average meme score above 20 votes.",
    "rarity": "RARE",
    "category": "PERFORMANCE",
    "requirements": "Average meme score > 20 votes.",
    "badge_image": "📊"
  },
  {
    "name": "Viral Meme",
    "description": "Awarded for a meme that scores over 100 votes.",
    "rarity": "EPIC",
    "category": "CREATIVITY",
    "requirements": "A single meme scores 100+ votes.",
    "badge_image": "🌐"
  },
  {
    "name": "Liked Artist",
    "description": "Awarded for receiving 100 total votes across all memes.",
    "rarity": "UNCOMMON",
    "category": "SOCIAL",
    "requirements": "Receive 100 total votes across all memes.",
    "badge_image": "❤️"
  },
  {
    "name": "Beloved Creator",
    "description": "Awarded for receiving 1,000 total votes across all memes.",
    "rarity": "RARE",
    "category": "SOCIAL",
    "requirements": "Receive 1,000 total votes.",
    "badge_image": "🌟"
  },
  {
    "name": "Supporter",
    "description": "Awarded for voting for at least 10 different users' memes.",
    "rarity": "COMMON",
    "category": "SOCIAL",
    "requirements": "Vote for at least 10 different users’ memes.",
    "badge_image": "🙌"
  },
  {
    "name": "Friendly Rival",
    "description": "Awarded for competing in campaigns with the same user 5 times.",
    "rarity": "UNCOMMON",
    "category": "SOCIAL",
    "requirements": "Compete in campaigns with the same user 5 times.",
    "badge_image": "⚔️"
  },
  {
    "name": "Meme Legend",
    "description": "Awarded for winning 50 campaigns.",
    "rarity": "LEGENDARY",
    "category": "SPECIAL",
    "requirements": "Win 50 campaigns.",
    "badge_image": "🐉"
  },
  {
    "name": "Underdog Victory",
    "description": "Awarded for winning a campaign from outside the top 10 halfway through.",
    "rarity": "EPIC",
    "category": "SPECIAL",
    "requirements": "Win a campaign that wasn’t in the top 10 halfway through.",
    "badge_image": "🐺"
  },
  {
    "name": "Collector",
    "description": "Awarded for uploading a meme to every active campaign in a single week.",
    "rarity": "EPIC",
    "category": "SPECIAL",
    "requirements": "Upload a meme to every active campaign in a single week.",
    "badge_image": "🖼️"
  },
  {
    "name": "Loyal Player",
    "description": "Awarded for logging in every day for 30 days.",
    "rarity": "EPIC",
    "category": "SPECIAL",
    "requirements": "Log in every day for 30 days.",
    "badge_image": "🔑"
  },
  {
    "name": "OG",
    "description": "Awarded to the first 100 users to join the platform.",
    "rarity": "LEGENDARY",
    "category": "SPECIAL",
    "requirements": "Be among the first 100 users to join the platform.",
    "badge_image": "🏆"
  }
]

db = SessionLocal()
for badge in badges:
    print(badge["name"])
    new_badge = Badge(
        name=badge["name"],
        description=badge["description"],
        rarity=badge["rarity"],
        category=badge["category"],
        requirements=badge["requirements"],
        badge_image=badge["badge_image"]
    )

    db.add(new_badge)
    db.commit()
    db.refresh(new_badge)

print("done")