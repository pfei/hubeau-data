"""
Tests for the Hydrobiologie API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.hydrobiologie import (
    IndiceHydrobio,
    StationHydrobio,
    TaxonHydrobio,
)


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_STATION = {"code_station_hydrobio": "04001000"}
MINIMAL_INDICE = {
    "code_station_hydrobio": "04001000",
    "code_indice": "1000",
    "libelle_indice": "IBGN",
    "date_prelevement": "2024-06-01T00:00:00Z",
    "resultat_indice": 14.0,
}
MINIMAL_TAXON = {
    "code_station_hydrobio": "04001000",
    "date_prelevement": "2024-06-01T00:00:00Z",
    "code_appel_taxon": "1234",
    "libelle_appel_taxon": "Baetis rhodani",
    "resultat_taxon": 42.0,
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/hydrobio/stations_hydrobio.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = HubeauClient()
    stations = client.hydrobiologie.get_stations()
    assert isinstance(stations, list)
    assert len(stations) == 1
    assert isinstance(stations[0], StationHydrobio)
    assert stations[0].code_station_hydrobio == "04001000"


def test_get_indices_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/hydrobio/indices.*"),
        json={"count": 1, "data": [MINIMAL_INDICE]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.hydrobiologie import IndiceHydrobioParams

    indices = client.hydrobiologie.get_indices(
        params=IndiceHydrobioParams(code_station_hydrobio=["04001000"], size=1)
    )
    assert isinstance(indices, list)
    assert len(indices) == 1
    assert isinstance(indices[0], IndiceHydrobio)
    assert indices[0].libelle_indice == "IBGN"


def test_get_taxons_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/hydrobio/taxons.*"),
        json={"count": 1, "data": [MINIMAL_TAXON]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.hydrobiologie import TaxonHydrobioParams

    taxons = client.hydrobiologie.get_taxons(
        params=TaxonHydrobioParams(code_station_hydrobio=["04001000"], size=1)
    )
    assert isinstance(taxons, list)
    assert len(taxons) == 1
    assert isinstance(taxons[0], TaxonHydrobio)
    assert taxons[0].libelle_appel_taxon == "Baetis rhodani"


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_stations_live() -> None:
    from hubeau_data.models.hydrobiologie import StationHydrobioParams

    stations = HubeauClient().hydrobiologie.get_stations(
        params=StationHydrobioParams(code_departement=["01"], size=1)
    )
    assert isinstance(stations, list)
    if stations:
        assert isinstance(stations[0], StationHydrobio)


@pytest.mark.live
def test_get_indices_live() -> None:
    from hubeau_data.models.hydrobiologie import (
        IndiceHydrobioParams,
        StationHydrobioParams,
    )

    stations = HubeauClient().hydrobiologie.get_stations(
        params=StationHydrobioParams(code_departement=["01"], size=1)
    )
    if not stations or not stations[0].code_station_hydrobio:
        pytest.skip("No station available")
    indices = HubeauClient().hydrobiologie.get_indices(
        params=IndiceHydrobioParams(
            code_station_hydrobio=[stations[0].code_station_hydrobio], size=1
        )
    )
    assert isinstance(indices, list)
    if indices:
        assert isinstance(indices[0], IndiceHydrobio)


@pytest.mark.live
def test_get_taxons_live() -> None:
    from hubeau_data.models.hydrobiologie import (
        StationHydrobioParams,
        TaxonHydrobioParams,
    )

    stations = HubeauClient().hydrobiologie.get_stations(
        params=StationHydrobioParams(code_departement=["01"], size=1)
    )
    if not stations or not stations[0].code_station_hydrobio:
        pytest.skip("No station available")
    taxons = HubeauClient().hydrobiologie.get_taxons(
        params=TaxonHydrobioParams(
            code_station_hydrobio=[stations[0].code_station_hydrobio], size=1
        )
    )
    assert isinstance(taxons, list)
    if taxons:
        assert isinstance(taxons[0], TaxonHydrobio)
