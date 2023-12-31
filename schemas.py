from pydantic import BaseModel


class UserBase(BaseModel):
    name: str

class CheckFace(BaseModel):
    img: str


class UserCreate(UserBase):
    name: str


class User(UserBase):
    id: int
    name: str

    class Config:
        from_attributes = True
