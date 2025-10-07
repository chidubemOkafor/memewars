from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.database import engine
from types_1 import CategoryEnum, RarityEnum, RoleEnum

Base = declarative_base()

time = lambda: datetime.now(timezone.utc)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    twitter_id = Column(String, unique=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    app_refresh_token = Column(String, nullable=True)
    app_refresh_token_expires_at = Column(DateTime, nullable=True)
    username = Column(String)
    display_name = Column(String)
    profile_image_url = Column(String)
    token_expires_at = Column(DateTime)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    scope = Column(String)
    token_type = Column(String)
    created_at = Column(DateTime, default=time)
    updated_at = Column(DateTime(timezone=True), default=time, onupdate=time)

    memes = relationship("Meme", back_populates="user", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")
    userbadges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    badge_progress = relationship("UserBadgeProgress", back_populates="user", cascade="all, delete-orphan")

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    start_date = Column(DateTime)
    isVoting = Column(Boolean, default=False)
    isPosting = Column(Boolean, default=False)
    isEnded = Column(Boolean, default=False)

    created_at = Column(DateTime, default=time)
    updated_at = Column(DateTime(timezone=True), default=time, onupdate=time)

    memes = relationship("Meme", back_populates="campaign")
    leaderboard = relationship("Leaderboard", back_populates="campaign")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    rarity = Column(Enum(RarityEnum), nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    requirements = Column(String, nullable=False)
    badge_image = Column(String, nullable=False)

    created_at = Column(DateTime, default=time)
    updated_at = Column(DateTime(timezone=True), default=time, onupdate=time)

    userbadges = relationship("UserBadge", back_populates="badge")

class UserBadgeProgress(Base):
    __tablename__ = "userbadgeprogress"

    id = Column(Integer, primary_key=True)
    badge_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    progress = Column(Integer, default=0)
    goal = Column(Integer)
    completed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=time)
    updated_at = Column(DateTime(timezone=True), default=time, onupdate=time)

    user = relationship("User", back_populates="badge_progress")
    badge = relationship("Badge")

class UserBadge(Base):
    __tablename__ = "userbadges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    created_at = Column(DateTime, default=time)
    updated_at = Column(DateTime(timezone=True), default=time, onupdate=time)

    badge = relationship("Badge", back_populates="userbadges")
    user = relationship("User", back_populates="userbadges")
    

class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=time)
    score = Column(Integer, default=0)  # cached total score

    votes = relationship("Vote", back_populates="meme")
    campaign = relationship("Campaign", back_populates="memes")
    user = relationship("User", back_populates="memes")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meme_id = Column(Integer, ForeignKey("memes.id"), nullable=False)
    vote = Column(Integer, nullable=False)  # +1 for upvote, -1 for downvote
    created_at = Column(DateTime, default=time)
    updated_at = Column(DateTime(timezone=True), default=time, onupdate=time)

    meme = relationship("Meme", back_populates="votes")
    user = relationship("User", back_populates="votes")

    __table_args__ = (UniqueConstraint("user_id", "meme_id", name="_user_meme_uc"),)

class Leaderboard(Base):
    __tablename__ = 'leaderboards'

    id = Column(Integer, primary_key=True, index=True)
    meme_id = Column(Integer, ForeignKey("memes.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    score = Column(Integer, default=0)

    meme = relationship("Meme")
    campaign = relationship("Campaign", back_populates="leaderboard")

Base.metadata.create_all(bind=engine)