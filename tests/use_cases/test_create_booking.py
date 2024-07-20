from unittest.mock import MagicMock

import pytest

from app.exceptions.booking_exceptions import CreateBookingException
from app.use_cases.create_booking import create_booking


@pytest.mark.asyncio
async def test_create_booking_ok(create_booking_command):
    dynamodb_resource_mock = MagicMock()
    table_mock = MagicMock()
    table_mock.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    dynamodb_resource_mock.Table.return_value = table_mock

    use_case = create_booking(dynamodb_resource=dynamodb_resource_mock)

    command = create_booking_command()

    booking = await use_case(command)

    assert booking.id is not None
    assert booking.user_id == command.user_id
    assert booking.bike_id == command.bike_id
    assert booking.booking_date == command.booking_date

    dynamodb_resource_mock.Table.assert_called_once_with("booking")
    table_mock.put_item.assert_called_once_with(
        Item={
            "id": booking.id,
            "bike_id": booking.bike_id,
            "user_id": booking.user_id,
            "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
            "entity": "BOOKING",
            "pk": "BIKE#099",
            "sk": f"BOOKING#{booking.id}",
            "gsi1_pk": "USER#601",
            "gsi1_sk": f"BOOKING#{booking.id}",
        }
    )


@pytest.mark.asyncio
async def test_create_booking_error_500(create_booking_command):
    dynamodb_resource_mock = MagicMock()
    table_mock = MagicMock()
    table_mock.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 500}}
    dynamodb_resource_mock.Table.return_value = table_mock

    use_case = create_booking(dynamodb_resource=dynamodb_resource_mock)

    command = create_booking_command()

    with pytest.raises(CreateBookingException):
        await use_case(command)

    dynamodb_resource_mock.Table.assert_called_once_with("booking")
    table_mock.put_item.assert_called_once()
