from typing import List

from hubeau_data.api.hydrometrie import HydrometrieAPI
from hubeau_data.api.qualite_rivieres import QualiteRivieresAPI
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


class HubeauClient:
    """Unified client for the Hubeau APIs.
    Access sub-APIs as .qualite_rivieres and .hydrometrie attributes.
    """

    def __init__(self) -> None:
        self.qualite_rivieres = QualiteRivieresAPI()
        self.hydrometrie = HydrometrieAPI()


class SimpleHydrometrieClient:
    def __init__(self) -> None:
        self.api = HydrometrieAPI()

    def get_sites_by_department(
        self, code_departement: str, size: int = 10
    ) -> List[Site]:
        params = SiteParams(code_departement=[code_departement], size=size)
        return self.api.get_sites(params=params)

    def get_stations_by_commune(
        self, code_commune: str, size: int = 10
    ) -> List[Station]:
        params = StationParams(code_commune_station=code_commune, size=size)
        return self.api.get_stations(params=params)

    def get_observations_by_station(
        self, code_station: str, size: int = 10
    ) -> List[ObservationTr]:
        params = ObservationTrParams(code_station=[code_station], size=size)
        return self.api.get_observations_tr(params=params)

    def get_observations_elab_by_station(
        self, code_station: str, size: int = 10
    ) -> List[ObsElab]:
        params = ObsElabParams(code_station=[code_station], size=size)
        return self.api.get_obs_elab(params=params)
