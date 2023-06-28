import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    *[(4, "2023-05-01", "2023-05-15", 201)] * 8,
    (4, "2023-05-01", "2023-05-15", 409),
    (4, "2023-05-01", "2023-05-15", 409),
    (3, "2023-05-01", "2023-04-30", 400),
    (3, "2023-05-01", "2023-06-04", 400),
    (3, "2023-05-01", "2023-05-10", 201)
])
async def test_add_add_get_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post("/v1/bookings/add_booking", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code


async def test_get_and_deleted_booking(
    authenticated_ac: AsyncClient
):
    booking_response = await authenticated_ac.get("/v1/bookings")

    for booking in booking_response.json():
        delete_response = await authenticated_ac.delete(f"/v1/bookings/{booking.get('id')}")
        assert delete_response.status_code == 202

    booking_response = await authenticated_ac.get("/v1/bookings")
    assert len(booking_response.json()) == 0
