from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.piezometrie import (
    ChroniquePiezo,
    ChroniquePiezoParams,
    ChroniquePiezoTr,
    ChroniquePiezoTrParams,
    StationPiezo,
    StationPiezoParams,
)
from hubeau_data.utils import extract_next_cursor


class AsyncPiezometrieAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/niveaux_nappes"

    async def get_stations(
        self, params: Optional[StationPiezoParams] = None
    ) -> PagedResponse[StationPiezo]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationPiezo](
            count=body["count"],
            data=[StationPiezo(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_chroniques(
        self, params: Optional[ChroniquePiezoParams] = None
    ) -> PagedResponse[ChroniquePiezo]:
        resp = await self._get(
            f"{self.BASE_URL}/chroniques",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniquePiezo](
            count=body["count"],
            data=[ChroniquePiezo(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_chroniques_tr(
        self, params: Optional[ChroniquePiezoTrParams] = None
    ) -> PagedResponse[ChroniquePiezoTr]:
        resp = await self._get(
            f"{self.BASE_URL}/chroniques_tr",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniquePiezoTr](
            count=body["count"],
            data=[ChroniquePiezoTr(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
