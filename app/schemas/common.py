from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedItems(BaseModel, Generic[T]):
    items: list[T]
    next: Optional[str]
