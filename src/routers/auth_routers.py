from fastapi import Depends, HTTPException, status, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta

from ..crud.auth_crud import get_user_by_username, create_user, save_token, delete_tokens_by_user_id
from ..documentations.base_documentations import not_authenticated_doc
from ..services.auth_services import authenticate_user, create_access_token, get_current_user
from ..schemas import auth_schemas
from ..utils import get_db

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post("/register",
             response_model=auth_schemas.UserRead,
             status_code=status.HTTP_201_CREATED,
             responses={
                 201: {
                     "description": "Register successful",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "username": "johndoe",
                             }
                         }
                     }
                 },
                 409: {
                     "description": "Username already exists.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Username already exists."}
                         }
                     }
                 },
                 422: {
                     "description": "Invalid request body",
                     "content": {
                         "application/json": {
                             "examples": {
                                 "Short password": {
                                     "value": {
                                         "detail": "Password must be at least 8 characters."
                                     }
                                 },
                                 "Password confirmation mismatch": {
                                     "value": {
                                         "detail": "Password confirmation does not match."
                                     }
                                 },
                             }
                         }
                     }
                 },
             })
def register_user(
        user: Annotated[
            auth_schemas.UserCreate,
            Body(
                example={
                    "username": "johndoe",
                    "password": "secretpassword",
                    "confirm_password": "secretpassword"
                }
            )],
        db: Session = Depends(get_db)
):
    """Username must be unique with minimal password length of 8 characters."""
    existing_user = get_user_by_username(db, user.username)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists.")

    if len(user.password) < 8:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password must be at least 8 characters.")

    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password confirmation does not match.")

    return create_user(db, user)


@router.post("/login",
             responses={
                 200: {
                     "description": "Login successful",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "token",
                                 "token_type": "bearer",
                             }
                         }
                     }
                 },
                 401: {
                     "description": "Invalid credentials",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Incorrect username or password."
                             }
                         }
                     }
                 },
             })
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
) -> auth_schemas.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    token_create = auth_schemas.TokenCreate(user_id=user.id, access_token=access_token)
    save_token(db, token_create)

    return auth_schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/logout",
             responses={
                 200: {
                    "description": "Logged out successfully.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Logged out successfully."
                            }
                        }
                    }
                 },
                 401: not_authenticated_doc
             })
def logout(current_user: Annotated[auth_schemas.UserRead, Depends(get_current_user)], db: Session = Depends(get_db)):
    delete_tokens_by_user_id(db, current_user.id)

    return {"detail": "Logged out successfully."}


@router.get("/me",
            response_model=auth_schemas.UserRead,
            responses={
                200: {
                    "description": "Returns the name and id of the current user.",
                    "content": {
                        "application/json": {
                            "example": {
                                "id": 1,
                                "username": "johndoe",
                            }
                        }
                    }
                },
                401: not_authenticated_doc
            })
def read_current_user(
        current_user: Annotated[auth_schemas.UserRead, Depends(get_current_user)],
):
    """
    Function for testing JWT authorization. Returns the name and id of the current user.
    """
    return current_user
