from dataclasses import dataclass
from typing import List, Generic, TypeVar, Any

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


@dataclass
class Page(Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]
    more: bool



class Criterion(BaseModel):
    field: str
    value: Any


class FilterReq(BaseModel):
    criteria: List[Criterion]


class PageReq(BaseModel):
    page: int
    page_size: int


class SearchReq(FilterReq, PageReq):
    pass
