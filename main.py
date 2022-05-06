import re
from typing import Optional
from urllib.request import HTTPErrorProcessor
from fastapi import  FastAPI, HTTPException, status
from pydantic import BaseModel
import random

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "Title of post 1", "content" : "content of post 1", "id": 1} , 
{"title": "fav food", "content" : "pizza and burger", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if(id == p['id']):
            return i


@app.get("/")
async def root():
    return {"message" : "Hello World!"}

@app.get("/posts")
async def get_posts():
    return{"posts" : my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict() 
    post_dict['id'] = random.randint(0,100000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/{id}")
def get_post(id : int ):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return{"post" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "no id for this")
    post = my_posts.pop(index)
    return {"detail" : post}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "no id for this")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{'updated post' : post_dict}
    