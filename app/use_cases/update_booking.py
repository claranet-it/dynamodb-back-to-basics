from typing import Optional, Protocol

from app.libs import DynamoDBResourceDependency
from app.schemas.booking import Booking, UpdateBookingCommand


class UpdateBookingUseCase(Protocol):
    def __call__(self, UpdateBookingCommand) -> None: ...


def update_booking(
    dynamodb_resource: DynamoDBResourceDependency,
):
    async def _update_booking(
        command: UpdateBookingCommand,
    ) -> Optional[Booking]:
        table = dynamodb_resource.Table("booking")

        pk_value = f"BIKE#{command.bike_id}"
        sk_value = f"BOOKING#{command.booking_id}"

        query_params = {
            "KeyConditionExpression": "pk = :pk AND sk = :sk",
            "ExpressionAttributeValues": {":pk": pk_value, ":sk": sk_value},
        }

        result = table.query(**query_params)

        if not result["Items"]:
            return None

        table.update_item(
            Key={"pk": pk_value, "sk": sk_value},
            UpdateExpression="SET user_id = :user_id, booking_date = :booking_date",
            ExpressionAttributeValues={
                ":user_id": command.user_id,
                ":booking_date": command.booking_date.strftime("%Y-%m-%d"),
            },
        )

        booking_data = {
            **result["Items"][0],
            "user_id": command.user_id,
            "booking_date": command.booking_date.strftime("%Y-%m-%d"),
        }

        return Booking(**booking_data)

    return _update_booking
