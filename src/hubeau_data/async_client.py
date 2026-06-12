"""Async client for Hub'Eau APIs."""

from types import TracebackType
from typing import Optional, Type

import httpx

from hubeau_data.api.async_hydrometrie import AsyncHydrometrieAPI


class AsyncHubeauClient:
    """
    Async entry point for Hub'Eau APIs.

    Usage:
        async with AsyncHubeauClient() as client:
            sites = await client.hydrometrie.get_sites()
    """

    def __init__(self) -> None:
        self._http_client = httpx.AsyncClient()
        self.hydrometrie = AsyncHydrometrieAPI(self._http_client)

    async def __aenter__(self) -> "AsyncHubeauClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._http_client.aclose()
