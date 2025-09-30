from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,  
    pool_pre_ping=True,    # avoids stale connections
    pool_size=5,           # adjust depending on worker count
    max_overflow=10)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
