import base64
import json
from typing import Annotated, Protocol

from fastapi import Depends

from app.libs.aws import DynamoDBResourceDependency
from app.libs.settings import SettingsDependency
from app.schemas.bike import Bike, GetAvailableBikesQuery
from app.schemas.common import PaginatedItems


class GetAvailableBikesUseCase(Protocol):
    def __call__(self, query: GetAvailableBikesQuery) -> PaginatedItems[Bike]: ...


def get_available_bikes(
    dynamodb_resource: DynamoDBResourceDependency,
    settings: SettingsDependency,
):
    async def _get_available_bikes(
        query: GetAvailableBikesQuery,
    ) -> PaginatedItems[Bike]:
        table = dynamodb_resource.Table("booking")

        query_params = {
            "KeyConditionExpression": "gsi1_pk = :gsi1_pk",
            "ExpressionAttributeValues": {
                ":gsi1_pk": "AVAILABLE",
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
            return PaginatedItems[Bike](items=[], next=None)

        last_evaluated_key = result.get("LastEvaluatedKey")
        next_token = None
        if last_evaluated_key:
            next_token = base64.b64encode(
                json.dumps(last_evaluated_key).encode()
            ).decode()

        bikes = result["Items"]

        return PaginatedItems[Bike](
            items=[Bike(**bike) for bike in bikes],
            next=next_token,
        )

    return _get_available_bikes


GetAvailableBikesDependency = Annotated[
    GetAvailableBikesUseCase, Depends(get_available_bikes)
]
