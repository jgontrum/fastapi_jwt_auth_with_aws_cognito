from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException

from .auth import get_jwks, verify_jwt
from .exceptions import JWTNoPublicKey
from .user_handlers import router as user_router

load_dotenv()  # Automatically load environment variables from a '.env' file.
app = FastAPI()

jwks = get_jwks()


async def verify_jwk_header(authorization: str = Header("")):
    global jwks

    jwt = authorization.replace("Bearer", "").strip()

    if not jwt:
        raise HTTPException(status_code=401, detail="Not authorized: JWT not found.")

    try:
        is_verified = verify_jwt(jwt, jwks)
    except JWTNoPublicKey:
        raise HTTPException(
            status_code=401, detail=f"Not authorized: No matching public key found."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}.")

    if not is_verified:
        raise HTTPException(
            status_code=401, detail=f"Not authorized: JWT signature invalid."
        )


@app.get("/secure", dependencies=[Depends(verify_jwk_header)])
async def secure() -> bool:
    return True


@app.get("/not_secure")
async def not_secure() -> bool:
    return True


app.include_router(user_router, prefix="/user", dependencies=[Depends(verify_jwk_header)])
