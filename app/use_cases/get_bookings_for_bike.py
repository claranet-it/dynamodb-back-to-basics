from typing import Annotated, Protocol

from fastapi import Depends

from app.libs import DynamoDBResourceDependency
from app.schemas.bike import Bike
from app.schemas.booking import Booking, BookingsForBike, GetBookingsForBikeQuery


class GetBookingsForBikeUseCase(Protocol):
    def __call__(self, query: GetBookingsForBikeQuery) -> BookingsForBike: ...


def get_bookings_for_bike(dynamodb_resource: DynamoDBResourceDependency):
    async def _get_bookings_for_bike(query: GetBookingsForBikeQuery) -> BookingsForBike:
        table = dynamodb_resource.Table("booking")

        pk_value = f"BIKE#{query.bike_id}"

        query_params = {
            "KeyConditionExpression": "pk = :pk",
            "ExpressionAttributeValues": {":pk": pk_value},
        }

        result = table.query(**query_params)
        if not result["Items"]:
            return None

        bike_item = result["Items"][0]
        booking_items = result["Items"][1:]

        return BookingsForBike(
            bike=Bike(**bike_item), bookings=[Booking(**item) for item in booking_items]
        )

    return _get_bookings_for_bike


GetBookingsForBikeDependency = Annotated[
    GetBookingsForBikeUseCase, Depends(get_bookings_for_bike)
]
