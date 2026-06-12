from typing import List, Optional

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


class AsyncHydrometrieAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"

    async def get_sites(self, params: Optional[SiteParams] = None) -> List[Site]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/sites",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [Site(**item) for item in resp.json()["data"]]

    async def get_stations(
        self, params: Optional[StationParams] = None
    ) -> List[Station]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [Station(**item) for item in resp.json()["data"]]

    async def get_observations_tr(
        self, params: Optional[ObservationTrParams] = None
    ) -> List[ObservationTr]:
        resp = await self._get(
            f"{self.BASE_URL}/observations_tr",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ObservationTr(**item) for item in resp.json()["data"]]

    async def get_obs_elab(
        self, params: Optional[ObsElabParams] = None
    ) -> List[ObsElab]:
        resp = await self._get(
            f"{self.BASE_URL}/obs_elab",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ObsElab(**item) for item in resp.json()["data"]]
