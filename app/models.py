from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    # created_at = Column()
    # upddated_at = Column()
    id_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("user")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Likes(Base):
    __tablename__ = "likes"

    id_user = Column(Integer, ForeignKey("user.id"), primary_key=True)
    id_post = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    user = relationship("users")
    post = relationship("posts")
