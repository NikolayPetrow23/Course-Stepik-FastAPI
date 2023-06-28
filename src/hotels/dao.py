from datetime import date

from sqlalchemy import func, select

from src.dao.base import BaseDAO
from src.bookings.models import Bookings
from src.database import async_session_maker
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_in_location_all(cls, location: str, date_from: date, date_to: date):
        booked_room = (
            select(
                Bookings.room_id, func.count(Bookings.room_id).label("count_bookings")
            )
            .where((Bookings.date_to >= date_to) & (Bookings.date_from <= date_from))
            .group_by(Bookings.room_id)
            .cte("booked_room")
        )

        rooms = (
            select(
                Rooms,
                (Rooms.quantity - booked_room.c.count_bookings).label("room_available"),
            )
            .join(booked_room, booked_room.c.room_id == Rooms.id, isouter=True)
            .where(Rooms.id == booked_room.c.room_id)
            .group_by(Rooms.id, booked_room.c)
            .cte("rooms")
        )

        async with async_session_maker() as session:
            query_hotels = (
                select(
                    cls.model.__table__.columns,
                    (
                        cls.model.rooms_quantity - func.count(rooms.c.room_available)
                    ).label("room_available"),
                )
                .join(rooms, rooms.c.hotel_id == cls.model.id, isouter=True)
                .where(
                    cls.model.location.like(f"%{location}%")
                )
                .group_by(cls.model.id, rooms.c.hotel_id)
            )

            count_bookings = await session.execute(query_hotels)
            result = count_bookings.mappings().all()
            return result
