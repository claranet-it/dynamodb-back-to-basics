from typing import Optional, Protocol

from app.exceptions.booking_exceptions import DeleteBookingException
from app.libs import DynamoDBResourceDependency
from app.schemas.booking import Booking, DeleteBookingCommand


class DeleteBookingUseCase(Protocol):
    def __call__(self, DeleteBookingCommand) -> None: ...


def delete_booking(
    dynamodb_resource: DynamoDBResourceDependency,
):
    async def _delete_booking(
        command: DeleteBookingCommand,
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

        response = table.delete_item(
            Key={
                "pk": pk_value,
                "sk": sk_value,
            }
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise DeleteBookingException("Failed to delete booking")

        return Booking(**result["Items"][0])

    return _delete_booking
