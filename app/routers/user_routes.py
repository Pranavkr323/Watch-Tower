from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.user_crud import create_user, update_password, update_user, verify_user,  get_user_by_email, get_user_by_username
from app.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from app.utils.jwt import create_access_token
from app.schemas.user_schema import UserLoginResponse, UserRegisterResponse, UserOut, UserRegister, UserLogin, UserUpdate, PasswordUpdate
from app.models import User

router = APIRouter(
    prefix= "/user",
    tags=["User"]
)

@router.post("/register",
             response_model= UserRegisterResponse,
             status_code= status.HTTP_201_CREATED)

def register_user(userdata: UserRegister, db: Session = Depends(get_db)):
    new_user = create_user(db, userdata)
    if new_user is None:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            detail= "User already exists! Please Login")

    return new_user

@router.post("/login",
             response_model= UserLoginResponse,
             status_code= status.HTTP_200_OK)
def login_user(userdata: UserLogin, db: Session = Depends(get_db)):
    user = verify_user(db, userdata)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password!")
    token = create_access_token({"sub": str(user.user_id)})
    data = {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
        "access_token": token,
        "token_type": "bearer"
    }
    return data

@router.get("/{username}",
            response_model= UserOut)
def get_profile(username: str, current_user: User = Depends(get_current_user)):
    if username != current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= "You can only access your own profile!")
    return current_user

@router.patch("/{username}",
              response_model= UserOut)
def update_user_profile(username: str,
                data: UserUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    if username != current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= "You can only change your own profile!")

    if data.email is not None and data.email != current_user.email:
        existing_user = get_user_by_email(db, data.email)
        if existing_user is not None:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= "Email alread in use")

    if data.username is not None and data.username != current_user.username:
        existing_user = get_user_by_username(db, data.username)
        if existing_user is not None:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= "username alread in use")
    return update_user(db, current_user, data)

@router.patch("/{username}/password")
def change_password(data: PasswordUpdate,
                    username: str,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):

    if username != current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= "You can only change your own password!")

    updated_user = update_password(db, data, current_user)

    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Current password is incorrect")

    return {"message": "Password updated successfully"}
