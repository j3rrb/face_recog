from pydantic import BaseModel
from typing import Annotated

from fastapi import File


class UserBase(BaseModel):
    name: str


class CheckFace(BaseModel):
    img: Annotated[bytes, File()]
    target: Annotated[bytes, File()]


class UserCreate(UserBase):
    name: str
    img_bin: Annotated[bytes, File()]
    img_mime_type: str


class User(UserBase):
    id: int
    name: str
    img_bin: Annotated[bytes, File()]
    img_mime_type: str

    class Config:
        orm_mode = True
