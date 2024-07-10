from typing import Annotated, Optional, Protocol

from fastapi import Depends

from app.libs.aws import DynamoDBResourceDependency
from app.schemas.booking import (
    Booking,
    GetBookingDetailQuery,
)


class GetBookingDetailUseCase(Protocol):
    def __call__(self, query: GetBookingDetailQuery) -> Optional[Booking]: ...


def get_booking_detail(dynamodb_resource: DynamoDBResourceDependency):
    async def _get_booking_detail(query: GetBookingDetailQuery) -> Optional[Booking]:
        table = dynamodb_resource.Table("booking")

        pk_value = f"BIKE#{query.bike_id}"
        sk_value = f"BOOKING#{query.booking_id}"

        query_params = {
            "KeyConditionExpression": "pk = :pk AND sk = :sk",
            "ExpressionAttributeValues": {":pk": pk_value, ":sk": sk_value},
        }

        result = table.query(**query_params)

        if not result["Items"]:
            return None

        return Booking(**result["Items"][0])

    return _get_booking_detail


GetBookingDetailDependency = Annotated[
    GetBookingDetailUseCase, Depends(get_booking_detail)
]
