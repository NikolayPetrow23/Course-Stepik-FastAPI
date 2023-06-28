from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from fastapi import status
from fastapi_versioning import version

from src.bookings.dao import BookingDAO
from src.bookings.schemas import SNewBooking
from src.exceptions import RoomCannotBeBooked
from src.tasks.tasks import send_booking_confirmation_email
from src.users.dependencies import get_current_user
from src.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@version(1)
async def get_test_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)


@router.post("/add_booking", status_code=201)
@version(1)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add_booking(user.id, room_id, date_from, date_to)

    if not booking:
        raise RoomCannotBeBooked

    booking_dict = parse_obj_as(SNewBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_202_ACCEPTED)
@version(1)
async def del_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingDAO.del_booking(id=booking_id, user_id=user.id)


@router.delete("/{booking_id}", status_code=status.HTTP_202_ACCEPTED)
@version(2)
async def del_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingDAO.del_booking(id=booking_id, user_id=user.id)
