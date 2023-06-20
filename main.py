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


users=[]

app=FastAPI()

#1Get for testing
@app.get("/",tags=["test"])

def greet():
    return {"Hello":"World!"}

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