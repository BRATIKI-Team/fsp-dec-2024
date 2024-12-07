from io import BytesIO
from typing import Annotated, List

import pandas as pd
from fastapi import Depends, HTTPException, status

from app.data.domains.file_model import FileModel
from app.data.domains.team_result import TeamResult, TeamPlace
from app.services.file_model_service import FileModelService
from app.services.region_service import RegionService


class FileParserService:
    def __init__(
            self,
            file_model_service: Annotated[FileModelService, Depends(FileModelService)],
            region_service: Annotated[RegionService, Depends(RegionService)]
    ):
        self._file_model_service = file_model_service
        self._region_service = region_service

    async def parse_file_for_statistics(self, file_id: str) -> None:
        file_model = await self._file_model_service.get(file_id)
        if not file_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        data = None
        match file_model.file_type:
            case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                data = self.__parse_excel_file(file_model)
            case "text/csv":
                data = self.__parse_csv_file(file_model)

    async def __compile_data(self, data_frame: pd.DataFrame) -> List[TeamResult]:
        team_results = []

        # Map Cyrillic column names to standard English ones
        column_mapping = {
            "Команда": "team",
            "Регион": "region",
            "Результат": "points"
        }
        data_frame = data_frame.rename(columns=column_mapping)

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


            team_results.append(
                TeamResult(
                    name=row["team"],
                    region_id=row["region"],
                    place=place
                )
            )

        return team_results

    @staticmethod
    async def __parse_excel_file(file_model: FileModel) -> pd.DataFrame:
        with BytesIO(file_model.file_data) as byte_stream:
            df = pd.read_excel(byte_stream)
        return df

    @staticmethod
    async def __parse_csv_file(file_model: FileModel) -> pd.DataFrame:
        with BytesIO(file_model.file_data) as byte_stream:
            df = pd.read_csv(byte_stream)
        return df
