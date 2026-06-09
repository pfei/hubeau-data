"""
WARNING: These tests include real API calls (marked as live) and mocked tests.
To run only the fast mocked tests:
    poetry run pytest -m "not live"

To run the live integration tests:
    poetry run pytest -m "live" -s
"""

import re

import httpx
import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.qualite_rivieres import AnalysePc, StationPc


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print(
        "\n[INFO] Live tests make real API calls and may be slow. "
        "If you experience timeouts, check your network connection or try again later."
    )


# ==============================================================================
# 1. MOCKED TESTS (Fast, deterministic, safe for CI)
# ==============================================================================


def test_get_stations_mocked(httpx_mock: HTTPXMock) -> None:
    """Test get_stations using a mocked HTTP response."""
    mocked_response = {
        "count": 1,
        "data": [
            {
                "code_station": "01001000",
                "libelle_commune": "Paris",
                "libelle_station": "Station Seine Paris",
            }
        ],
    }

    # Use a regex pattern to match the endpoint regardless of query parameters order
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/qualite_rivieres/station_pc.*"),
        json=mocked_response,
        status_code=200,
    )

    client = HubeauClient()
    stations = client.qualite_rivieres.get_stations(libelle_commune="Paris", size=1)

    assert isinstance(stations, list)
    assert len(stations) == 1
    assert stations[0].code_station == "01001000"


def test_get_analyses_mocked(httpx_mock: HTTPXMock) -> None:
    """Test get_analyses using a mocked HTTP response."""
    mocked_response = {
        "count": 1,
        "data": [
            {
                "code_station": "01001000",
                "date_prelevement": "2026-05-28",
                "libelle_parametre": "Nitrates",
                "resultat": 12.5,
                "libelle_station": "Station Seine Paris",
            }
        ],
    }

    # Use a regex pattern to match the endpoint regardless of query parameters order
    httpx_mock.add_response(
        url=re.compile(r".*/api/v2/qualite_rivieres/analyse_pc.*"),
        json=mocked_response,
        status_code=200,
    )

    client = HubeauClient()
    analyses = client.qualite_rivieres.get_analyses(
        code_station="01001000", size=1, max_records=1
    )

    assert isinstance(analyses, list)
    assert len(analyses) == 1
    assert analyses[0].libelle_parametre == "Nitrates"


# ==============================================================================
# 2. LIVE INTEGRATION TESTS (Real network calls, marked as 'live')
# ==============================================================================


@pytest.mark.live
def test_get_stations_live() -> None:
    """Perform a real API call to verify the station endpoint data structure."""
    client = HubeauClient()
    stations = client.qualite_rivieres.get_stations(libelle_commune="Paris", size=1)
    assert isinstance(stations, list)
    if stations:
        assert isinstance(stations[0], StationPc)
        assert hasattr(stations[0], "code_station")
        assert hasattr(stations[0], "libelle_station")


@pytest.mark.live
@pytest.mark.xfail(
    reason=(
        "Qualité Rivières API has known stability issues (timeouts, ~60% error rate)"
    ),
    raises=httpx.ReadTimeout,
    strict=False,
)
def test_get_analyses_live() -> None:
    """Perform a real API call to verify the analysis endpoint data structure."""
    client = HubeauClient()
    stations = client.qualite_rivieres.get_stations(libelle_commune="Paris", size=1)
    if not stations:
        pytest.skip("No stations available for testing")
    analyses = client.qualite_rivieres.get_analyses(
        code_station=stations[0].code_station, size=1, max_records=1
    )
    assert isinstance(analyses, list)
    if analyses:
        assert isinstance(analyses[0], AnalysePc)
        assert hasattr(analyses[0], "code_station")
        assert hasattr(analyses[0], "libelle_station")
        assert hasattr(analyses[0], "libelle_parametre")
