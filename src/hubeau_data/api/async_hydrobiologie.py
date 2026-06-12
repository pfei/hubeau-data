from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.hydrobiologie import (
    IndiceHydrobio,
    IndiceHydrobioParams,
    StationHydrobio,
    StationHydrobioParams,
    TaxonHydrobio,
    TaxonHydrobioParams,
)


class AsyncHydrobiologieAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/hydrobio"

    async def get_stations(
        self, params: Optional[StationHydrobioParams] = None
    ) -> List[StationHydrobio]:
        resp = await self._get(
            f"{self.BASE_URL}/stations_hydrobio",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationHydrobio(**item) for item in resp.json().get("data", [])]

    async def get_indices(
        self, params: Optional[IndiceHydrobioParams] = None
    ) -> List[IndiceHydrobio]:
        resp = await self._get(
            f"{self.BASE_URL}/indices",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [IndiceHydrobio(**item) for item in resp.json().get("data", [])]

    async def get_taxons(
        self, params: Optional[TaxonHydrobioParams] = None
    ) -> List[TaxonHydrobio]:
        resp = await self._get(
            f"{self.BASE_URL}/taxons",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [TaxonHydrobio(**item) for item in resp.json().get("data", [])]
