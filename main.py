from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta
from enum import Enum

from database import engine
from authentication import models, schemas
from authentication.crud import get_user_by_username, create_user
from authentication.utils import authenticate_user, create_access_token, get_current_user
from utils import get_db

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations related to the authentication and authorization of users.",
    },
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Silang", openapi_tags=tags_metadata)

class Tags(Enum):
    authentication = "Authentication"


@app.post("/register", response_model=schemas.UserRead, tags=[Tags.authentication])
async def register_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db), ):
    existing_user = get_user_by_username(db, user.username)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered.")

    if len(user.password) < 8 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters.")

    if user.password != user.confirm_password :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password confirmation does not match.")

    response.status_code = status.HTTP_201_CREATED
    return create_user(db, user)


@app.post("/login", tags=[Tags.authentication])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> schemas.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/me", response_model=schemas.UserRead, tags=[Tags.authentication])
async def read_current_user(
    current_user: Annotated[schemas.UserRead, Depends(get_current_user)],
):
    """
    Function for testing JWT authorization. Returns the name and id of the current user.
    """
    return current_user
