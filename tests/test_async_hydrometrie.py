"""
Tests for AsyncHydrometrieAPI / AsyncHubeauClient.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import asyncio
import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.async_client import AsyncHubeauClient
from hubeau_data.models.hydrometrie import ObservationTrParams, Site, SiteParams

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


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


@pytest.mark.anyio
async def test_get_sites_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v2/hydrometrie/referentiel/sites.*"),
        json={"count": 1, "data": [MINIMAL_SITE]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        sites = await client.hydrometrie.get_sites()
    assert isinstance(sites, list)
    assert len(sites) == 1
    assert isinstance(sites[0], Site)
    assert sites[0].code_site == "A1234567"


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
@pytest.mark.anyio
async def test_get_sites_live() -> None:
    async with AsyncHubeauClient() as client:
        sites = await client.hydrometrie.get_sites(
            params=SiteParams(code_departement=["75"], size=1)
        )
    assert isinstance(sites, list)


@pytest.mark.live
@pytest.mark.anyio
async def test_parallel_fetch_live() -> None:
    """The actual value proposition: fetch multiple stations in parallel."""
    async with AsyncHubeauClient() as client:
        codes = ["Y120201001", "K418001001"]
        tasks = [
            client.hydrometrie.get_observations_tr(
                params=ObservationTrParams(code_station=[c], size=1)
            )
            for c in codes
        ]
        results = await asyncio.gather(*tasks)
    assert len(results) == 2
    for obs in results:
        assert isinstance(obs, list)
