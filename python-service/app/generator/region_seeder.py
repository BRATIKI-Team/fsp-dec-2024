import json
from typing import Annotated, List

from fastapi import Depends

from app.data.domains.contacts import Contacts
from app.data.domains.region import Region
from app.data.repositories.region_repository import RegionRepository
from app.services.base_service import BaseService


class RegionSeeder(BaseService[Region]):
    def __init__(self, region_repository: Annotated[RegionRepository, Depends(RegionRepository)]):
        super().__init__(region_repository)

    async def seed(self) -> bool:
        regions = self.__load_regions_from_file('app/generator/docs/regions.json')
        for region in regions:
            print(f"Creating region: {region})")
            await self.create(region)

        return True

    @staticmethod
    def __load_regions_from_file(file_path: str) -> List[Region]:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        regions = []
        for item in json_data:
            contacts = Contacts(email=item["email"])
            region = Region(
                name=item["region"],
                subject=item["subject"],
                person=item.get("person"),
                contacts=contacts,
                is_main=False
            )
            regions.append(region)

        regions[0].is_main = True
        return regions
