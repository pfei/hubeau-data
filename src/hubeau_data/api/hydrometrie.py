from typing import Any, List

import httpx

from hubeau_data.models.hydrometrie import ObsElab, ObservationTr, Site, Station


class HydrometrieAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"

    def get_sites(self, **kwargs: Any) -> List[Site]:
        url = f"{self.BASE_URL}/referentiel/sites"
        resp = httpx.get(url, params=kwargs)
        resp.raise_for_status()
        data = resp.json()["data"]
        return [Site(**item) for item in data]

    def get_stations(self, **kwargs: Any) -> List[Station]:
        url = f"{self.BASE_URL}/referentiel/stations"
        resp = httpx.get(url, params=kwargs)
        resp.raise_for_status()
        data = resp.json()["data"]
        return [Station(**item) for item in data]

    def get_observations_tr(self, **kwargs: Any) -> List[ObservationTr]:
        url = f"{self.BASE_URL}/observations_tr"
        resp = httpx.get(url, params=kwargs)
        resp.raise_for_status()
        data = resp.json()["data"]
        return [ObservationTr(**item) for item in data]

    def get_obs_elab(self, **kwargs: Any) -> List[ObsElab]:
        url = f"{self.BASE_URL}/obs_elab"
        resp = httpx.get(url, params=kwargs)
        resp.raise_for_status()
        data = resp.json()["data"]
        return [ObsElab(**item) for item in data]
