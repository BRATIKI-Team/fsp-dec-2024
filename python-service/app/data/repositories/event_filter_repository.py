from typing import List

from app.data.domains.event import EventFilter
from app.data.repositories.filter_repository import FilterRepository, FilterMapItem, mongo_multiple_equality_builder


class EventFilterRepository(FilterRepository[EventFilter]):
    def get_filters(self) -> List[FilterMapItem[EventFilter]]:
        return [
            FilterMapItem(
                type=EventFilter.regions,
                build=mongo_multiple_equality_builder,
                field='region_id'
            )
        ]
