"""
Tests for the Poisson API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.poisson import (
    IndicateurPoisson,
    ObservationPoisson,
    OperationPoisson,
    StationPoisson,
)


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_STATION = {"code_station": "01000001"}
MINIMAL_INDICATEUR = {
    "code_station": "01000001",
    "date_operation": "2024-06-01T00:00:00Z",
    "ipr_note": 5.2,
    "ipr_code_classe": "1",
    "ipr_libelle_classe": "Très bon",
}
MINIMAL_OBSERVATION = {
    "code_station": "01000001",
    "date_operation": "2024-06-01T00:00:00Z",
    "nom_latin_taxon": "Salmo trutta",
    "nom_commun_taxon": "Truite fario",
}
MINIMAL_OPERATION = {
    "code_operation": 12345,
    "code_station": "01000001",
    "date_operation": "2024-06-01T00:00:00Z",
    "protocole_peche": "Pêche complète à un ou plusieurs passages",
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/etat_piscicole/stations.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = HubeauClient()
    stations = client.poisson.get_stations()
    assert isinstance(stations, PagedResponse)
    assert len(stations.data) == 1
    assert isinstance(stations.data[0], StationPoisson)
    assert stations.data[0].code_station == "01000001"


def test_get_indicateurs_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/etat_piscicole/indicateurs.*"),
        json={"count": 1, "data": [MINIMAL_INDICATEUR]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.poisson import IndicateurPoissonParams

    indicateurs = client.poisson.get_indicateurs(
        params=IndicateurPoissonParams(code_station=["01000001"], size=1)
    )
    assert isinstance(indicateurs, PagedResponse)
    assert len(indicateurs.data) == 1
    assert isinstance(indicateurs.data[0], IndicateurPoisson)
    assert indicateurs.data[0].ipr_libelle_classe == "Très bon"


def test_get_observations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/etat_piscicole/observations.*"),
        json={"count": 1, "data": [MINIMAL_OBSERVATION]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.poisson import ObservationPoissonParams

    obs = client.poisson.get_observations(
        params=ObservationPoissonParams(code_station=["01000001"], size=1)
    )
    assert isinstance(obs, PagedResponse)
    assert len(obs.data) == 1
    assert isinstance(obs.data[0], ObservationPoisson)
    assert obs.data[0].nom_latin_taxon == "Salmo trutta"


def test_get_operations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/etat_piscicole/operations.*"),
        json={"count": 1, "data": [MINIMAL_OPERATION]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.poisson import OperationPoissonParams

    ops = client.poisson.get_operations(
        params=OperationPoissonParams(code_station=["01000001"], size=1)
    )
    assert isinstance(ops, PagedResponse)
    assert len(ops.data) == 1
    assert isinstance(ops.data[0], OperationPoisson)
    assert ops.data[0].protocole_peche == "Pêche complète à un ou plusieurs passages"


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_stations_live() -> None:
    from hubeau_data.models.poisson import StationPoissonParams

    stations = HubeauClient().poisson.get_stations(
        params=StationPoissonParams(code_departement=["01"], size=1)
    )
    assert isinstance(stations, PagedResponse)
    if stations.data:
        assert isinstance(stations.data[0], StationPoisson)


@pytest.mark.live
def test_get_indicateurs_live() -> None:
    from hubeau_data.models.poisson import IndicateurPoissonParams, StationPoissonParams

    stations = HubeauClient().poisson.get_stations(
        params=StationPoissonParams(code_departement=["01"], size=1)
    )
    if not stations.data or not stations.data[0].code_station:
        pytest.skip("No station available")
    indicateurs = HubeauClient().poisson.get_indicateurs(
        params=IndicateurPoissonParams(
            code_station=[stations.data[0].code_station], size=1
        )
    )
    assert isinstance(indicateurs, PagedResponse)
    if indicateurs.data:
        assert isinstance(indicateurs.data[0], IndicateurPoisson)


@pytest.mark.live
def test_get_observations_live() -> None:
    from hubeau_data.models.poisson import (
        ObservationPoissonParams,
        StationPoissonParams,
    )

    stations = HubeauClient().poisson.get_stations(
        params=StationPoissonParams(code_departement=["01"], size=1)
    )
    if not stations.data or not stations.data[0].code_station:
        pytest.skip("No station available")
    obs = HubeauClient().poisson.get_observations(
        params=ObservationPoissonParams(
            code_station=[stations.data[0].code_station], size=1
        )
    )
    assert isinstance(obs, PagedResponse)
    if obs.data:
        assert isinstance(obs.data[0], ObservationPoisson)


@pytest.mark.live
def test_get_operations_live() -> None:
    from hubeau_data.models.poisson import OperationPoissonParams, StationPoissonParams

    stations = HubeauClient().poisson.get_stations(
        params=StationPoissonParams(code_departement=["01"], size=1)
    )
    if not stations.data or not stations.data[0].code_station:
        pytest.skip("No station available")
    ops = HubeauClient().poisson.get_operations(
        params=OperationPoissonParams(
            code_station=[stations.data[0].code_station], size=1
        )
    )
    assert isinstance(ops, PagedResponse)
    if ops.data:
        assert isinstance(ops.data[0], OperationPoisson)
