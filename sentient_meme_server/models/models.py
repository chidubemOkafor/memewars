from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.database import engine

Base = declarative_base()

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
    scope = Column(String)
    token_type = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)


class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    start_date = Column(DateTime)
    isVoting = Column(Boolean, default=False)
    isPosting = Column(Boolean, default=False)
    isEnded = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    memes = relationship("Meme", back_populates="campaign", cascade="all, delete-orphan")

class Meme(Base):
    __tablename__ = 'meme'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    campaign = relationship("Campaign", back_populates="memes")
    user = relationship("User", back_populates="memes")

class Leaderboard(Base):
    __tablename__ = 'leaderboard'

    id = Column(Integer, primary_key=True, index=True)
    meme_id = Column(Integer, ForeignKey("meme.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    score = Column(Integer, default=0)

    meme = relationship("Meme")
    campaign = relationship("Campaign")


Base.metadata.create_all(bind=engine)