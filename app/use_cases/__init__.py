from typing import Annotated

from fastapi import Depends

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
