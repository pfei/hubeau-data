from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.pagination import PagedResponse
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
from hubeau_data.utils import extract_next_cursor


class AsyncPoissonAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/etat_piscicole"

    async def get_stations(
        self, params: Optional[StationPoissonParams] = None
    ) -> PagedResponse[StationPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationPoisson](
            count=body["count"],
            data=[StationPoisson(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_indicateurs(
        self, params: Optional[IndicateurPoissonParams] = None
    ) -> PagedResponse[IndicateurPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/indicateurs",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[IndicateurPoisson](
            count=body["count"],
            data=[IndicateurPoisson(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_observations(
        self, params: Optional[ObservationPoissonParams] = None
    ) -> PagedResponse[ObservationPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/observations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ObservationPoisson](
            count=body["count"],
            data=[ObservationPoisson(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_operations(
        self, params: Optional[OperationPoissonParams] = None
    ) -> PagedResponse[OperationPoisson]:
        resp = await self._get(
            f"{self.BASE_URL}/operations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[OperationPoisson](
            count=body["count"],
            data=[OperationPoisson(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
