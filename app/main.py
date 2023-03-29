from fastapi import FastAPI, Response, status, HTTPException
from app.schemas import Post, PatchPost
from random import randrange
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


my_posts = []

while True:
    try:
        conn = psycopg2.connect(
            host="",
            database="",
            user="",
            password="",
            cursor_factory=RealDictCursor,
        )
        # RealDictCursor -> column name
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(3)


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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_posts(post: Post):

    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )

    conn.commit()  # push changes to database

    new_post = cursor.fetchone()

    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/posts/{id}")
def patch_post(id: int, post: PatchPost):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    selected_post = cursor.fetchall()

    if selected_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    # transforming tuple in dict
    columns = [col[0] for col in cursor.description]

    dict_post = {}
    for i in range(len(columns)):
        dict_post[columns[i]] = selected_post[0][columns[i]]

    # see with value the client sand to api and apply in dict_post
    for key, value in post.dict().items():
        if value:
            dict_post[key] = value

    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s, updated_at = %s WHERE id = %s""",
        (
            dict_post["title"],
            dict_post["content"],
            dict_post["published"],
            str(date.today().strftime("%d/%m/%Y")),
            str(id),
        ),
    )

    conn.commit()

    return {"message": "post was successfully patched"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    selected_post = cursor.fetchone()

    if selected_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s, updated_at = %s WHERE id = %s""",
        (
            post.title,
            post.content,
            post.published,
            str(date.today().strftime("%d/%m/%Y")),
            str(id),
        ),
    )

    conn.commit()

    return {"message": "post was successfully update"}
