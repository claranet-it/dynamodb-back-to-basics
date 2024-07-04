from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.libs.aws import get_dynamodb_resource
from app.schemas.booking import (
    Booking,
    BookingsForBike,
    GetBookingsForBikeQuery,
    GetBookingsForUserQuery,
)
from app.schemas.common import PaginatedItems
from app.settings import Settings, get_settings
from app.use_cases.get_bookings_for_bike import get_bookings_for_bike
from app.use_cases.get_bookings_for_user import get_bookings_for_user

router = APIRouter(
    prefix="/api/booking",
)

DynamoDBResourceDependency = Annotated[Any, Depends(get_dynamodb_resource)]
SettingsDependency = Annotated[Settings, Depends(get_settings)]


@router.get("/bike/{bike_id}", response_model=BookingsForBike)
async def bookings_for_bike(
    dynamodb_resource: DynamoDBResourceDependency,
    bike_id: str,
) -> BookingsForBike:
    use_case = get_bookings_for_bike(dynamodb_resource)
    result = await use_case(GetBookingsForBikeQuery(bike_id=bike_id))

    if result is None:
        raise HTTPException(status_code=404, detail="Bike not found")

    return result


@router.get("/user/{user_id}", response_model=PaginatedItems[Booking])
async def bookings_for_user(
    dynamodb_resource: DynamoDBResourceDependency,
    get_settings: SettingsDependency,
    user_id: str,
    start: Optional[str] = None,
    limit: Optional[int] = None,
) -> BookingsForBike:
    use_case = get_bookings_for_user(dynamodb_resource, get_settings)
    return await use_case(
        GetBookingsForUserQuery(
            user_id=user_id,
            start=start,
            limit=limit,
        )
    )
