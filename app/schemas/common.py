from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedItems(BaseModel, Generic[T]):
    items: list[T]
    next: Optional[str]


class Paginated(BaseModel):
    start: Optional[str] = None
    limit: Optional[int] = None


class SingleTableModel(BaseModel):
    pk: str = Field(exclude=True)
    sk: str = Field(exclude=True)
    gs1_pk: str = Field(exclude=True)
    gs1_sk: str = Field(exclude=True)
    entity: str = Field(exclude=True)
