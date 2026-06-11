"""
Tests for the Phytopharmaceutiques API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.phytopharmaceutiques import (
    AchatProduit,
    AchatSubstance,
    VenteProduit,
    VenteSubstance,
)


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_ACHAT_SUBSTANCE = {
    "annee": 2022,
    "libelle_substance": "Glyphosate",
    "code_cas": "1071-83-6",
    "quantite": 5000.0,
    "type_territoire": "National",
}
MINIMAL_ACHAT_PRODUIT = {
    "annee": 2022,
    "amm": "2090069",
    "quantite": 1200.0,
    "type_territoire": "National",
    "unite": "kg",
}
MINIMAL_VENTE_SUBSTANCE = {
    "annee": 2022,
    "libelle_substance": "Glyphosate",
    "quantite": 8000.0,
    "type_territoire": "National",
}
MINIMAL_VENTE_PRODUIT = {
    "annee": 2022,
    "amm": "2090069",
    "quantite": 2000.0,
    "type_territoire": "National",
    "unite": "kg",
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_achats_substances_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/achats/substances.*"),
        json={"count": 1, "data": [MINIMAL_ACHAT_SUBSTANCE]},
        status_code=200,
    )
    client = HubeauClient()
    resultats = client.phytopharmaceutiques.get_achats_substances()
    assert isinstance(resultats, list)
    assert len(resultats) == 1
    assert isinstance(resultats[0], AchatSubstance)
    assert resultats[0].libelle_substance == "Glyphosate"


def test_get_achats_produits_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/achats/produits.*"),
        json={"count": 1, "data": [MINIMAL_ACHAT_PRODUIT]},
        status_code=200,
    )
    client = HubeauClient()
    resultats = client.phytopharmaceutiques.get_achats_produits()
    assert isinstance(resultats, list)
    assert len(resultats) == 1
    assert isinstance(resultats[0], AchatProduit)
    assert resultats[0].unite == "kg"


def test_get_ventes_substances_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/ventes/substances.*"),
        json={"count": 1, "data": [MINIMAL_VENTE_SUBSTANCE]},
        status_code=200,
    )
    client = HubeauClient()
    resultats = client.phytopharmaceutiques.get_ventes_substances()
    assert isinstance(resultats, list)
    assert len(resultats) == 1
    assert isinstance(resultats[0], VenteSubstance)
    assert resultats[0].libelle_substance == "Glyphosate"


def test_get_ventes_produits_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/ventes/produits.*"),
        json={"count": 1, "data": [MINIMAL_VENTE_PRODUIT]},
        status_code=200,
    )
    client = HubeauClient()
    resultats = client.phytopharmaceutiques.get_ventes_produits()
    assert isinstance(resultats, list)
    assert len(resultats) == 1
    assert isinstance(resultats[0], VenteProduit)
    assert resultats[0].annee == 2022


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_achats_substances_live() -> None:
    from hubeau_data.models.phytopharmaceutiques import AchatSubstanceParams

    resultats = HubeauClient().phytopharmaceutiques.get_achats_substances(
        params=AchatSubstanceParams(type_territoire="National", size=1)
    )
    assert isinstance(resultats, list)
    if resultats:
        assert isinstance(resultats[0], AchatSubstance)


@pytest.mark.live
def test_get_ventes_substances_live() -> None:
    from hubeau_data.models.phytopharmaceutiques import VenteSubstanceParams

    resultats = HubeauClient().phytopharmaceutiques.get_ventes_substances(
        params=VenteSubstanceParams(type_territoire="National", size=1)
    )
    assert isinstance(resultats, list)
    if resultats:
        assert isinstance(resultats[0], VenteSubstance)
