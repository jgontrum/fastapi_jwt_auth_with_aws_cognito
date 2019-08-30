from fastapi import APIRouter, Depends

from app.JWTBearer import JWTBearer, JWTAuthorizationCredentials
from app.auth import jwks

router = APIRouter()
auth = JWTBearer(jwks)


@router.get("/test")
async def read_users(authorization: JWTAuthorizationCredentials = Depends(auth)):
    user = authorization.claims["username"]
    return {"username": user}
