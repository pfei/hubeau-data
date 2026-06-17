"""Async client for Hub'Eau APIs."""

from types import TracebackType
from typing import Optional, Type

import httpx

from hubeau_data.api.async_eau_potable import AsyncEauPotableAPI
from hubeau_data.api.async_ecoulement import AsyncEcoulementAPI
from hubeau_data.api.async_hydrobiologie import AsyncHydrobiologieAPI
from hubeau_data.api.async_hydrometrie import AsyncHydrometrieAPI
from hubeau_data.api.async_phytopharmaceutiques import AsyncPhytopharmaceutiquesAPI
from hubeau_data.api.async_piezometrie import AsyncPiezometrieAPI
from hubeau_data.api.async_poisson import AsyncPoissonAPI
from hubeau_data.api.async_prelevements import AsyncPrelevementsAPI
from hubeau_data.api.async_qualite_nappes import AsyncQualiteNappesAPI
from hubeau_data.api.async_qualite_rivieres import AsyncQualiteRivieresAPI
from hubeau_data.api.async_temperature import AsyncTemperatureAPI
from hubeau_data.async_base import AsyncHubeauBaseAPI


class AsyncHubeauClient:
    """
    Async entry point for Hub'Eau APIs.

    Usage:
        async with AsyncHubeauClient() as client:
            sites = await client.hydrometrie.get_sites()
    """

    def __init__(
        self, max_concurrent: int = AsyncHubeauBaseAPI.DEFAULT_MAX_CONCURRENT
    ) -> None:
        self._http_client = httpx.AsyncClient()
        self.hydrometrie = AsyncHydrometrieAPI(self._http_client, max_concurrent)
        self.qualite_rivieres = AsyncQualiteRivieresAPI(
            self._http_client, max_concurrent
        )
        self.piezometrie = AsyncPiezometrieAPI(self._http_client, max_concurrent)
        self.qualite_nappes = AsyncQualiteNappesAPI(self._http_client, max_concurrent)
        self.ecoulement = AsyncEcoulementAPI(self._http_client, max_concurrent)
        self.temperature = AsyncTemperatureAPI(self._http_client, max_concurrent)
        self.prelevements = AsyncPrelevementsAPI(self._http_client, max_concurrent)
        self.hydrobiologie = AsyncHydrobiologieAPI(self._http_client, max_concurrent)
        self.poisson = AsyncPoissonAPI(self._http_client, max_concurrent)
        self.eau_potable = AsyncEauPotableAPI(self._http_client, max_concurrent)
        self.phytopharmaceutiques = AsyncPhytopharmaceutiquesAPI(
            self._http_client, max_concurrent
        )

    async def __aenter__(self) -> "AsyncHubeauClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._http_client.aclose()
