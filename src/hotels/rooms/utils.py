# from sqlalchemy import select, func
#
# from src.bookings.models import Bookings
# from src.database import async_session_maker
#
#
# async def find_hotels_in_rooms_all(room_id: int):
#     async with async_session_maker() as session:
#         query = select(Bookings.__table__.columns).filter_by(room_id=room_id)
#         count_query = select(func.count()).select_from(query.alias())
#         result = await session.execute(count_query)
#         count = result.scalar()
#         # results = [count]
#         return count
