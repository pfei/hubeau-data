from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.temperature import (
    ChroniqueTemperature,
    ChroniqueTemperatureParams,
    StationTemperature,
    StationTemperatureParams,
)
from hubeau_data.utils import extract_next_cursor


class AsyncTemperatureAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/temperature"

    async def get_stations(
        self, params: Optional[StationTemperatureParams] = None
    ) -> PagedResponse[StationTemperature]:
        resp = await self._get(
            f"{self.BASE_URL}/station",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationTemperature](
            count=body["count"],
            data=[StationTemperature(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_chronique(
        self, params: Optional[ChroniqueTemperatureParams] = None
    ) -> PagedResponse[ChroniqueTemperature]:
        resp = await self._get(
            f"{self.BASE_URL}/chronique",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniqueTemperature](
            count=body["count"],
            data=[ChroniqueTemperature(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
