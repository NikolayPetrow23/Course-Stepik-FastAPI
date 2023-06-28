from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from src.config import settings
from src.exceptions import (IncorrectTokenException, TokenAbsentException,
                            TokenExpiredException, UserIsNotPresentException)
from src.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("bookings_access_token")
    if token:
        return token

    raise TokenAbsentException


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenException

    expire: str = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
