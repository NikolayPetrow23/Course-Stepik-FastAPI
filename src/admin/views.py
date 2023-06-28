from sqladmin import ModelView

from src.bookings.models import Bookings
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms
from src.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [column.name for column in Bookings.__table__.c]
       # + [Bookings.user]
       # + [Bookings.room]
    #)
    # column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Бронь"
    name_plural = "Бронирования"
    icon = "fa-solid fa-file-pen"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [column.name for column in Hotels.__table__.c]# + [Hotels.room]
    # column_details_exclude_list = [Users.hashed_password]
    # can_delete = False
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [column.name for column in Rooms.__table__.c]# + [Rooms.hotel]
    # column_details_exclude_list = [Users.hashed_password]
    # can_delete = False
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
