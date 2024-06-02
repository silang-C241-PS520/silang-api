from sqlalchemy.orm import Session

from . import models, schemas
from utils import pwd_context

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.UserRead(id=db_user.id, username=db_user.username)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
