from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.hydrobiologie import (
    IndiceHydrobio,
    IndiceHydrobioParams,
    StationHydrobio,
    StationHydrobioParams,
    TaxonHydrobio,
    TaxonHydrobioParams,
)
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.utils import extract_next_cursor


class AsyncHydrobiologieAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/hydrobio"

    async def get_stations(
        self, params: Optional[StationHydrobioParams] = None
    ) -> PagedResponse[StationHydrobio]:
        resp = await self._get(
            f"{self.BASE_URL}/stations_hydrobio",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationHydrobio](
            count=body["count"],
            data=[StationHydrobio(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_indices(
        self, params: Optional[IndiceHydrobioParams] = None
    ) -> PagedResponse[IndiceHydrobio]:
        resp = await self._get(
            f"{self.BASE_URL}/indices",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[IndiceHydrobio](
            count=body["count"],
            data=[IndiceHydrobio(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_taxons(
        self, params: Optional[TaxonHydrobioParams] = None
    ) -> PagedResponse[TaxonHydrobio]:
        resp = await self._get(
            f"{self.BASE_URL}/taxons",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[TaxonHydrobio](
            count=body["count"],
            data=[TaxonHydrobio(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
