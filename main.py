from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from schemas import UserCreate, User, CheckFace
from crud import create_user, get_user, get_users
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/check-face', response_class=bool):
def check_face(data: CheckFace, db: Session = Depends(get_db)):
    

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)

    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
