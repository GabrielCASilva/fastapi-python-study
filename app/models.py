from sqlalchemy import Column, Integer
from .database import Base

# post table
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
