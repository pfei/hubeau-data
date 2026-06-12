from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.piezometrie import (
    ChroniquePiezo,
    ChroniquePiezoParams,
    ChroniquePiezoTr,
    ChroniquePiezoTrParams,
    StationPiezo,
    StationPiezoParams,
)


class AsyncPiezometrieAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/niveaux_nappes"

    async def get_stations(
        self, params: Optional[StationPiezoParams] = None
    ) -> List[StationPiezo]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationPiezo(**item) for item in resp.json().get("data", [])]

    async def get_chroniques(
        self, params: Optional[ChroniquePiezoParams] = None
    ) -> List[ChroniquePiezo]:
        resp = await self._get(
            f"{self.BASE_URL}/chroniques",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ChroniquePiezo(**item) for item in resp.json().get("data", [])]

    async def get_chroniques_tr(
        self, params: Optional[ChroniquePiezoTrParams] = None
    ) -> List[ChroniquePiezoTr]:
        resp = await self._get(
            f"{self.BASE_URL}/chroniques_tr",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ChroniquePiezoTr(**item) for item in resp.json().get("data", [])]
