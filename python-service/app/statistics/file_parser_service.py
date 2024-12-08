from io import BytesIO
from typing import Annotated, List

import pandas as pd
from fastapi import Depends, HTTPException, status, UploadFile

from app.data.domains.team_result import TeamResult, TeamPlace
from app.services.region_service import RegionService


class FileParserService:
    def __init__(
            self,
            region_service: Annotated[RegionService, Depends(RegionService)],
    ):
        self._region_service = region_service

    async def parse_from_results_file(self, file: UploadFile) -> List[TeamResult]:
        data = None
        print("file type", file.content_type)
        match file.content_type:
            case "application/vnd.ms-excel":
                data = await self.__parse_excel_file(file)
            case "text/csv":
                data = await self.__parse_csv_file(file)

        if data is not None and not data.empty:
            return await self.__compile_data(data)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File type is not allowed",
            )

    async def parse_to_results_file(self, team_results: List[TeamResult]) -> BytesIO:
        data = []
        for team_result in team_results:
            region = await self._region_service.get(team_result.region_id)
            data.append({
                "Команда": team_result.name,
                "Регион": region.name,
                "Рейтинг": team_result.rating,
            })

        df = pd.DataFrame(data)

        # Save the DataFrame to an Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output) as writer:
            df.to_excel(writer, index=False, sheet_name="Results")

        # Move the pointer to the start of the stream
        output.seek(0)
        return output

    async def __compile_data(self, data_frame: pd.DataFrame) -> List[TeamResult]:
        team_results = []

        # Map Cyrillic column names to standard English ones
        column_mapping = {
            "Команда": "team",
            "Регион": "region",
            "Рейтинг": "points"
        }
        print("data_frame", data_frame)

        data_frame = data_frame.rename(columns=column_mapping)
        print("data_frame", data_frame)
        # Validate required columns
        required_columns = {"team", "region", "points"}
        if not required_columns.issubset(data_frame.columns):
            raise ValueError(f"DataFrame is missing required columns: {required_columns - set(data_frame.columns)}")

        # Sort teams by points in descending order
        df_sorted = data_frame.sort_values(by="points", ascending=False).reset_index(drop=True)

        for idx, row in df_sorted.iterrows():
            place = None
            if idx == 0:
                place = TeamPlace.FIRST
            elif idx == 1:
                place = TeamPlace.SECOND
            elif idx == 2:
                place = TeamPlace.THIRD

            region = await self._region_service.get_by_subject(row["region"])
            team_results.append(
                TeamResult(
                    name=row["team"],
                    region_id=region.id,
                    place=place,
                    rating=row["points"]
                )
            )

        return team_results

    @staticmethod
    async def __parse_excel_file(file: UploadFile) -> pd.DataFrame:
        data = await file.read()
        return pd.read_excel(BytesIO(data), engine="xlrd")

    @staticmethod
    async def __parse_csv_file(file: UploadFile) -> pd.DataFrame:
        return pd.read_csv(BytesIO(await file.read()))
