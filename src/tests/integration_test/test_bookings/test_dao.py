from datetime import datetime

from src.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add_booking(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


async def test_crud_booking():
    new_booking = await BookingDAO.add_booking(
        user_id=2,
        room_id=3,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )
    booking_read = await BookingDAO.find_by_id(new_booking.get("id"))
    booking_read_dict = dict(booking_read.__dict__)

    assert new_booking.get("id") == booking_read_dict.get("id")

    await BookingDAO.del_booking(id=new_booking.get("id"))

    booking_read = await BookingDAO.find_by_id(new_booking.get("id"))

    assert booking_read is None
