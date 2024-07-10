from typing import Annotated, Protocol
from uuid import uuid4

from fastapi import Depends

from app.exceptions.booking_exceptions import CreateBookingException
from app.libs.aws import DynamoDBResourceDependency
from app.schemas.bike import GetAvailableBikesQuery
from app.schemas.booking import Booking


class CreateBookingUseCase(Protocol):
    def __call__(self, CreateBookingCommand) -> Booking: ...


def create_booking(
    dynamodb_resource: DynamoDBResourceDependency,
):
    async def _create_booking(
        command: GetAvailableBikesQuery,
    ) -> Booking:
        table = dynamodb_resource.Table("booking")

        booking_id = uuid4()

        item_data = {
            "id": str(booking_id),
            "bike_id": command.bike_id,
            "user_id": command.user_id,
            "booking_date": command.booking_date.strftime("%Y-%m-%d"),
            "entity": "BOOKING",
            "pk": f"BIKE#{command.bike_id}",
            "sk": f"BOOKING#{booking_id}",
            "gsi1_pk": f"USER#{command.user_id}",
            "gsi1_sk": f"BOOKING#{booking_id}",
        }

        response = table.put_item(
            Item=item_data,
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise CreateBookingException("Error creating booking")

        return Booking(**item_data)

    return _create_booking


CreateBookingDependency = Annotated[CreateBookingUseCase, Depends(create_booking)]
