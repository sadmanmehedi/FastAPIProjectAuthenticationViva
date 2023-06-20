import fastapi
import uvicorn
from fastapi import FastAPI,Body,Depends
from app.model import PostSchema
from app.model import PostSchema,UserLoginSchema,UserSchema
from app.auth.jwt_handler import signJWT
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException


# MongoDB connection settings
MONGODB_URL = "mongodb+srv://admin:admin@cluster0.lb7qjfv.mongodb.net/Authentication"
DATABASE_NAME = "Authentication"

# Create a MongoDB client
client = AsyncIOMotorClient("mongodb+srv://admin:admin@cluster0.lb7qjfv.mongodb.net/Authentication")

# Get a reference to the database
db = client["Authentication"]

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
@app.get("/posts", tags=["posts"])
async def get_posts():
    posts = await db.posts.find().to_list(length=None)
    return {"data": posts}


#3Get single Posts aboout ID
@app.get("/posts/{id}", tags=["posts"])
async def get_one_post(id: int):
    post = await db.posts.find_one({"id": id})
    if post:
        return {"data": post}
    return {"error": "Post with this ID does not exist!"}

#4 Post a blog Post[A handler for creating a Post]
@app.post("/posts", tags=["posts"])
async def add_post(post: PostSchema):
    post_dict = post.dict()
    post_dict["id"] = len(posts) + 1
    await db.posts.insert_one(post_dict)
    return {"info": "Post Added!"}
  

  #5User Signup[Create a new User ]
@app.post("/user/signup", tags=["user"])
async def user_signup(user: UserSchema = Body(default=None)):
    users_collection = db.users
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    await users_collection.insert_one(user.dict())
    return signJWT(user.email)

async def check_user(data: UserLoginSchema):
    users_collection = db.users
    user = await users_collection.find_one({"email": data.email, "password": data.password})
    return user is not None

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(default=None)):
    if await check_user(user):
        return signJWT(user.email)
    else:
        return {"error": "Invalid Login Details!"}