import httpx
import pytest

from hubeau_data.client import SimpleHydrometrieClient
from hubeau_data.models.hydrometrie import ObsElab, ObservationTr, Site, Station

# --- FIXTURES ---


# @pytest.fixture
# def client() -> SimpleHydrometrieClient:
#     """Initialize the client for test injection."""
#     return SimpleHydrometrieClient()


# @pytest.fixture
# def mock_obs_data() -> dict:
#     """Mock data based on real Hubeau API response schema."""
#     return {
#         "data": [
#             {
#                 "code_station": "K066331001",
#                 "date_obs": "2026-06-08T14:00:00Z",
#                 "resultat_obs": 12.5,
#                 "libelle_qualification_obs": "Qualifiée",
#             }
#         ]
#     }


# --- TESTS --


@pytest.mark.live
def test_station_model_validation() -> None:
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/referentiel/stations"
    params: dict[str, str | int] = {"code_commune_station": "75056", "size": 1}
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()["data"]
    for item in data:
        Station(**item)


@pytest.mark.live
def test_site_model_validation() -> None:
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/referentiel/sites"
    params: dict[str, str | int] = {"code_departement": "95", "size": 1}
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()["data"]
    for item in data:
        Site(**item)


@pytest.mark.live
def test_observation_tr_model_validation() -> None:
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/observations_tr"
    params: dict[str, str | int] = {"code_station": "Y120201001", "size": 1}
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()["data"]
    for item in data:
        ObservationTr(**item)


@pytest.mark.live
def test_obs_elab_model_validation() -> None:
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab"
    params: dict[str, str | int] = {
        "code_station": "Y390001001",  # Example: Rhône at Valence (often has data)
        "grandeur_hydro_elab": "QmM",  # Débit moyen mensuel (valid value)
        "size": 1,
    }
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()["data"]
    for item in data:
        ObsElab(**item)


simple_client = SimpleHydrometrieClient()


@pytest.mark.live
def test_simple_client_sites_by_department() -> None:
    sites = simple_client.get_sites_by_department("95", size=1)
    assert len(sites) > 0
    assert hasattr(sites[0], "libelle_site")


@pytest.mark.live
def test_simple_client_stations_by_commune() -> None:
    stations = simple_client.get_stations_by_commune("75056", size=1)
    assert len(stations) > 0
    assert hasattr(stations[0], "libelle_station")


@pytest.mark.live
def test_simple_client_observations_by_station() -> None:
    obs = simple_client.get_observations_by_station("Y120201001", size=1)
    assert len(obs) > 0
    assert hasattr(obs[0], "date_obs")


@pytest.mark.live
def test_simple_client_observations_elab_by_station() -> None:
    obs = simple_client.get_observations_elab_by_station("Y390001001", size=1)
    assert len(obs) > 0
    assert hasattr(obs[0], "date_obs_elab")
