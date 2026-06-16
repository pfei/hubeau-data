"""
Tests for the tenacity retry logic in HubeauBaseAPI._get().

These tests verify that:
- Transient errors (503, ReadTimeout) trigger retries
- Non-transient errors (404) are raised immediately
- After max retries, the exception is reraised
"""

import re
from unittest.mock import patch

import httpx
import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient

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

SITES_URL = re.compile(r".*/api/v2/hydrometrie/referentiel/sites.*")


def test_retry_on_503_succeeds_on_third_attempt(httpx_mock: HTTPXMock) -> None:
    """503 twice then success — retry should recover."""
    with patch("tenacity.nap.time.sleep"):
        httpx_mock.add_response(status_code=503)
        httpx_mock.add_response(status_code=503)
        httpx_mock.add_response(
            url=SITES_URL,
            json={"count": 1, "data": [MINIMAL_SITE]},
            status_code=200,
        )
        client = HubeauClient()
        sites = client.hydrometrie.get_sites()
        assert len(sites.data) == 1
        assert sites.data[0].code_site == "A1234567"


def test_retry_on_read_timeout_succeeds_on_third_attempt(httpx_mock: HTTPXMock) -> None:
    """ReadTimeout twice then success — retry should recover."""
    with patch("tenacity.nap.time.sleep"):
        httpx_mock.add_exception(httpx.ReadTimeout("timeout"))
        httpx_mock.add_exception(httpx.ReadTimeout("timeout"))
        httpx_mock.add_response(
            url=SITES_URL,
            json={"count": 1, "data": [MINIMAL_SITE]},
            status_code=200,
        )
        client = HubeauClient()
        sites = client.hydrometrie.get_sites()
        assert len(sites.data) == 1


def test_no_retry_on_404(httpx_mock: HTTPXMock) -> None:
    """404 is a client error — should raise immediately, no retry."""
    with patch("tenacity.nap.time.sleep"):
        httpx_mock.add_response(status_code=404)
        client = HubeauClient()
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            client.hydrometrie.get_sites()
        assert exc_info.value.response.status_code == 404
        # Only 1 request should have been made
        assert len(httpx_mock.get_requests()) == 1


def test_reraises_after_max_retries(httpx_mock: HTTPXMock) -> None:
    """3 consecutive 503s — should reraise after exhausting retries."""
    with patch("tenacity.nap.time.sleep"):
        httpx_mock.add_response(status_code=503)
        httpx_mock.add_response(status_code=503)
        httpx_mock.add_response(status_code=503)
        client = HubeauClient()
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            client.hydrometrie.get_sites()
        assert exc_info.value.response.status_code == 503
        assert len(httpx_mock.get_requests()) == 3
