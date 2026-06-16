from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.ecoulement import (
    CampagneEcoulement,
    CampagneEcoulementParams,
    ObservationEcoulement,
    ObservationEcoulementParams,
    StationEcoulement,
    StationEcoulementParams,
)
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.utils import extract_next_cursor


class AsyncEcoulementAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/ecoulement"

    async def get_stations(
        self, params: Optional[StationEcoulementParams] = None
    ) -> PagedResponse[StationEcoulement]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationEcoulement](
            count=body["count"],
            data=[StationEcoulement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_observations(
        self, params: Optional[ObservationEcoulementParams] = None
    ) -> PagedResponse[ObservationEcoulement]:
        resp = await self._get(
            f"{self.BASE_URL}/observations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ObservationEcoulement](
            count=body["count"],
            data=[ObservationEcoulement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_campagnes(
        self, params: Optional[CampagneEcoulementParams] = None
    ) -> PagedResponse[CampagneEcoulement]:
        resp = await self._get(
            f"{self.BASE_URL}/campagnes",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[CampagneEcoulement](
            count=body["count"],
            data=[CampagneEcoulement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
