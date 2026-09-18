from joserfc import jwt, jwk
from joserfc.jwt import JWTClaimsRegistry
from app.config import settings
from fastapi import HTTPException, status
from joserfc.errors import ClaimError, JoseError
from datetime import datetime, timezone, timedelta

JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRY_MINUTES = settings.ACCESS_TOKEN_EXPIRY_MINUTES
SECRET_KEY = settings.SECRET_KEY
JWT_KEY = jwk.import_key(SECRET_KEY, "oct")

def create_access_token(data: dict) -> str:
    header = {'alg': JWT_ALGORITHM}
    expiry = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    payload = data.copy()
    payload.update({"exp": expiry})
    return jwt.encode(header, payload, JWT_KEY)

def verify_token(token: str):
    try:
        token_obj = jwt.decode(
            token,
            JWT_KEY,
            algorithms= [JWT_ALGORITHM],
        )

        claim_registy = JWTClaimsRegistry(
            exp = {"essential": True},
            sub = {"essential": True}
        )

        claim_registy.validate(token_obj.claims)
        return dict(token_obj.claims)

    except (JoseError, ClaimError):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Cannot validate Credentials"
        )
