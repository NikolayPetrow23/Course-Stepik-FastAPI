from datetime import date

from sqlalchemy import case, func, select

from src.dao.base import BaseDAO
from src.bookings.models import Bookings
from src.database import async_session_maker
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_in_location_all(cls, location: str, date_from: date, date_to: date):
        count_bookings = (
            select(
                Bookings.room_id, func.count(Bookings.room_id).label("room_available")
            )
            .join(Rooms, Bookings.room_id == Rooms.id)
            .where((Bookings.date_to >= date_to) & (Bookings.date_from <= date_from))
            .group_by(Bookings.room_id)
            .cte("count_bookings")
        )

        room_available = func.sum(count_bookings.c.room_available)

        query = (
            select(
                cls.model.__table__.columns,
                case(
                    (room_available == None, Hotels.rooms_quantity),
                    else_=Hotels.rooms_quantity - room_available,
                ).label("room_available"),
            )
            .join(count_bookings, Hotels.id == count_bookings.c.room_id, isouter=True)
            .where(cls.model.location.like(f"%{location}%"))
            .group_by(cls.model.id, Hotels.rooms_quantity)
        )

        async with async_session_maker() as session:
            # result = await session.execute(query_count_bookings_in_hotel_id)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_id(cls, hotel):
        pass
