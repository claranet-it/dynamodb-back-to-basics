import base64
import json
from typing import Any

from app.schemas.booking import (
    Booking,
    GetBookingsForUserQuery,
)
from app.schemas.common import PaginatedItems
from app.settings import Settings


def get_bookings_for_user(
    dynamodb_resource: Any,
    settings: Settings,
):
    async def _get_bookings_for_user(
        query: GetBookingsForUserQuery,
    ) -> PaginatedItems[Booking]:
        table = dynamodb_resource.Table("booking")

        gs1_pk_value = f"USER#{query.user_id}"

        query_params = {
            "KeyConditionExpression": "gs1_pk = :gs1_pk AND begins_with(gs1_sk, :gs1_sk)",
            "ExpressionAttributeValues": {
                ":gs1_pk": gs1_pk_value,
                ":gs1_sk": "BOOKING#",
            },
            "Limit": query.limit or settings.dynamodb_default_query_limit,
            "IndexName": "gs1",
        }

        if query.start:
            query_params["ExclusiveStartKey"] = json.loads(
                base64.b64decode(query.start).decode()
            )

        result = table.query(**query_params)
        if not result["Items"]:
            return PaginatedItems[Booking](items=[], next=None)

        last_evaluated_key = result.get("LastEvaluatedKey")
        next = None
        if last_evaluated_key:
            next = base64.b64encode(json.dumps(last_evaluated_key).encode()).decode()

        bookings = result["Items"]

        return PaginatedItems[Booking](
            items=[Booking(**booking) for booking in bookings],
            next=next,
        )

    return _get_bookings_for_user
