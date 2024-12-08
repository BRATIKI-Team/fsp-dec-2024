from typing import List

from app.data.domains.event import EventFilter
from app.data.repositories.filter_repository import FilterRepository, FilterMapItem, mongo_multiple_equality_builder, \
    mongo_daterange_builder, mongo_bool_builder


class EventFilterRepository(FilterRepository[EventFilter]):
    def get_filters(self) -> List[FilterMapItem[EventFilter]]:
        return [
            FilterMapItem(
                type=EventFilter.regions,
                build=mongo_multiple_equality_builder,
                field='region_id'
            ),
            FilterMapItem(
                type=EventFilter.disciplines,
                build=mongo_multiple_equality_builder,
                field='discipline'
            ),
            FilterMapItem(
                type=EventFilter.daterange,
                build=mongo_daterange_builder,
                field='start_date'
            ),
            FilterMapItem(
                type=EventFilter.ekp,
                build=mongo_bool_builder,
                field='is_approved_event'
            )
        ]
