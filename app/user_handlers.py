from fastapi import APIRouter, Depends

from app.auth import get_current_user

router = APIRouter()


@router.get("/test")
async def test(username: str = Depends(get_current_user)):
    return {"username": username}
