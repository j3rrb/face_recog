from sqlalchemy.orm import Session
from fastapi import UploadFile, Response
from base64 import b64encode

from models import User
from schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create(db: Session, user: UserCreate):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_photo(db: Session, id: int, file: UploadFile):
    user = get_user(db, id)

    if user == None:
        raise Response("User not found!", status_code=404)

    encoded = b64encode(file.file.read())

    img_string = encoded
    user.img_string = img_string

    db.commit()
    db.refresh(user)
