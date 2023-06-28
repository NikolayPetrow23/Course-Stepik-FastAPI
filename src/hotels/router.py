import asyncio
from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.hotels.old_dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели и номера"],
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_in_location(location, date_from: date, date_to: date):
    await asyncio.sleep(3)
    return await HotelDAO.find_in_location_all(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    return await HotelDAO.find_by_id(hotel_id)


@router.get("/all_hotels")
async def all_hotels():
    return await HotelDAO.find_all()
