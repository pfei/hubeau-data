"""
Tests for the Piézométrie API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.piezometrie import (
    ChroniquePiezo,
    ChroniquePiezoTr,
    StationPiezo,
)


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_STATION = {
    "bss_id": "BSS001ABCD",
}

MINIMAL_CHRONIQUE = {
    "bss_id": "BSS001ABCD",
    "date_mesure": "2024-01-15",
    "niveau_nappe_eau": 12.5,
}


MINIMAL_CHRONIQUE_TR = {
    "bss_id": "BSS001ABCD",
    "date_mesure": "2026-06-01",
    "niveau_eau_ngf": 45.2,
}

# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/niveaux_nappes/stations.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = HubeauClient()
    stations = client.piezometrie.get_stations()
    assert isinstance(stations, PagedResponse)
    assert len(stations.data) == 1
    assert isinstance(stations.data[0], StationPiezo)
    assert stations.data[0].bss_id == "BSS001ABCD"


def test_get_chroniques_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/niveaux_nappes/chroniques.*"),
        json={"count": 1, "data": [MINIMAL_CHRONIQUE]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.piezometrie import ChroniquePiezoParams

    chroniques = client.piezometrie.get_chroniques(
        params=ChroniquePiezoParams(bss_id=["BSS001ABCD"], size=1)
    )
    assert isinstance(chroniques, PagedResponse)
    assert len(chroniques.data) == 1
    assert isinstance(chroniques.data[0], ChroniquePiezo)
    assert chroniques.data[0].date_mesure == "2024-01-15"


def test_get_chroniques_tr_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/niveaux_nappes/chroniques_tr.*"),
        json={"count": 1, "data": [MINIMAL_CHRONIQUE_TR]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.piezometrie import ChroniquePiezoTrParams

    chroniques = client.piezometrie.get_chroniques_tr(
        params=ChroniquePiezoTrParams(bss_id=["BSS001ABCD"], size=1)
    )
    assert isinstance(chroniques, PagedResponse)
    assert len(chroniques.data) == 1
    assert isinstance(chroniques.data[0], ChroniquePiezoTr)
    assert chroniques.data[0].niveau_eau_ngf == 45.2


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_stations_live() -> None:
    from hubeau_data.models.piezometrie import StationPiezoParams

    client = HubeauClient()
    stations = client.piezometrie.get_stations(
        params=StationPiezoParams(code_departement=["75"], size=1)
    )
    assert isinstance(stations, PagedResponse)
    if stations.data:
        assert isinstance(stations.data[0], StationPiezo)


@pytest.mark.live
def test_get_chroniques_live() -> None:
    from hubeau_data.models.piezometrie import ChroniquePiezoParams, StationPiezoParams

    client = HubeauClient()
    stations = client.piezometrie.get_stations(
        params=StationPiezoParams(code_departement=["75"], size=1)
    )
    if not stations.data or not stations.data[0].bss_id:
        pytest.skip("No station available")
    chroniques = client.piezometrie.get_chroniques(
        params=ChroniquePiezoParams(bss_id=[stations.data[0].bss_id], size=1)
    )
    assert isinstance(chroniques, PagedResponse)
    if chroniques.data:
        assert isinstance(chroniques.data[0], ChroniquePiezo)


@pytest.mark.live
def test_get_chroniques_tr_live() -> None:
    from hubeau_data.models.piezometrie import (
        ChroniquePiezoTrParams,
        StationPiezoParams,
    )

    client = HubeauClient()
    stations = client.piezometrie.get_stations(
        params=StationPiezoParams(code_departement=["75"], size=1)
    )
    if not stations.data or not stations.data[0].bss_id:
        pytest.skip("No station available")
    chroniques = client.piezometrie.get_chroniques_tr(
        params=ChroniquePiezoTrParams(bss_id=[stations.data[0].bss_id], size=1)
    )
    assert isinstance(chroniques, PagedResponse)
    if chroniques.data:
        assert isinstance(chroniques.data[0], ChroniquePiezoTr)
