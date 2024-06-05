from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str

    class Config:
        form_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
