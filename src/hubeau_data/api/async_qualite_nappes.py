from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.qualite_nappes import (
    AnalyseNappe,
    AnalyseNappeParams,
    StationNappe,
    StationNappeParams,
)
from hubeau_data.utils import extract_next_cursor


class AsyncQualiteNappesAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/qualite_nappes"

    async def get_stations(
        self, params: Optional[StationNappeParams] = None
    ) -> PagedResponse[StationNappe]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationNappe](
            count=body["count"],
            data=[StationNappe(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_analyses(
        self, params: Optional[AnalyseNappeParams] = None
    ) -> PagedResponse[AnalyseNappe]:
        resp = await self._get(
            f"{self.BASE_URL}/analyses",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[AnalyseNappe](
            count=body["count"],
            data=[AnalyseNappe(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
