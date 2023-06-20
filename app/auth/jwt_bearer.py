from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def _init_(self,auto_Error:bool=True):
        super(jwtBearer,self)._init_(auto_Error=auto_Error)

    async def _call_(self,request: Request):
        credentials: HTTPAuthorizationCredentials=await super(jwtBearer,self)._call_(request)
        if credentials:
            if not credentials.scheme=="Bearer":
                raise.HTTPException(status_code-403,details="Invalid or Expired Token")
            return credentials.credentials
    
        else:
            raise HTTPException(status_code=403,details="Invalid or expired Token")

    def verify_jwt(self,jwtokenLstr):
        isTokenValid:bool=False 
        payload=decodeJWT(jwtoken)
        if payload:
            isTokenValid=True
        return isTokenValid