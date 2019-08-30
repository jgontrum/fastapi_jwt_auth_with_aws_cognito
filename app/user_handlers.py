from fastapi import APIRouter, Depends
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials

from .auth import get_user_from_jwt

router = APIRouter()
auth = HTTPBearer()


@router.get("/test")
async def read_users(authorization: HTTPAuthorizationCredentials = Depends(auth)):
    user = get_user_from_jwt(authorization.credentials)
    return {"username": user}
