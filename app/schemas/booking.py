from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.schemas.bike import Bike
from app.schemas.common import PaginatedQuery, SingleTableModel


class Booking(SingleTableModel):
    id: str
    user_id: str
    bike_id: str
    booking_date: date

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class BookingsForBike(BaseModel):
    bike: Bike
    bookings: list[Booking]


class GetBookingsForBikeQuery(BaseModel):
    bike_id: str


class GetBookingsForUserQuery(PaginatedQuery):
    user_id: str


class GetBookingDetailQuery(BaseModel):
    bike_id: str
    booking_id: str
