from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.exceptions.booking_exceptions import (
    CreateBookingException,
    DeleteBookingException,
)
from app.schemas.bike import Bike, GetAvailableBikesQuery
from app.schemas.booking import (
    Booking,
    BookingsForBike,
    CreateBookingCommand,
    DeleteBookingCommand,
    GetBookingDetailQuery,
    GetBookingsForBikeQuery,
    GetBookingsForUserQuery,
)
from app.schemas.common import PaginatedItems
from app.use_cases import (
    CreateBookingDependency,
    DeleteBookingDependency,
    GetAvailableBikesDependency,
    GetBookingDetailDependency,
    GetBookingsForBikeDependency,
    GetBookingsForUserDependency,
)

router = APIRouter(
    prefix="/api/booking",
)


@router.get("/available-bikes", response_model=PaginatedItems[Bike])
async def available_bikes(
    use_case: GetAvailableBikesDependency,
    start: Optional[str] = None,
    limit: Optional[int] = None,
) -> BookingsForBike:
    return await use_case(
        GetAvailableBikesQuery(
            start=start,
            limit=limit,
        )
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


@router.get("/detail/{bike_id}/{booking_id}", response_model=Optional[Booking])
async def booking_detail(
    use_case: GetBookingDetailDependency,
    bike_id: str,
    booking_id: str,
) -> BookingsForBike:
    result = await use_case(
        GetBookingDetailQuery(bike_id=bike_id, booking_id=booking_id)
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return result


@router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking(
    use_case: CreateBookingDependency,
    command: CreateBookingCommand,
) -> Booking:
    try:
        return await use_case(command)
    except CreateBookingException:
        raise HTTPException(status_code=500, detail="Error creating booking")


@router.delete("/{bike_id}/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    use_case: DeleteBookingDependency,
    bike_id: str,
    booking_id: str,
) -> None:
    try:
        result = await use_case(
            DeleteBookingCommand(
                bike_id=bike_id,
                booking_id=booking_id,
            )
        )

        if result is None:
            raise HTTPException(status_code=404, detail="Booking not found")

    except DeleteBookingException:
        raise HTTPException(status_code=500, detail="Error deleting booking")
