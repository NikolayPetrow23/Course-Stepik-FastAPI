from datetime import date

from sqlalchemy import func, select

from src.dao.base import BaseDAO
from src.bookings.models import Bookings
from src.database import async_session_maker
from src.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_hotels_in_rooms_all(
        cls, hotel_id: int, date_from: date, date_to: date
    ):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(hotel_id=hotel_id)
            result = await session.execute(query)
            res = result.mappings().all()

            results = []

            for obj in res:
                room_id = obj["id"]
                count = await cls.find_bookings_count_by_room(room_id)
                total_days = (date_to - date_from).days

                obj_dict = dict(obj)
                obj_dict["total_price"] = obj_dict["price"] * total_days
                obj_dict["room_available"] = obj_dict["quantity"] - count
                if obj_dict["room_available"] > 0:
                    results.append(obj_dict)

            return results

    @classmethod
    async def find_bookings_count_by_room(cls, room_id: int):
        async with async_session_maker() as session:
            query = select(func.count()).where(Bookings.room_id == room_id)
            result = await session.execute(query)
            count = result.scalar()
            return count
