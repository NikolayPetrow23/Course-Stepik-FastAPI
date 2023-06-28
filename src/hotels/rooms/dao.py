from datetime import date

from sqlalchemy import func, literal, select

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
            all_rooms_execute = await session.execute(query)
            all_rooms = all_rooms_execute.mappings().all()

            results = []
            for room in all_rooms:
                room_id = room["id"]

                booked_room = (
                    select(Bookings)
                    .where(
                        (Bookings.room_id == room_id)
                        & (Bookings.date_to >= date_to)
                        & (Bookings.date_from <= date_from)
                    )
                    .cte("booked_room")
                )

                get_room_available = (
                    select(
                        (Rooms.quantity - func.count(booked_room.c.room_id)).label(
                            "room_available"
                        ),
                        (
                            (literal(date_to) - literal(date_from)) * cls.model.price
                        ).label("total_price"),
                    )
                    .select_from(cls.model)
                    .join(
                        booked_room, booked_room.c.room_id == cls.model.id, isouter=True
                    )
                    .where(cls.model.id == room_id)
                    .group_by(cls.model.quantity, booked_room.c.room_id, Rooms.price)
                )

            return results
