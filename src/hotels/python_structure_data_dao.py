from datetime import date

from sqlalchemy import select

from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.hotels.models import Hotels
from src.hotels.rooms.dao_python_structure_data import RoomDAO


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_in_location_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).where(
                cls.model.location.like(f"%{location}%")
            )
            result = await session.execute(query)
            hotels = result.mappings().all()
            print(result)

            results = []

            for hotel in hotels:
                hotel_id = hotel["id"]
                count = await RoomDAO.find_hotels_in_rooms_all(
                    hotel_id, date_from, date_to
                )
                room_available = sum([room.get("room_available", 0) for room in count])
                print(room_available)

                hotel = dict(hotel)
                hotel["room_available"] = hotel["rooms_quantity"] - room_available
                if hotel["room_available"] > 0:
                    results.append(hotel)
            return results
