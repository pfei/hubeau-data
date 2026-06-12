from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.ecoulement import (
    CampagneEcoulement,
    CampagneEcoulementParams,
    ObservationEcoulement,
    ObservationEcoulementParams,
    StationEcoulement,
    StationEcoulementParams,
)


class AsyncEcoulementAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/ecoulement"

    async def get_stations(
        self, params: Optional[StationEcoulementParams] = None
    ) -> List[StationEcoulement]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationEcoulement(**item) for item in resp.json().get("data", [])]

    async def get_observations(
        self, params: Optional[ObservationEcoulementParams] = None
    ) -> List[ObservationEcoulement]:
        resp = await self._get(
            f"{self.BASE_URL}/observations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ObservationEcoulement(**item) for item in resp.json().get("data", [])]

    async def get_campagnes(
        self, params: Optional[CampagneEcoulementParams] = None
    ) -> List[CampagneEcoulement]:
        resp = await self._get(
            f"{self.BASE_URL}/campagnes",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [CampagneEcoulement(**item) for item in resp.json().get("data", [])]
