from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.schemas.bike import Bike
from app.schemas.common import PaginatedQuery, SingleTableModel


class GetBookingsForBikeQuery(BaseModel):
    bike_id: str


class GetBookingsForUserQuery(PaginatedQuery):
    user_id: str


class GetBookingDetailQuery(BaseModel):
    bike_id: str
    booking_id: str


class CreateBookingPayload(BaseModel):
    user_id: str
    bike_id: str
    booking_date: date

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CreateBookingCommand(CreateBookingPayload):
    pass


class DeleteBookingCommand(BaseModel):
    booking_id: str
    bike_id: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class UpdateBookingPayload(BaseModel):
    user_id: str
    booking_date: date

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class UpdateBookingCommand(UpdateBookingPayload):
    booking_id: str
    bike_id: str


class Booking(SingleTableModel):
    id: str
    user_id: str
    bike_id: str
    booking_date: date

    def update(self, command: UpdateBookingCommand):
        self.user_id = command.user_id
        self.booking_date = command.booking_date

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class BookingsForBike(BaseModel):
    bike: Bike
    bookings: list[Booking]
