from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate, CheckFace


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email, img_bin=user.img_bin, img_mime_type=user.img_mime_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def check_face(db: Session, data: CheckFace):
    
