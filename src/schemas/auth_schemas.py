from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenCreate(BaseModel):
    user_id: int
    access_token: str
