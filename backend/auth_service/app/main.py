from fastapi import FastAPI
from config import settings
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Auth Service is running"}
