from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from app.schemas.common import SingleTableModel


class User(SingleTableModel):
    id: str
    fullname: str
    email: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
