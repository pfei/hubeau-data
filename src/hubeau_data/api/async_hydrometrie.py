from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.hydrometrie import (
    ObsElab,
    ObsElabParams,
    ObservationTr,
    ObservationTrParams,
    Site,
    SiteParams,
    Station,
    StationParams,
)
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.utils import extract_next_cursor


class AsyncHydrometrieAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"

    async def get_sites(
        self, params: Optional[SiteParams] = None
    ) -> PagedResponse[Site]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/sites",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[Site](
            count=body["count"],
            data=[Site(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_stations(
        self, params: Optional[StationParams] = None
    ) -> PagedResponse[Station]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[Station](
            count=body["count"],
            data=[Station(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_observations_tr(
        self, params: Optional[ObservationTrParams] = None
    ) -> PagedResponse[ObservationTr]:
        resp = await self._get(
            f"{self.BASE_URL}/observations_tr",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ObservationTr](
            count=body["count"],
            data=[ObservationTr(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_obs_elab(
        self, params: Optional[ObsElabParams] = None
    ) -> PagedResponse[ObsElab]:
        resp = await self._get(
            f"{self.BASE_URL}/obs_elab",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ObsElab](
            count=body["count"],
            data=[ObsElab(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
