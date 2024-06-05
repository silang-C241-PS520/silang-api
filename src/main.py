from fastapi import FastAPI
from src.routers import auth_routers

app = FastAPI()

app.include_router(auth_routers.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}