from typing import Annotated

from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.auth_schemas import UserCreate, UserRead, Token

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRead,
    responses={
        200: {"description": "Register successful"},
        409: {"description": "Username already exists"},
        # 422: {"description": "Invalid input"},  # TODO masalahnya fast api punya 422 sendiri
    })
async def register(user: UserCreate):
    # TODO
    return UserRead(id=1, username=user.username)


@router.post(
    "/login",
    response_model=Token,
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Wrong credential"},
    })
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO
    return Token(access_token="fake_token", token_type="bearer")


@router.post(
    "/logout",
    responses={
        200: {"description": "Logout successful"},

    })
async def logout():
    # TODO
    return {"message": "Logout successful"}
