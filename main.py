import uvicorn
from fastapi import FastAPI
from app.model import PostSchema

posts=[
    {
        "id":1,
        "title":"penguins",
        "text":"Penguins are a group of aquatic fligtless birds"
    },
    {
        "id":2,
        "title":"tigers",
        "text":"Tigers are the largest living cat species and a members of the genus Panthera"
    },
     {
        "id":3,
        "title":"Koalas",
        "text":"Koala is arboreal herbivoures marsupial native to Australia"
    }
]

users=[]

app=FastAPI()

#1Get for testing
@app.get("/",tags=["test"])

def greet():
    return {"Hello":"World!"}


#2Get Posts
@app.get("/ posts",tags=["posts"])
def get_posts():
    return{"data":posts}


#3Get single Posts aboout ID
@app.get("/posts/{id}",tags=["posts"])
def get_one_post(id: int):
    if id>len(posts):
        return{
            "error":"Posts with this ID does not exist!"
        }
    
    for post in posts:
        if post["id"]==id:
            return{
                "data":post
            }
        

#4 Post a blog Post[A handler for creating a Post]
@app.post("/posts",tags=["posts"])
def add_post(post:PostSchema):
    post.id=len(posts)+1
    posts.append(post.dict())
    return{
        "info":"Post Added!"
    }
  