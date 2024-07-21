from unittest.mock import AsyncMock, MagicMock

import pytest

from app.exceptions.booking_exceptions import DeleteBookingException
from app.schemas.booking import Booking, GetBookingDetailQuery
from app.use_cases.delete_booking import delete_booking


@pytest.mark.asyncio
async def test_delete_booking_ok(delete_booking_command):
    command = delete_booking_command()

    dynamodb_resource_mock = MagicMock()
    table_mock = MagicMock()
    table_mock.delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    dynamodb_resource_mock.Table.return_value = table_mock

    get_booking_use_case_mock = AsyncMock()
    return_booking = Booking(
        **{
            "id": command.booking_id,
            "bike_id": command.bike_id,
            "user_id": "001",
            "booking_date": "2024-07-11",
            "entity": "BOOKING",
            "pk": f"BIKE#{command.bike_id}",
            "sk": f"BOOKING#{command.booking_id}",
            "gsi1_pk": "USER#601",
            "gsi1_sk": f"BOOKING#{command.booking_id}",
        }
    )
    get_booking_use_case_mock.return_value = return_booking

    use_case = delete_booking(
        dynamodb_resource=dynamodb_resource_mock,
        get_booking_use_case=get_booking_use_case_mock,
    )

    booking = await use_case(command)

    assert booking == return_booking

    dynamodb_resource_mock.Table.assert_called_once_with("booking")

    table_mock.delete_item.assert_called_once_with(
        Key={
            "pk": f"BIKE#{command.bike_id}",
            "sk": f"BOOKING#{command.booking_id}",
        }
    )

    get_booking_use_case_mock.assert_awaited_once_with(
        GetBookingDetailQuery(
            bike_id=command.bike_id,
            booking_id=command.booking_id,
        )
    )


@pytest.mark.asyncio
async def test_delete_booking_not_found(delete_booking_command):
    command = delete_booking_command()

    dynamodb_resource_mock = MagicMock()
    table_mock = MagicMock()
    table_mock.delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 500}}
    dynamodb_resource_mock.Table.return_value = table_mock

    get_booking_use_case_mock = AsyncMock()
    get_booking_use_case_mock.return_value = None

    use_case = delete_booking(
        dynamodb_resource=dynamodb_resource_mock,
        get_booking_use_case=get_booking_use_case_mock,
    )

    booking = await use_case(command)

    assert booking is None

    dynamodb_resource_mock.Table.assert_called_once_with("booking")

    table_mock.delete_item.assert_not_called()

    get_booking_use_case_mock.assert_awaited_once_with(
        GetBookingDetailQuery(
            bike_id=command.bike_id,
            booking_id=command.booking_id,
        )
    )


@pytest.mark.asyncio
async def test_delete_booking_error(delete_booking_command):
    command = delete_booking_command()

    dynamodb_resource_mock = MagicMock()
    table_mock = MagicMock()
    table_mock.delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 500}}
    dynamodb_resource_mock.Table.return_value = table_mock

    get_booking_use_case_mock = AsyncMock()
    return_booking = Booking(
        **{
            "id": command.booking_id,
            "bike_id": command.bike_id,
            "user_id": "001",
            "booking_date": "2024-07-11",
            "entity": "BOOKING",
            "pk": f"BIKE#{command.bike_id}",
            "sk": f"BOOKING#{command.booking_id}",
            "gsi1_pk": "USER#601",
            "gsi1_sk": f"BOOKING#{command.booking_id}",
        }
    )
    get_booking_use_case_mock.return_value = return_booking

    use_case = delete_booking(
        dynamodb_resource=dynamodb_resource_mock,
        get_booking_use_case=get_booking_use_case_mock,
    )

    with pytest.raises(DeleteBookingException) as exc:
        await use_case(command)

    assert str(exc.value) == "Failed to delete booking"

    dynamodb_resource_mock.Table.assert_called_once_with("booking")

    table_mock.delete_item.assert_called_once_with(
        Key={
            "pk": f"BIKE#{command.bike_id}",
            "sk": f"BOOKING#{command.booking_id}",
        }
    )

    get_booking_use_case_mock.assert_awaited_once_with(
        GetBookingDetailQuery(
            bike_id=command.bike_id,
            booking_id=command.booking_id,
        )
    )
