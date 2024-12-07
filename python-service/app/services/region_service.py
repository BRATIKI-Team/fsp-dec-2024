import json
from typing import Annotated, List

from fastapi import Depends, HTTPException, status

from app.data.domains.contacts import Contacts
from app.data.domains.region import Region
from app.data.domains.user import UserRole
from app.data.repositories.region_repository import RegionRepository
from app.services.base_service import BaseService
from app.services.user_service import UserService


class RegionService(BaseService[Region]):
    def __init__(
            self,
            region_repository: Annotated[RegionRepository, Depends(RegionRepository)],
            user_service: Annotated[UserService, Depends(UserService)]):
        super().__init__(region_repository)
        self.region_repository = region_repository
        self.user_service = user_service

    # async def seed(self) -> bool:
    #     regions = self.__stub_regions()
    #     for region in regions:
    #         await self.create(region)
    #
    #     return True

    async def seed(self) -> bool:
        regions = self.__load_regions_from_file('app/generator/docs/regions.json')
        for region in regions:
            print(f"Creating region: {region})")
            await self.create(region)

        return True

    async def assign_admin(self, region_id: str, user_id: str) -> bool:
        return await  self.__assign_user_internal(region_id, user_id, UserRole.ADMIN)

    async def assign_member(self, region_id: str, user_id: str) -> bool:
        return await  self.__assign_user_internal(region_id, user_id, UserRole.MEMBER)

    async def __assign_user_internal(self, region_id: str, user_id: str, role: UserRole) -> bool:
        user = await self.user_service.get(user_id)
        if user is None or user.role != UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist or role is not default"
            )

        region = await  self.region_repository.get(region_id)
        if region is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region does not exist"
            )

        user.role = role
        user.region_id = region_id

        if role == UserRole.ADMIN:
            region.admin_id = user.id
            await self.region_repository.update(region.id, region)
        return await self.user_service.update(user_id, user)

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

    # @staticmethod
    # def __stub_regions() -> list[Region]:
    #     return [
    #         Region(
    #             name="North Region",
    #             description="Region characterized by mountain landscapes.",
    #             is_main=True,
    #             contacts=Contacts(email="north@example.com", phone="123-456-7890", social_links=[""])
    #         ),
    #         Region(
    #             name="South Region",
    #             description="Region known for its sunny beaches.",
    #             is_main=False,
    #             contacts=Contacts(email="south@example.com", phone="234-567-8901", social_links=[""])
    #         ),
    #         Region(
    #             name="East Region",
    #             description="Region with a rich cultural heritage.",
    #             is_main=False,
    #             contacts=Contacts(email="east@example.com", phone="345-678-9012", social_links=[""])
    #         )]
