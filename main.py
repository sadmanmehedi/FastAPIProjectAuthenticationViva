import time
import jwt
from fastapi import FastAPI, Body, HTTPException, Depends
from app.model import UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT, decodeJWT
from motor.motor_asyncio import AsyncIOMotorClient


MONGODB_URL = "mongodb+srv://admin:admin@cluster0.nppt6z5.mongodb.net/"
DATABASE_NAME = "Authentication"

client = AsyncIOMotorClient(MONGODB_URL +DATABASE_NAME)

db = client["Authentication"]


users=[]

app=FastAPI()



@app.on_event("startup")
async def startup_db_client():
    # Connect to the MongoDB database when the app starts
    client.get_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    # Close the MongoDB connection when the app shuts down
    client.close()

@app.post("/user/signup", tags=["user"])
async def user_signup(user: UserSchema = Body(default=None)):
    users_collection = db.users
    print(users_collection)
    existing_user = await users_collection.find_one({"email": user.email})
    print(existing_user)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    await users_collection.insert_one(user.dict())

    # Generate access token and refresh token
    tokens = signJWT(user.email)

    return tokens

@app.post("/user/refresh", tags=["user"])
async def refresh_token(refresh_token: str = Body(...)):
    decoded_refresh_token = decodeJWT(refresh_token)

    if not decoded_refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if decoded_refresh_token["expiry"] < time.time():
        raise HTTPException(status_code=401, detail="Refresh token has expired")

    users_collection = db.users
    user = await users_collection.find_one({"email": decoded_refresh_token["userID"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a new access token using the userID from the refresh token
    new_tokens = signJWT(decoded_refresh_token["userID"])

    # Update the user with the new access token in the database
    await users_collection.update_one({"email": decoded_refresh_token["userID"]}, {"$set": new_tokens})

    return new_tokens

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(default=None)):
    users_collection = db.users
    user_data = await users_collection.find_one({"email": user.email, "password": user.password})
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Login Details")

    # Generate access token and refresh token for
    #  the logged-in user
    tokens = signJWT(user.email)

    # Update the user with the generated tokens in the database
    await users_collection.update_one({"email": user.email}, {"$set": tokens})

    return tokens


