"""
Lightweight mocked tests for all Async*API clients.
Validates the async wiring (AsyncClient, await, response parsing) for each API.
Business logic is already covered by the sync test suites.
"""

import re

import pytest
from pytest_httpx import HTTPXMock

from hubeau_data.async_client import AsyncHubeauClient


@pytest.mark.anyio
async def test_async_qualite_rivieres(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v2/qualite_rivieres/station_pc.*"),
        json={"count": 1, "data": [{"code_station": "01000001"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        stations = await client.qualite_rivieres.get_stations()
    assert len(stations.data) == 1
    assert stations.data[0].code_station == "01000001"


@pytest.mark.anyio
async def test_async_piezometrie(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/niveaux_nappes/stations.*"),
        json={"count": 1, "data": [{"bss_id": "BSS001ABCD"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        stations = await client.piezometrie.get_stations()
    assert len(stations.data) == 1
    assert stations.data[0].bss_id == "BSS001ABCD"


@pytest.mark.anyio
async def test_async_qualite_nappes(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/qualite_nappes/stations.*"),
        json={"count": 1, "data": [{"bss_id": "BSS001ABCD"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        stations = await client.qualite_nappes.get_stations()
    assert len(stations.data) == 1


@pytest.mark.anyio
async def test_async_ecoulement(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/ecoulement/stations.*"),
        json={"count": 1, "data": [{"code_station": "A1000600"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        stations = await client.ecoulement.get_stations()
    assert len(stations.data) == 1


@pytest.mark.anyio
async def test_async_temperature(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/temperature/station.*"),
        json={"count": 1, "data": [{"code_station": "04001000"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        stations = await client.temperature.get_stations()
    assert len(stations.data) == 1


@pytest.mark.anyio
async def test_async_prelevements(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/prelevements/referentiel/ouvrages.*"),
        json={"count": 1, "data": [{"code_ouvrage": "OPR0000000001"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        ouvrages = await client.prelevements.get_ouvrages()
    assert len(ouvrages.data) == 1


@pytest.mark.anyio
async def test_async_hydrobiologie(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/hydrobio/stations_hydrobio.*"),
        json={"count": 1, "data": [{"code_station_hydrobio": "04001000"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        stations = await client.hydrobiologie.get_stations()
    assert len(stations.data) == 1


@pytest.mark.anyio
async def test_async_poisson(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/etat_piscicole/stations.*"),
        json={"count": 1, "data": [{"code_station": "01000001"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        stations = await client.poisson.get_stations()
    assert len(stations.data) == 1


@pytest.mark.anyio
async def test_async_eau_potable(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/v1/qualite_eau_potable/communes_udi.*"),
        json={"count": 1, "data": [{"code_commune": "75056"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        communes = await client.eau_potable.get_communes_udi()
    assert len(communes.data) == 1


@pytest.mark.anyio
async def test_async_phytopharmaceutiques(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url=re.compile(r".*/achats/substances.*"),
        json={"count": 1, "data": [{"annee": 2022, "libelle_substance": "Glyphosate"}]},
        status_code=200,
    )
    async with AsyncHubeauClient() as client:
        resultats = await client.phytopharmaceutiques.get_achats_substances()
    assert len(resultats.data) == 1
