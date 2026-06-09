from typing import List, Optional

import httpx

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


class HydrometrieAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"

    def get_sites(self, params: Optional[SiteParams] = None) -> List[Site]:
        url = f"{self.BASE_URL}/referentiel/sites"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [Site(**item) for item in resp.json()["data"]]

    def get_stations(self, params: Optional[StationParams] = None) -> List[Station]:
        url = f"{self.BASE_URL}/referentiel/stations"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [Station(**item) for item in resp.json()["data"]]

    def get_observations_tr(
        self, params: Optional[ObservationTrParams] = None
    ) -> List[ObservationTr]:
        url = f"{self.BASE_URL}/observations_tr"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [ObservationTr(**item) for item in resp.json()["data"]]

    def get_obs_elab(self, params: Optional[ObsElabParams] = None) -> List[ObsElab]:
        url = f"{self.BASE_URL}/obs_elab"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [ObsElab(**item) for item in resp.json()["data"]]
