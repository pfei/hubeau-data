"""
Tests for the Écoulement API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.ecoulement import (
    CampagneEcoulement,
    ObservationEcoulement,
    StationEcoulement,
)
from hubeau_data.models.pagination import PagedResponse


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_STATION = {"code_station": "A1000600"}
MINIMAL_OBSERVATION = {
    "code_station": "A1000600",
    "date_observation": "2024-06-01T00:00:00Z",
    "code_ecoulement": "1",
    "libelle_ecoulement": "Ecoulement visible",
}
MINIMAL_CAMPAGNE = {
    "code_campagne": 1,
    "date_campagne": "2024-06-01T00:00:00Z",
    "code_type_campagne": 1,
    "libelle_type_campagne": "Usuelle",
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/ecoulement/stations.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = HubeauClient()
    stations = client.ecoulement.get_stations()
    assert isinstance(stations, PagedResponse)
    assert len(stations.data) == 1
    assert isinstance(stations.data[0], StationEcoulement)
    assert stations.data[0].code_station == "A1000600"


def test_get_observations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/ecoulement/observations.*"),
        json={"count": 1, "data": [MINIMAL_OBSERVATION]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.ecoulement import ObservationEcoulementParams

    obs = client.ecoulement.get_observations(
        params=ObservationEcoulementParams(code_station=["A1000600"], size=1)
    )
    assert isinstance(obs, PagedResponse)
    assert len(obs.data) == 1
    assert isinstance(obs.data[0], ObservationEcoulement)
    assert obs.data[0].code_ecoulement == "1"


def test_get_campagnes_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/ecoulement/campagnes.*"),
        json={"count": 1, "data": [MINIMAL_CAMPAGNE]},
        status_code=200,
    )
    client = HubeauClient()
    campagnes = client.ecoulement.get_campagnes()
    assert isinstance(campagnes, PagedResponse)
    assert len(campagnes.data) == 1
    assert isinstance(campagnes.data[0], CampagneEcoulement)
    assert campagnes.data[0].libelle_type_campagne == "Usuelle"


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_stations_live() -> None:
    from hubeau_data.models.ecoulement import StationEcoulementParams

    stations = HubeauClient().ecoulement.get_stations(
        params=StationEcoulementParams(code_departement=["75"], size=1)
    )
    assert isinstance(stations, PagedResponse)
    if stations.data:
        assert isinstance(stations.data[0], StationEcoulement)


@pytest.mark.live
def test_get_observations_live() -> None:
    from hubeau_data.models.ecoulement import (
        ObservationEcoulementParams,
        StationEcoulementParams,
    )

    stations = HubeauClient().ecoulement.get_stations(
        params=StationEcoulementParams(code_departement=["75"], size=1)
    )
    if not stations.data or not stations.data[0].code_station:
        pytest.skip("No station available")
    obs = HubeauClient().ecoulement.get_observations(
        params=ObservationEcoulementParams(
            code_station=[stations.data[0].code_station], size=1
        )
    )
    assert isinstance(obs, PagedResponse)
    if obs.data:
        assert isinstance(obs.data[0], ObservationEcoulement)


@pytest.mark.live
def test_get_campagnes_live() -> None:
    from hubeau_data.models.ecoulement import CampagneEcoulementParams

    campagnes = HubeauClient().ecoulement.get_campagnes(
        params=CampagneEcoulementParams(size=1)
    )
    assert isinstance(campagnes, PagedResponse)
    if campagnes.data:
        assert isinstance(campagnes.data[0], CampagneEcoulement)
