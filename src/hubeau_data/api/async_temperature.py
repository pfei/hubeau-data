from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.temperature import (
    ChroniqueTemperature,
    ChroniqueTemperatureParams,
    StationTemperature,
    StationTemperatureParams,
)


class AsyncTemperatureAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/temperature"

    async def get_stations(
        self, params: Optional[StationTemperatureParams] = None
    ) -> List[StationTemperature]:
        resp = await self._get(
            f"{self.BASE_URL}/station",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationTemperature(**item) for item in resp.json().get("data", [])]

    async def get_chronique(
        self, params: Optional[ChroniqueTemperatureParams] = None
    ) -> List[ChroniqueTemperature]:
        resp = await self._get(
            f"{self.BASE_URL}/chronique",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ChroniqueTemperature(**item) for item in resp.json().get("data", [])]
