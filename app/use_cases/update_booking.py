from typing import Annotated, Optional, Protocol

from fastapi import Depends

from app.libs.aws import DynamoDBResourceDependency
from app.schemas.booking import Booking, GetBookingDetailQuery, UpdateBookingCommand
from app.use_cases.get_booking_detail import GetBookingDetailDependency


class UpdateBookingUseCase(Protocol):
    def __call__(self, UpdateBookingCommand) -> None: ...


def update_booking(
    dynamodb_resource: DynamoDBResourceDependency,
    get_booking_use_case: GetBookingDetailDependency,
) -> UpdateBookingUseCase:
    async def _update_booking(
        command: UpdateBookingCommand,
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

        table.update_item(
            Key={"pk": pk_value, "sk": sk_value},
            UpdateExpression="SET user_id = :user_id, booking_date = :booking_date",
            ExpressionAttributeValues={
                ":user_id": command.user_id,
                ":booking_date": command.booking_date.strftime("%Y-%m-%d"),
            },
        )

        booking.update(command)

        return booking

    return _update_booking


UpdateBookingDependency = Annotated[UpdateBookingUseCase, Depends(update_booking)]
