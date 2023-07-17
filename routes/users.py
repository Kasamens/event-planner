from fastapi import APIRouter, HTTPException, status, Depends
from models.users import User, UserSignIn
from auth.hash_password import HashPassword
from database.connection import get_session
from sqlmodel import select
import logging



user_router = APIRouter(
    tags=["User"]
)

hash_password = HashPassword

# 

@user_router.post("/signup")
async def sign_user_up(user: User, session=Depends(get_session)) -> dict:
    statement = select(User)
    users = session.exec(statement)

    if any(u.email == user.email for u in users):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with email provided exists already."
                
    )
    hashed_password = hash_password.create_hash(self="",password=user.password)
    user.password = hashed_password
    #await user_database.save(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
            "message": "User created successfully"
    }

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with email does not exist."
    )
    if user_exist.password == user.password:
        return {
                "message": "User signed in successfully."
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )