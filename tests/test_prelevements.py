"""
Tests for the Prélèvements API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import httpx
import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.prelevements import (
    ChroniquePrelevement,
    OuvragePrelevement,
    PointPrelevement,
)


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_OUVRAGE = {"code_ouvrage": "OPR0000000001"}
MINIMAL_POINT = {"code_point_prelevement": "PTP000000000000001"}
MINIMAL_CHRONIQUE = {
    "code_ouvrage": "OPR0000000001",
    "annee": 2022,
    "volume": 150000.0,
    "code_usage": "AEP",
    "libelle_usage": "Alimentation en eau potable",
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_ouvrages_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/prelevements/referentiel/ouvrages.*"),
        json={"count": 1, "data": [MINIMAL_OUVRAGE]},
        status_code=200,
    )
    client = HubeauClient()
    ouvrages = client.prelevements.get_ouvrages()
    assert isinstance(ouvrages, list)
    assert len(ouvrages) == 1
    assert isinstance(ouvrages[0], OuvragePrelevement)
    assert ouvrages[0].code_ouvrage == "OPR0000000001"


def test_get_points_prelevement_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/prelevements/referentiel/points_prelevement.*"),
        json={"count": 1, "data": [MINIMAL_POINT]},
        status_code=200,
    )
    client = HubeauClient()
    points = client.prelevements.get_points_prelevement()
    assert isinstance(points, list)
    assert len(points) == 1
    assert isinstance(points[0], PointPrelevement)
    assert points[0].code_point_prelevement == "PTP000000000000001"


def test_get_chroniques_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/prelevements/chroniques.*"),
        json={"count": 1, "data": [MINIMAL_CHRONIQUE]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.prelevements import ChroniquePrelevementParams

    chroniques = client.prelevements.get_chroniques(
        params=ChroniquePrelevementParams(code_ouvrage=["OPR0000000001"], size=1)
    )
    assert isinstance(chroniques, list)
    assert len(chroniques) == 1
    assert isinstance(chroniques[0], ChroniquePrelevement)
    assert chroniques[0].annee == 2022


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_ouvrages_live() -> None:
    from hubeau_data.models.prelevements import OuvrageParams

    ouvrages = HubeauClient().prelevements.get_ouvrages(
        params=OuvrageParams(code_departement=["75"], size=1)
    )
    assert isinstance(ouvrages, list)
    if ouvrages:
        assert isinstance(ouvrages[0], OuvragePrelevement)


@pytest.mark.live
def test_get_points_prelevement_live() -> None:
    from hubeau_data.models.prelevements import PointPrelevementParams

    points = HubeauClient().prelevements.get_points_prelevement(
        params=PointPrelevementParams(code_departement=["75"], size=1)
    )
    assert isinstance(points, list)
    if points:
        assert isinstance(points[0], PointPrelevement)


@pytest.mark.live
@pytest.mark.xfail(
    reason="Prélèvements API chroniques endpoint has known timeout issues",
    raises=httpx.ReadTimeout,
    strict=False,
)
def test_get_chroniques_live() -> None:
    from hubeau_data.models.prelevements import (
        ChroniquePrelevementParams,
        OuvrageParams,
    )

    ouvrages = HubeauClient().prelevements.get_ouvrages(
        params=OuvrageParams(code_departement=["75"], size=1)
    )
    if not ouvrages or not ouvrages[0].code_ouvrage:
        pytest.skip("No ouvrage available")
    chroniques = HubeauClient().prelevements.get_chroniques(
        params=ChroniquePrelevementParams(
            code_ouvrage=[ouvrages[0].code_ouvrage], size=1
        )
    )
    assert isinstance(chroniques, list)
    if chroniques:
        assert isinstance(chroniques[0], ChroniquePrelevement)
