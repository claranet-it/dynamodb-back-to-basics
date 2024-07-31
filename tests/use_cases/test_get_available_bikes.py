from unittest.mock import MagicMock

import pytest

from app.libs import settings
from app.schemas.bike import Bike
from app.use_cases.get_available_bikes import get_available_bikes


@pytest.mark.asyncio
async def test_get_available_bikes_ok(get_available_bikes_query):
    dynamodb_resource_mock = MagicMock()
    table_mock = MagicMock()
    table_mock.query.return_value = {
        "Items": [
            {
                "pk": "BIKE#002",
                "sk": "BIKE#002",
                "entity": "BIKE",
                "gsi1_pk": "NOT AVAILABLE",
                "gsi1_sk": "002",
                "id": "002",
                "model": "Camaro",
                "status": "AVAILABLE",
                "location": "Gotham City",
            }
        ],
        "LastEvaluatedKey": None,
    }
    dynamodb_resource_mock.Table.return_value = table_mock

    use_case = get_available_bikes(
        dynamodb_resource=dynamodb_resource_mock, settings=settings.get_settings()
    )

    query = get_available_bikes_query()

    available_bikes = await use_case(query)

    assert len(available_bikes.items) == 1
    assert available_bikes.items[0] == Bike(
        pk="BIKE#002",
        sk="BIKE#002",
        gsi1_pk="NOT AVAILABLE",
        gsi1_sk="002",
        entity="BIKE",
        id="002",
        model="Camaro",
        status="AVAILABLE",
        location="Gotham City",
    )

    dynamodb_resource_mock.Table.assert_called_once_with("booking")
    table_mock.query.assert_called_once_with(
        KeyConditionExpression="gsi1_pk = :gsi1_pk",
        ExpressionAttributeValues={":gsi1_pk": "AVAILABLE"},
        Limit=10,
        IndexName="gs1",
    )
