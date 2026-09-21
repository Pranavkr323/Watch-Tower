from app.database import SessionLocal
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.jwt import verify_token
from sqlalchemy import select
from app.models import User

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

security = HTTPBearer()
def get_current_user(secrets: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)):

    token = secrets.credentials
    claims = verify_token(token)
    user_ID = int(claims['sub'])
    statement = select(User).where(User.user_id == user_ID)
    user = db.execute(statement).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "User Not Found")
    return user

