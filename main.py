import fastapi
import uvicorn
from fastapi import FastAPI,Body,Depends
from app.model import PostSchema
from app.model import PostSchema,UserLoginSchema,UserSchema
from app.auth.jwt_handler import signJWT


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
  

  #5User Signup[Create a new User ]
@app.post("/user/signup",tags=["user"])
def user_signup(user: UserSchema=Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data:UserLoginSchema):
    for user in users:
        if user.email==data.email and user.password==data.password:
            return True
        return False
    
@app.post("/user.login",tags=["user"])
def user_login(user:UserLoginSchema=Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error":"Invalid Login Details!"
        }
