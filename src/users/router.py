from fastapi import APIRouter, Depends, Response

from src.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from src.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from src.users.dao import UsersDAO
from src.users.dependencies import get_current_user
from src.users.models import Users
from src.users.schemas import SUserRegisterOrAuth

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register")
async def register_user(user_data: SUserRegisterOrAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add_data(email=user_data.email, hashed_password=hashed_password)


@router.post("/authenticated")
async def authenticated(response: Response, user_data: SUserRegisterOrAuth):
    user = await authenticate_user(user_data.email, user_data.password)

    if user:
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("bookings_access_token", access_token, httponly=True)
        return access_token

    raise IncorrectEmailOrPasswordException


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("bookings_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
