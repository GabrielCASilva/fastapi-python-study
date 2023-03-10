from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "welcome to my api!!!"}


@app.get("/posts")
def get_posts():
    return {"data": "This is yout posts"}


@app.post("/posts")
def post_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
