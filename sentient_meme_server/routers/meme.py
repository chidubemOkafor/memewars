from fastapi import APIRouter, Depends, File, UploadFile
from requests import Session
from models.dependency import get_db
from services.meme_service import store_meme

router = APIRouter()

@router.post("/")
async def create_meme(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:

        await store_meme(file, db)
    
    except Exception as e:
        print(f"error: {e}")