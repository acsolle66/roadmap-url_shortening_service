from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..settings import AuthConfig
from .models import User
from .schemas import Token, UserCreate, UserResponse
from .security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)

auth = APIRouter(prefix="/auth", tags=["Authentication"])
ACCESS_TOKEN_EXPIRE_MINUTES = AuthConfig.access_token_expire_minutes


@auth.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@auth.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    user = User(
        username=user.username, hashed_password=get_password_hash(user.password)
    )
    await User.insert_one(user)
    await user.sync()
    return user
