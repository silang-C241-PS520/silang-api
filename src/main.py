from fastapi import FastAPI
from .routers import auth_routers, translation_routers

app = FastAPI()

app.include_router(auth_routers.router)
app.include_router(translation_routers.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}