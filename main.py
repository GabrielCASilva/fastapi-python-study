from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    # to validate payload post content
    title: str
    category: str
    content: str
    author: str
    published: bool = True  # optional field with default value
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "welcome to my api!!!"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/posts")
def post_posts(payload: Post):
    post = payload.dict()
    return {"data": post, "message": "successfully create a new post"}
