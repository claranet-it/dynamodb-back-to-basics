from typing import Annotated

from fastapi import Depends

from app.use_cases.create_booking import CreateBookingUseCase, create_booking
from app.use_cases.get_available_bikes import (
    GetAvailableBikesUseCase,
    get_available_bikes,
)
from app.use_cases.get_booking_detail import (
    GetBookingDetailUseCase,
    get_booking_detail,
)
from app.use_cases.get_bookings_for_bike import (
    GetBookingsForBikeUseCase,
    get_bookings_for_bike,
)
from app.use_cases.get_bookings_for_user import (
    GetBookingsForUserUseCase,
    get_bookings_for_user,
)

GetBookingsForBikeDependency = Annotated[
    GetBookingsForBikeUseCase, Depends(get_bookings_for_bike)
]

GetBookingsForUserDependency = Annotated[
    GetBookingsForUserUseCase, Depends(get_bookings_for_user)
]

GetAvailableBikesDependency = Annotated[
    GetAvailableBikesUseCase, Depends(get_available_bikes)
]

GetBookingDetailDependency = Annotated[
    GetBookingDetailUseCase, Depends(get_booking_detail)
]

CreateBookingDependency = Annotated[CreateBookingUseCase, Depends(create_booking)]
