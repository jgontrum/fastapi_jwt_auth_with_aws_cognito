import os

import requests
from dotenv import load_dotenv

from app.JWTBearer import JWKS

load_dotenv()  # Automatically load environment variables from a '.env' file.

jwks = JWKS.parse_obj(
    requests.get(
        f"https://cognito-idp.{os.environ.get('COGNITO_REGION')}.amazonaws.com/"
        f"{os.environ.get('COGNITO_POOL_ID')}/.well-known/jwks.json"
    ).json()
)
