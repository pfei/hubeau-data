"""
Tests for the Température API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import httpx
import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.temperature import ChroniqueTemperature, StationTemperature


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_STATION = {"code_station": "04001000"}
MINIMAL_CHRONIQUE = {
    "code_station": "04001000",
    "date_mesure_temp": "2024-06-01",
    "heure_mesure_temp": "12:00:00",
    "resultat": 18.5,
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/temperature/station.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = HubeauClient()
    stations = client.temperature.get_stations()
    assert isinstance(stations, PagedResponse)
    assert len(stations.data) == 1
    assert isinstance(stations.data[0], StationTemperature)
    assert stations.data[0].code_station == "04001000"


def test_get_chronique_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/temperature/chronique.*"),
        json={"count": 1, "data": [MINIMAL_CHRONIQUE]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.temperature import ChroniqueTemperatureParams

    chronique = client.temperature.get_chronique(
        params=ChroniqueTemperatureParams(code_station=["04001000"], size=1)
    )
    assert isinstance(chronique, PagedResponse)
    assert len(chronique.data) == 1
    assert isinstance(chronique.data[0], ChroniqueTemperature)
    assert chronique.data[0].resultat == 18.5


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_stations_live() -> None:
    from hubeau_data.models.temperature import StationTemperatureParams

    stations = HubeauClient().temperature.get_stations(
        params=StationTemperatureParams(code_departement=["01"], size=1)
    )
    assert isinstance(stations, PagedResponse)
    if stations.data:
        assert isinstance(stations.data[0], StationTemperature)


@pytest.mark.live
@pytest.mark.xfail(
    reason="Température API chronique endpoint has known timeout issues",
    raises=httpx.ReadTimeout,
    strict=False,
)
def test_get_chronique_live() -> None:
    from hubeau_data.models.temperature import (
        ChroniqueTemperatureParams,
        StationTemperatureParams,
    )

    stations = HubeauClient().temperature.get_stations(
        params=StationTemperatureParams(code_departement=["01"], size=1)
    )
    if not stations.data or not stations.data[0].code_station:
        pytest.skip("No station available")
    chronique = HubeauClient().temperature.get_chronique(
        params=ChroniqueTemperatureParams(
            code_station=[stations.data[0].code_station], size=1
        )
    )
    assert isinstance(chronique, PagedResponse)
    if chronique.data:
        assert isinstance(chronique.data[0], ChroniqueTemperature)
