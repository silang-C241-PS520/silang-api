from sqlalchemy.orm import Session

from ..schemas import auth_schemas
from ..models import auth_models
from ..utils import pwd_context

def create_user(db: Session, user: auth_schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = auth_models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return auth_schemas.UserRead(id=db_user.id, username=db_user.username)

def get_user_by_username(db: Session, username: str):
    return db.query(auth_models.User).filter(auth_models.User.username == username).first()

def save_token(db: Session, token: auth_schemas.TokenCreate):
    token = auth_models.Token(user_id=token.user_id, access_token=token.access_token)
    db.add(token)
    db.commit()

def get_token_by_user_id(db: Session, user_id: int):
    return db.query(auth_models.Token).filter(auth_models.Token.user_id == user_id).first()

def get_access_token(db: Session, access_token: str):
    return db.query(auth_models.Token).filter(auth_models.Token.access_token == access_token).first()

def delete_tokens_by_user_id(db: Session, user_id: int):
    db.query(auth_models.Token).filter(auth_models.Token.user_id == user_id).delete()
    db.commit()
