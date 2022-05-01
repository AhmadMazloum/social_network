from turtle import title
from certifi import contents
from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World!"}

@app.get("/posts")
async def get_posts():
    return{"posts" : "total_posts"}

@app.post("/create_post")
async def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post" : f"title: {payload['title']} content: {payload['content']}"}
