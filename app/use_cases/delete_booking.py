from typing import Annotated, Optional, Protocol

from fastapi import Depends

from app.exceptions.booking_exceptions import DeleteBookingException
from app.libs.aws import DynamoDBResourceDependency
from app.schemas.booking import Booking, DeleteBookingCommand, GetBookingDetailQuery
from app.use_cases.get_booking_detail import GetBookingDetailDependency


class DeleteBookingUseCase(Protocol):
    def __call__(self, command: DeleteBookingCommand) -> Optional[Booking]: ...


def delete_booking(
    dynamodb_resource: DynamoDBResourceDependency,
    get_booking_use_case: GetBookingDetailDependency,
):
    async def _delete_booking(
        command: DeleteBookingCommand,
    ) -> Optional[Booking]:
        table = dynamodb_resource.Table("booking")

        pk_value = f"BIKE#{command.bike_id}"
        sk_value = f"BOOKING#{command.booking_id}"

        booking = await get_booking_use_case(
            GetBookingDetailQuery(
                bike_id=command.bike_id,
                booking_id=command.booking_id,
            )
        )

        if not booking:
            return None

        response = table.delete_item(
            Key={
                "pk": pk_value,
                "sk": sk_value,
            }
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise DeleteBookingException("Failed to delete booking")

        return booking

    return _delete_booking


DeleteBookingDependency = Annotated[DeleteBookingUseCase, Depends(delete_booking)]
