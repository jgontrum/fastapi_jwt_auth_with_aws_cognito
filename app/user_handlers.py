from fastapi import APIRouter, Header

from .auth import get_user_from_jwt

router = APIRouter()


@router.get("/test")
async def read_users(authorization: str = Header("")):
    user = get_user_from_jwt(authorization)
    return {"username": user}
