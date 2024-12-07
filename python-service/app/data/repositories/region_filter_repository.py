from typing import List

from app.data.domains.region import RegionFilter
from app.data.repositories.filter_repository import FilterMapItem, FilterRepository, mongo_text_builder


class RegionFilterRepository(FilterRepository[RegionFilter]):
    def get_filters(self) -> List[FilterMapItem[RegionFilter]]:
        return [
            FilterMapItem(
                type=RegionFilter.search,
                build=mongo_text_builder,
                field='subject'
            )
        ]
