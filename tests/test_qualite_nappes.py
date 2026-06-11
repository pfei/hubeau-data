"""
Tests for the Qualité des Nappes API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import httpx
import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.qualite_nappes import AnalyseNappe, StationNappe


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_STATION = {
    "bss_id": "BSS000XUUM",
}

MINIMAL_ANALYSE = {
    "bss_id": "BSS000XUUM",
    "date_debut_prelevement": "2024-01-15T00:00:00Z",
    "nom_param": "Nitrates",
    "resultat": 12.5,
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/qualite_nappes/stations.*"),
        json={"count": 1, "data": [MINIMAL_STATION]},
        status_code=200,
    )
    client = HubeauClient()
    stations = client.qualite_nappes.get_stations()
    assert isinstance(stations, list)
    assert len(stations) == 1
    assert isinstance(stations[0], StationNappe)
    assert stations[0].bss_id == "BSS000XUUM"


def test_get_analyses_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/qualite_nappes/analyses.*"),
        json={"count": 1, "data": [MINIMAL_ANALYSE]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.qualite_nappes import AnalyseNappeParams

    analyses = client.qualite_nappes.get_analyses(
        params=AnalyseNappeParams(bss_id=["BSS000XUUM"], size=1),
        max_records=1,
    )
    assert isinstance(analyses, list)
    assert len(analyses) == 1
    assert isinstance(analyses[0], AnalyseNappe)
    assert analyses[0].nom_param == "Nitrates"


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
@pytest.mark.xfail(
    reason="Qualité Nappes API has known stability issues (503, timeouts)",
    raises=httpx.HTTPStatusError,
    strict=False,
)
def test_get_stations_live() -> None:
    from hubeau_data.models.qualite_nappes import StationNappeParams

    client = HubeauClient()
    stations = client.qualite_nappes.get_stations(
        params=StationNappeParams(num_departement=["75"], size=1)
    )
    assert isinstance(stations, list)
    if stations:
        assert isinstance(stations[0], StationNappe)


@pytest.mark.live
@pytest.mark.xfail(
    reason="Qualité Nappes API has known stability issues (503, timeouts)",
    raises=httpx.HTTPStatusError,
    strict=False,
)
def test_get_analyses_live() -> None:
    from hubeau_data.models.qualite_nappes import AnalyseNappeParams, StationNappeParams

    client = HubeauClient()
    stations = client.qualite_nappes.get_stations(
        params=StationNappeParams(num_departement=["75"], size=1)
    )
    if not stations or not stations[0].bss_id:
        pytest.skip("No station available")
    analyses = client.qualite_nappes.get_analyses(
        params=AnalyseNappeParams(bss_id=[stations[0].bss_id], size=1),
        max_records=1,
    )
    assert isinstance(analyses, list)
    if analyses:
        assert isinstance(analyses[0], AnalyseNappe)
