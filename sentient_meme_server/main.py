from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, user, owner

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def read_root():
    return {"hello": "world"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(auth.router, prefix="/campaign", tags=["campaign"])
app.include_router(auth.router, prefix="/meme", tags=["meme"])
app.include_router(auth.router, prefix="/profile", tags=["profile"])
app.include_router(owner.router, prefix="/owner",tags=["owner"])