"""
Tests for the Hydrométrie API client.
To run only the fast mocked tests:
    uv run pytest -m "not live"
To run the live integration tests:
    uv run pytest -m "live" -s
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient, SimpleHydrometrieClient
from hubeau_data.models.hydrometrie import ObsElab, ObservationTr, Site, Station


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print(
        "\n[INFO] Live tests make real API calls and may be slow. "
        "If you experience timeouts, check your network connection or try again later."
    )


# ==============================================================================
# 1. MOCKED TESTS (Fast, deterministic, safe for CI)
# ==============================================================================

MINIMAL_SITE = {
    "code_site": "A1234567",
    "code_projection": 26,
    "coordonnee_x_site": 2.35,
    "coordonnee_y_site": 48.85,
    "latitude_site": 48.85,
    "longitude_site": 2.35,
    "premier_mois_annee_hydro_site": 1,
    "premier_mois_etiage_site": 7,
    "statut_site": 1,
    "geometry": {"type": "Point", "coordinates": [2.35, 48.85]},
}
MINIMAL_STATION = {
    "code_site": "A1234567",
    "code_station": "A123456701",
    "en_service": True,
    "code_projection": 26,
    "code_regime_station": 1,
    "coordonnee_x_station": 2.35,
    "coordonnee_y_station": 48.85,
    "latitude_station": 48.85,
    "longitude_station": 2.35,
    "qualification_donnees_station": 1,
}


MINIMAL_OBSERVATION_TR = {
    "code_station": "Y120201001",
    "date_obs": "2026-06-01T12:00:00Z",
    "resultat_obs": 42.5,
    "grandeur_hydro": "H",
}

MINIMAL_OBS_ELAB = {
    "code_station": "Y390001001",
    "date_obs_elab": "2026-01-01",
    "resultat_obs_elab": 150.0,
    "grandeur_hydro_elab": "QmM",
}


def test_get_sites_mocked(httpx_mock: HTTPXMock) -> None:
    """Test get_sites using a mocked HTTP response."""
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/referentiel/sites.*"),
        json={"count": 1, "data": [MINIMAL_SITE]},
        status_code=200,
    )
    client = HubeauClient()
    sites = client.hydrometrie.get_sites()
    assert isinstance(sites, list)
    assert len(sites) == 1
    assert isinstance(sites[0], Site)
    assert sites[0].code_site == "A1234567"


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    """Test get_stations using a mocked HTTP response."""
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/referentiel/stations.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = HubeauClient()
    stations = client.hydrometrie.get_stations()
    assert isinstance(stations, list)
    assert len(stations) == 1
    assert isinstance(stations[0], Station)
    assert stations[0].code_station == "A123456701"


def test_get_observations_tr_mocked(httpx_mock: HTTPXMock) -> None:
    """Test get_observations_tr using a mocked HTTP response."""
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/observations_tr.*"),
        json={"count": 1, "data": [MINIMAL_OBSERVATION_TR]},
        status_code=200,
    )
    client = HubeauClient()
    obs = client.hydrometrie.get_observations_tr()
    assert isinstance(obs, list)
    assert len(obs) == 1
    assert isinstance(obs[0], ObservationTr)
    assert obs[0].code_station == "Y120201001"


def test_get_obs_elab_mocked(httpx_mock: HTTPXMock) -> None:
    """Test get_obs_elab using a mocked HTTP response."""
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/obs_elab.*"),
        json={"count": 1, "data": [MINIMAL_OBS_ELAB]},
        status_code=200,
    )
    client = HubeauClient()
    obs = client.hydrometrie.get_obs_elab()
    assert isinstance(obs, list)
    assert len(obs) == 1
    assert isinstance(obs[0], ObsElab)
    assert obs[0].grandeur_hydro_elab == "QmM"


def test_simple_client_sites_by_department_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/referentiel/sites.*"),
        json={"count": 1, "data": [MINIMAL_SITE]},
        status_code=200,
    )
    client = SimpleHydrometrieClient()
    sites = client.get_sites_by_department("95", size=1)
    assert len(sites) > 0
    assert hasattr(sites[0], "libelle_site")


def test_simple_client_stations_by_commune_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/referentiel/stations.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = SimpleHydrometrieClient()
    stations = client.get_stations_by_commune("75056", size=1)
    assert len(stations) > 0
    assert hasattr(stations[0], "libelle_station")


def test_simple_client_observations_by_station_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/observations_tr.*"),
        json={"count": 1, "data": [MINIMAL_OBSERVATION_TR]},
        status_code=200,
    )
    client = SimpleHydrometrieClient()
    obs = client.get_observations_by_station("Y120201001", size=1)
    assert len(obs) > 0
    assert hasattr(obs[0], "date_obs")


def test_simple_client_observations_elab_by_station_mocked(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/hydrometrie/obs_elab.*"),
        json={"count": 1, "data": [MINIMAL_OBS_ELAB]},
        status_code=200,
    )
    client = SimpleHydrometrieClient()
    obs = client.get_observations_elab_by_station("Y390001001", size=1)
    assert len(obs) > 0
    assert hasattr(obs[0], "date_obs_elab")


# ==============================================================================
# 2. LIVE INTEGRATION TESTS (Real network calls, marked as 'live')
# ==============================================================================


@pytest.mark.live
def test_station_model_validation() -> None:
    from hubeau_data.api.hydrometrie import HydrometrieAPI
    from hubeau_data.models.hydrometrie import StationParams

    api = HydrometrieAPI()
    stations = api.get_stations(
        params=StationParams(code_commune_station="75056", size=1)
    )
    for s in stations:
        assert isinstance(s, Station)


@pytest.mark.live
def test_site_model_validation() -> None:
    from hubeau_data.api.hydrometrie import HydrometrieAPI
    from hubeau_data.models.hydrometrie import SiteParams

    api = HydrometrieAPI()
    sites = api.get_sites(params=SiteParams(code_departement=["95"], size=1))
    for s in sites:
        assert isinstance(s, Site)


@pytest.mark.live
def test_observation_tr_model_validation() -> None:
    from hubeau_data.api.hydrometrie import HydrometrieAPI
    from hubeau_data.models.hydrometrie import ObservationTrParams

    api = HydrometrieAPI()
    obs = api.get_observations_tr(
        params=ObservationTrParams(code_station=["Y120201001"], size=1)
    )
    for o in obs:
        assert isinstance(o, ObservationTr)


@pytest.mark.live
def test_obs_elab_model_validation() -> None:
    from hubeau_data.api.hydrometrie import HydrometrieAPI
    from hubeau_data.models.hydrometrie import ObsElabParams

    api = HydrometrieAPI()
    obs = api.get_obs_elab(
        params=ObsElabParams(
            code_station=["Y390001001"], grandeur_hydro_elab="QmM", size=1
        )
    )
    for o in obs:
        assert isinstance(o, ObsElab)


@pytest.mark.live
def test_simple_client_sites_by_department() -> None:
    sites = SimpleHydrometrieClient().get_sites_by_department("95", size=1)
    assert len(sites) > 0
    assert hasattr(sites[0], "libelle_site")


@pytest.mark.live
def test_simple_client_stations_by_commune() -> None:
    stations = SimpleHydrometrieClient().get_stations_by_commune("75056", size=1)
    assert len(stations) > 0
    assert hasattr(stations[0], "libelle_station")


@pytest.mark.live
def test_simple_client_observations_by_station() -> None:
    obs = SimpleHydrometrieClient().get_observations_by_station("Y120201001", size=1)
    assert len(obs) > 0
    assert hasattr(obs[0], "date_obs")


@pytest.mark.live
def test_simple_client_observations_elab_by_station() -> None:
    obs = SimpleHydrometrieClient().get_observations_elab_by_station(
        "Y390001001", size=1
    )
    assert len(obs) > 0
    assert hasattr(obs[0], "date_obs_elab")
