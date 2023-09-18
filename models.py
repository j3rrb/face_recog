from sqlalchemy import Column, Integer, String, LargeBinary

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    img_bin = Column(LargeBinary, nullable=False)
    img_mime_type = Column(String, nullable=False)
