from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.libs.aws import get_dynamodb_resource
from app.schemas.booking import BookingsForBike, GetBookingsForBikeQuery
from app.use_cases.get_bookings_for_bike import get_bookings_for_bike

router = APIRouter(
    prefix="/api/booking",
)

DynamoDBResourceDependency = Annotated[Any, Depends(get_dynamodb_resource)]


@router.get("/bike/{bike_id}", response_model=BookingsForBike)
async def list_devices(
    dynamodb_resource: DynamoDBResourceDependency,
    bike_id: str,
) -> BookingsForBike:
    use_case = get_bookings_for_bike(dynamodb_resource)
    result = await use_case(GetBookingsForBikeQuery(bike_id=bike_id))

    if result is None:
        raise HTTPException(status_code=404, detail="Bike not found")

    return result
