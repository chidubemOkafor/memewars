from fastapi import APIRouter, File, UploadFile
import supabase

router = APIRouter()

@router.post("/")
async def create_meme(file: UploadFile = File(...)):
    contents = await file.read()
    response = supabase.storage.from_("images_bucket").upload(
        f"uploads/{file.filename}", contents
    )

    public_url = supabase.storage.from_("images_bucket").get_public_url(
        f"uploads/{file.filename}"
    )

    return {"url": public_url}