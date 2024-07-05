from typing import Optional

from fastapi import APIRouter, HTTPException

from app.schemas.booking import (
    Booking,
    BookingsForBike,
    GetBookingsForBikeQuery,
    GetBookingsForUserQuery,
)
from app.schemas.common import PaginatedItems
from app.use_cases import (
    GetBookingsForBikeDependency,
    GetBookingsForUserDependency,
)

router = APIRouter(
    prefix="/api/booking",
)


@router.get("/bike/{bike_id}", response_model=BookingsForBike)
async def bookings_for_bike(
    use_case: GetBookingsForBikeDependency,
    bike_id: str,
) -> BookingsForBike:
    result = await use_case(GetBookingsForBikeQuery(bike_id=bike_id))

    if result is None:
        raise HTTPException(status_code=404, detail="Bike not found")

    return result


@router.get("/user/{user_id}", response_model=PaginatedItems[Booking])
async def bookings_for_user(
    use_case: GetBookingsForUserDependency,
    user_id: str,
    start: Optional[str] = None,
    limit: Optional[int] = None,
) -> BookingsForBike:
    return await use_case(
        GetBookingsForUserQuery(
            user_id=user_id,
            start=start,
            limit=limit,
        )
    )
