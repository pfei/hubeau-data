from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.poisson import (
    IndicateurPoisson,
    IndicateurPoissonParams,
    ObservationPoisson,
    ObservationPoissonParams,
    OperationPoisson,
    OperationPoissonParams,
    StationPoisson,
    StationPoissonParams,
)


class AsyncPoissonAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/etat_piscicole"

    async def get_stations(
        self, params: Optional[StationPoissonParams] = None
    ) -> List[StationPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationPoisson(**item) for item in resp.json().get("data", [])]

    async def get_indicateurs(
        self, params: Optional[IndicateurPoissonParams] = None
    ) -> List[IndicateurPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/indicateurs",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [IndicateurPoisson(**item) for item in resp.json().get("data", [])]

    async def get_observations(
        self, params: Optional[ObservationPoissonParams] = None
    ) -> List[ObservationPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/observations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ObservationPoisson(**item) for item in resp.json().get("data", [])]

    async def get_operations(
        self, params: Optional[OperationPoissonParams] = None
    ) -> List[OperationPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/operations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [OperationPoisson(**item) for item in resp.json().get("data", [])]
