"""
Tests for the Qualité Eau Potable API client.
To run only mocked tests: uv run pytest -m "not live"
To run live tests:        uv run pytest -m "live" -s
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.client import HubeauClient
from hubeau_data.models.eau_potable import CommuneUdi, ResultatEauPotable


@pytest.fixture(autouse=True, scope="session")
def api_test_notice() -> None:
    print("\n[INFO] Live tests make real API calls and may be slow.")


MINIMAL_COMMUNE_UDI = {
    "annee": "2024",
    "code_commune": "75056",
    "code_reseau": "075-RES-01",
    "nom_commune": "Paris",
    "nom_reseau": "Réseau Paris",
}

MINIMAL_RESULTAT = {
    "code_commune": "75056",
    "nom_commune": "Paris",
    "code_parametre": "1340",
    "libelle_parametre": "Nitrates",
    "resultat_numerique": 12.5,
    "date_prelevement": "2024-06-01T10:00:00Z",
    "conformite_limites_pc_prelevement": "C",
}


# ==============================================================================
# 1. MOCKED TESTS
# ==============================================================================


def test_get_communes_udi_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/qualite_eau_potable/communes_udi.*"),
        json={"count": 1, "data": [MINIMAL_COMMUNE_UDI]},
        status_code=200,
    )
    client = HubeauClient()
    communes = client.eau_potable.get_communes_udi()
    assert isinstance(communes, list)
    assert len(communes) == 1
    assert isinstance(communes[0], CommuneUdi)
    assert communes[0].code_commune == "75056"


def test_get_resultats_dis_mocked(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/qualite_eau_potable/resultats_dis.*"),
        json={"count": 1, "data": [MINIMAL_RESULTAT]},
        status_code=200,
    )
    client = HubeauClient()
    from hubeau_data.models.eau_potable import ResultatEauPotableParams

    resultats = client.eau_potable.get_resultats_dis(
        params=ResultatEauPotableParams(code_commune=["75056"], size=1)
    )
    assert isinstance(resultats, list)
    assert len(resultats) == 1
    assert isinstance(resultats[0], ResultatEauPotable)
    assert resultats[0].libelle_parametre == "Nitrates"


# ==============================================================================
# 2. LIVE TESTS
# ==============================================================================


@pytest.mark.live
def test_get_communes_udi_live() -> None:
    from hubeau_data.models.eau_potable import CommuneUdiParams

    communes = HubeauClient().eau_potable.get_communes_udi(
        params=CommuneUdiParams(code_commune=["75056"], size=1)
    )
    assert isinstance(communes, list)
    if communes:
        assert isinstance(communes[0], CommuneUdi)


@pytest.mark.live
def test_get_resultats_dis_live() -> None:
    from hubeau_data.models.eau_potable import ResultatEauPotableParams

    resultats = HubeauClient().eau_potable.get_resultats_dis(
        params=ResultatEauPotableParams(code_commune=["75056"], size=1)
    )
    assert isinstance(resultats, list)
    if resultats:
        assert isinstance(resultats[0], ResultatEauPotable)
