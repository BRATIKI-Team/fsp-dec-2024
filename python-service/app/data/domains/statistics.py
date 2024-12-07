from typing import Optional

from pydantic import BaseModel


class Statistics(BaseModel):
    id: Optional[str] = None
    region_id: str
    participants_count: int
    events_count: int
    first_place_count: int
    second_place_count: int
    third_place_count: int
    year: int

    @staticmethod
    def get_default(region_id: str, year: int):
        return Statistics(
            region_id=region_id,
            participants_count=0,
            events_count=0,
            first_place_count=0,
            second_place_count=0,
            third_place_count=0,
            year=year
        )