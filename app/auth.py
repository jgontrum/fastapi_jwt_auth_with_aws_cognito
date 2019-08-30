import os
from typing import Dict, List, Optional

import requests
from fastapi import HTTPException
from jose import jwt, jwk
from jose.utils import base64url_decode


class JWTNoPublicKey(Exception):
    pass


JWK = Dict[str, str]
JWKS = Dict[str, List[JWK]]


def get_jwks() -> JWKS:
    return requests.get(
        f"https://cognito-idp.{os.environ.get('COGNITO_REGION')}.amazonaws.com/"
        f"{os.environ.get('COGNITO_POOL_ID')}/.well-known/jwks.json"
    ).json()


def get_hmac_key(token: str, jwks: JWKS) -> Optional[JWK]:
    kid = jwt.get_unverified_header(token).get("kid")
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key


def verify_jwt(token: str, jwks: JWKS) -> bool:
    hmac_key = get_hmac_key(token, jwks)

    if not hmac_key:
        raise JWTNoPublicKey()

    hmac_key = jwk.construct(get_hmac_key(token, jwks))

    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode())

    return hmac_key.verify(message.encode(), decoded_signature)


def get_user_from_jwt(jwt_token: str) -> str:
    try:
        return jwt.get_unverified_claims(jwt_token)["username"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Username not found in JWT.")
