from fastapi import FastAPI, Response, status, HTTPException
from schemas import Post, PatchPost
from random import randrange
from datetime import date


app = FastAPI()


my_posts = []


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i


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


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(int(id))

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    my_posts.remove(post)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/posts/{id}")
def patch_post(id: int, payload: PatchPost):
    post = payload.dict()
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    for key, value in post.items():
        if value is not None:
            my_posts[index][key] = value

    my_posts[index]["update_at"] = date.today().strftime("%d/%m/%Y")

    return {"message": "post was successfully patched"}
