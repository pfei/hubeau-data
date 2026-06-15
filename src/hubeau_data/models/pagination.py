from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PagedResponse(BaseModel, Generic[T]):
    """Wraps a paginated Hub'Eau API response."""

    count: int
    data: list[T]
    next_cursor: Optional[str] = None
