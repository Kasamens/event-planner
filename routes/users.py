from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse
from auth.hash_password import HashPassword
from database.connection import get_session
from sqlmodel import select
import logging



user_router = APIRouter(
    tags=["User"]
)

hash_password = HashPassword()


@user_router.post("/signup")
async def sign_user_up(user: User, session=Depends(get_session)) -> dict:

    user_exist = session.query(User).filter(User.email == user.email).first()
    if user_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with email provided exists already."
                
    )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    #await user_database.save(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
            "message": "User created successfully"
    }

@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)) -> dict:
    #user_exist = await User.find_one(User.email == user.username)
    user_exist = session.query(User).filter(User.email == user.username).first()
    # if user_exist:
    #     if hash_password.verify_hash(user.password, user_exist.password):
    #         access_token = create_access_token(
    #             user_exist.email)
    #     return{
    #         "access_token" : access_token,
    #         "token_type" : "Bearer"
    #     }
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "User not found"
    )
   