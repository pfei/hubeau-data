"""Async base class for Hub'Eau API clients."""

import asyncio
from typing import Any

import httpx

from hubeau_data.retry import hubeau_retry


class AsyncHubeauBaseAPI:
    """
    Async base class providing a shared httpx.AsyncClient with retry logic.

    Usage:
        async with AsyncHubeauClient() as client:
            sites = await client.hydrometrie.get_sites()
    """

    DEFAULT_TIMEOUT: float = 30.0
    DEFAULT_MAX_CONCURRENT: int = 5

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        max_concurrent: int = DEFAULT_MAX_CONCURRENT,
    ) -> None:
        self._client = http_client
        self._semaphore = asyncio.Semaphore(max_concurrent)

    @hubeau_retry
    async def _get(
        self, url: str, params: dict[str, Any] | None = None
    ) -> httpx.Response:
        """Async GET request with automatic retry on transient errors."""
        async with self._semaphore:
            resp = await self._client.get(
                url, params=params or {}, timeout=self.DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
            return resp
