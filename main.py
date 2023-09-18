from fastapi import Depends, FastAPI, HTTPException, UploadFile, Response
from sqlalchemy.orm import Session

from schemas import UserCreate, User
from crud import create, get_user, get_users, create_photo
import models
from database import SessionLocal, engine
from lib.face_match import FaceMatch
from numpy import array
from PIL import Image
from base64 import b64encode, b64decode
from io import BytesIO

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create(db=db, user=user)


@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)

    return users


@app.post("/users/check-face")
def check_face(
    file: UploadFile, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    users = read_users(skip, limit, db)

    if not len(users) > 0:
        return Response("Users list is empty!", status_code=400)

    for user in users:
        if not user.img_string:
            return Response("User does not have an image!", status_code=400)

        encoded_file = b64encode(file.file.read())
        decoded_file = b64decode(encoded_file)

        decoded_image = b64decode(user.img_string)

        image_file = Image.open(BytesIO(decoded_file))
        user_file = Image.open(BytesIO(decoded_image))

        image_arr = array(image_file)
        user_img_arr = array(user_file)

        result = FaceMatch.match(image_arr, user_img_arr)

        if int(result) == 1:
            return Response("Faces match!", status_code=202)
        else:
            return Response("Face did not match with any user", status_code=404)


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@app.post("/users/{id}/photo/")
def create_user_photo(file: UploadFile, id: int, db: Session = Depends(get_db)):
    read_user(id, db)

    create_photo(db=db, id=id, file=file)
