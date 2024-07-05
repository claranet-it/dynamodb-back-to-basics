from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from app.schemas.common import PaginatedQuery, SingleTableModel


class Bike(SingleTableModel):
    id: str
    model: str
    status: str
    location: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class GetAvailableBikesQuery(PaginatedQuery):
    pass
