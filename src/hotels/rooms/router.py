from datetime import date

from fastapi import APIRouter

from src.hotels.rooms.dao import RoomDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели и номера"],
)


@router.get("/{hotel_id}/rooms")
async def get_in_hotel_rooms(hotel_id: int, date_from: date, date_to: date):
    return await RoomDAO.find_hotels_in_rooms_all(hotel_id, date_from, date_to)
