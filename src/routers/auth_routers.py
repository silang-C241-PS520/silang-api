from typing import Annotated

from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import auth_schemas

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=auth_schemas.UserRead,
    responses={
        200: {"description": "Register successful"},
        409: {"description": "Username already exists"},
        # 422: {"description": "Invalid input"},  # TODO masalahnya fast api punya 422 sendiri
    })
async def register(user: auth_schemas.UserCreate):
    # TODO
    return {"message": "Register"}


@router.post(
    "/login",
    response_model=auth_schemas.Token,
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Wrong credential"},
    })
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO
    return {"message": "Login"}


@router.post(
    "/logout",
    responses={
        200: {"description": "Logout successful"},

    })
async def logout():
    # TODO
    return {"message": "Logout"}
