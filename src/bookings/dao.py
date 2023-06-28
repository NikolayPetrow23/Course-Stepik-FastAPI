from datetime import date

from fastapi import status
from sqlalchemy import func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.dao.base import BaseDAO
from src.bookings.models import Bookings
from src.database import async_session_maker, engine
from src.exceptions import BookingNotFound, BookingWrongData
from src.hotels.rooms.models import Rooms
from src.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            query = query.select_from(cls.model).join(
                Rooms, cls.model.room_id == Rooms.id
            )
            query = query.add_columns(
                Rooms.image_id, Rooms.name, Rooms.description, Rooms.services
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def del_booking(cls, **filter_by):
        async with async_session_maker() as session:
            obj = await session.execute(select(cls.model).filter_by(**filter_by))
            booking = obj.scalar()
            if booking:
                await session.delete(booking)
                await session.commit()
                return status.HTTP_202_ACCEPTED

            raise BookingNotFound

    @classmethod
    async def add_booking(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ):
        if date_from >= date_to or (date_to - date_from).days > 30:
            raise BookingWrongData

        try:
            booked_room = (
                select(Bookings)
                .where(
                    (Bookings.room_id == room_id)
                    & (
                            (Bookings.date_from >= date_from) &
                            (Bookings.date_from <= date_to)
                    )
                    & (
                            (Bookings.date_from <= date_from) &
                            (Bookings.date_to > date_from)
                    )
                )
                .cte("booked_room")
            )

            get_room_available = (
                select(
                    (Rooms.quantity - func.count(booked_room.c.room_id)).label(
                        "room_available"
                    )
                )
                .select_from(Rooms)
                .join(booked_room, booked_room.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_room.c.room_id)
            )

            async with async_session_maker() as session:
                print(
                    get_room_available.compile(
                        engine, compile_kwargs={"literal_binds": True}
                    )
                )
                room_available: int = await session.execute(get_room_available)
                room_available: int = room_available.scalar()

                if room_available > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_bookings = (
                        insert(Bookings)
                        .values(
                            user_id=user_id,
                            room_id=room_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(
                            Bookings.id,
                            Bookings.user_id,
                            Bookings.room_id,
                            Bookings.date_from,
                            Bookings.date_to,
                        )
                    )
                    new_booking = await session.execute(add_bookings)
                    await session.commit()
                    return new_booking.mappings().one()

                else:
                    return None
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = f"Database Exception"
            elif isinstance(error, Exception):
                message = f"Unknown Exception {error}"

            message += ": Cannot add booking"

            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(message, extra=extra, exc_info=True)
