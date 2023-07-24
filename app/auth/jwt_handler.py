#this file is responsible for signing,encoding,decoding and returning JWTS
import time
import jwt 
from decouple import config 

JWT_SECRET = config("secret")
JWT_ALGORITHM=config("algorithm")

#Function returns the generated Tokens(JWTs)
def token_response(token:str):
    return{
    "access token" :token
    }

def signJWT(userID:str):
    payload={
        "userID": userID,
        "expiry":time.time()+600
    }
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    refresh_payload = {
        "userID": userID,
        "expiry": time.time() + 3600  # Set the expiry time for the refresh token (e.g., 1 hour)
    }
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token['expiry'] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None