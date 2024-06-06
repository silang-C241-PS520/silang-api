from fastapi import FastAPI

from .database import engine
from .models import auth_models
from .routers import auth_routers, translation_routers

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations related to the authentication and authorization of users.",
    },
]

auth_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Silang", openapi_tags=tags_metadata)

app.include_router(auth_routers.router)
app.include_router(translation_routers.router)
