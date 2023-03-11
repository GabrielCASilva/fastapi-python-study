from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
from datetime import date


app = FastAPI()


class Post(BaseModel):
    # to validate payload post content
    id: int = 0
    title: str
    category: str
    content: str
    author: str
    published: bool = True  # optional field with default value
    rating: Optional[int] = None
    created_at: str = "0"


my_posts = []


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/")
def root():
    return {"message": "welcome to my api!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {f"{id}": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_posts(payload: Post):
    post_dict = payload.dict()

    post_dict["created_at"] = date.today().strftime("%d/%m/%Y")
    post_dict["id"] = randrange(0, 1000000)

    my_posts.append(post_dict)

    return {"data": post_dict}
