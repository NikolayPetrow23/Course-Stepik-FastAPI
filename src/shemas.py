from datetime import date

from pydantic import BaseModel


class Booking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Hotel(BaseModel):
    address: str
    name: str
    stars: int
