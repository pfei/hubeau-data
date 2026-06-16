from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.qualite_rivieres import (
    AnalysePc,
    AnalysePcParams,
    StationPc,
    StationPcParams,
)
from hubeau_data.utils import extract_next_cursor


class AsyncQualiteRivieresAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres"

    async def get_stations(
        self, params: Optional[StationPcParams] = None
    ) -> PagedResponse[StationPc]:
        resp = await self._get(
            f"{self.BASE_URL}/station_pc",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationPc](
            count=body["count"],
            data=[StationPc(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_analyses(
        self, params: Optional[AnalysePcParams] = None
    ) -> PagedResponse[AnalysePc]:
        resp = await self._get(
            f"{self.BASE_URL}/analyse_pc",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[AnalysePc](
            count=body["count"],
            data=[AnalysePc(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
