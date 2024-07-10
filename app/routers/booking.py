from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.exceptions.booking_exceptions import (
    CreateBookingException,
    DeleteBookingException,
    UpdateBookingException,
)
from app.libs import LoggerDependency
from app.schemas.bike import Bike, GetAvailableBikesQuery
from app.schemas.booking import (
    Booking,
    BookingsForBike,
    CreateBookingCommand,
    CreateBookingPayload,
    DeleteBookingCommand,
    GetBookingDetailQuery,
    GetBookingsForBikeQuery,
    GetBookingsForUserQuery,
    UpdateBookingCommand,
    UpdateBookingPayload,
)
from app.schemas.common import PaginatedItems
from app.use_cases.create_booking import CreateBookingDependency
from app.use_cases.delete_booking import DeleteBookingDependency
from app.use_cases.get_available_bikes import GetAvailableBikesDependency
from app.use_cases.get_booking_detail import GetBookingDetailDependency
from app.use_cases.get_bookings_for_bike import GetBookingsForBikeDependency
from app.use_cases.get_bookings_for_user import GetBookingsForUserDependency
from app.use_cases.update_booking import UpdateBookingDependency

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bike not found"
        )

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
        )

    return result


@router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking(
    use_case: CreateBookingDependency,
    logger: LoggerDependency,
    payload: CreateBookingPayload,
) -> Booking:
    try:
        return await use_case(CreateBookingCommand(**payload.model_dump()))
    except CreateBookingException as e:
        logger.error(f"Error creating booking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating booking",
        )


@router.delete("/{bike_id}/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    use_case: DeleteBookingDependency,
    logger: LoggerDependency,
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
            )

    except DeleteBookingException as e:
        logger.error(f"Error deleting booking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting booking",
        )


@router.patch("/{bike_id}/{booking_id}", response_model=Booking)
async def update_booking(
    use_case: UpdateBookingDependency,
    logger: LoggerDependency,
    bike_id: str,
    booking_id: str,
    payload: UpdateBookingPayload,
) -> Booking:
    try:
        result = await use_case(
            UpdateBookingCommand(
                bike_id=bike_id,
                booking_id=booking_id,
                user_id=payload.user_id,
                booking_date=payload.booking_date,
            )
        )

        if result is None:
            raise HTTPException(status_code=404, detail="Booking not found")

    except UpdateBookingException as e:
        logger.error(f"Error updating booking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating booking",
        )

    return result
