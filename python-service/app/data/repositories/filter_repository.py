from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Callable, Any, TypeVar, Generic, Mapping

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor

from app.api.dto import SearchReq, Criterion

TEnum = TypeVar("TEnum", bound=Enum)


@dataclass
class DatabaseQuery:
    collection: AsyncIOMotorCollection
    filters: Mapping[str, Any]

    def get(self) -> AsyncIOMotorCursor:
        return self.collection.find(self.filters)


@dataclass
class FilterMapItem(Generic[TEnum]):
    type: TEnum
    build: Callable[[str | None, Any], Mapping[str, Any]]
    field: str | None


class FilterRepository(Generic[TEnum]):
    def apply(
            self,
            collection: AsyncIOMotorCollection,
            req: SearchReq
    ) -> AsyncIOMotorCursor:
        filters = self.get_filters()
        query = DatabaseQuery(collection=collection, filters={})

        for criterion in req.criteria:
            filter_model = self.__get_filter_map_item_by_criterion(criterion, filters)

            query.filters = {**query.filters, **filter_model.build(filter_model.field, criterion.value)}

        return query.get()

    @abstractmethod
    def get_filters(self) -> List[FilterMapItem[TEnum]]:
        pass

    @staticmethod
    def __get_filter_map_item_by_criterion(criterion: Criterion, filters: List[FilterMapItem[TEnum]]) -> FilterMapItem[
        TEnum]:
        print(criterion, filters)
        for filter_model in filters:
            if filter_model.type == criterion.field:
                return filter_model
        raise Exception("Filter not found")


def mongo_multiple_equality_builder(field: str | None, value: Any) -> Mapping[str, Any]:
    if isinstance(field, str) and isinstance(value, List) and all(isinstance(item, (str, int)) for item in value):
        return {field: {"$in": value}}

    raise Exception("Bad configuration of filters.")


def mongo_daterange_builder(field: str | None, value: Any) -> Mapping[str, Any]:
    if isinstance(field, str) and isinstance(value, Mapping) and "start" in value and "end" in value:
        return {field: {"$gte": datetime.fromisoformat(value["start"]), "$lte": datetime.fromisoformat(value["end"])}}

    raise Exception("Bad configuration of filters.")


def mongo_bool_builder(field: str | None, value: Any) -> Mapping[str, Any]:
    if isinstance(field, str) and isinstance(value, bool):
        return {field: {"$eq": value}}

    raise Exception("Bad configuration of filters.")


def mongo_text_builder(field: str | None, value: Any) -> Mapping[str, Any]:
    if isinstance(field, str) and isinstance(value, str):
        return {field: {"$regex": value, '$options': 'i'}}

    raise Exception("Bad configuration of filters.")
