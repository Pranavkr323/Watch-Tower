from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user_schema import UserRegister, UserLogin, UserUpdate, PasswordUpdate
from app.utils.password import hash_password, verify_password

def create_user(db: Session,
                data: UserRegister):
    user = get_user_by_email(db, data.email)
    if user is not None:
        return None

    new_user = User(
        email = data.email,
        username = data.username,
        hashed_password = hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_email(db: Session,
                      email: str):
    statement = select(User).where(User.email == email)
    return db.execute(statement).scalar_one_or_none()


def get_user_by_username(db: Session,
                      username: str):
    statement = select(User).where(User.username == username)
    return db.execute(statement).scalar_one_or_none()

def verify_user(db: Session,
                data: UserLogin):
    user = get_user_by_email(db, data.email)
    if user is None:
        return None

    if verify_password(plain_password=data.password,
                       hashed_password= user.hashed_password):
        return user
    return None

def update_user(db: Session,
                user: User,
                data: UserUpdate,
                ):
    if data.email is not None:
        user.email = data.email

    if data.username is not None:
        user.username = data.username

    db.commit()
    db.refresh(user)
    return user

def update_password(db: Session,
                    password: PasswordUpdate,
                    user: User):

    if not verify_password(password.current_password, user.hashed_password):
        return None

    user.hashed_password = hash_password(password.new_password)
    db.commit()
    db.refresh(user)
    return user

