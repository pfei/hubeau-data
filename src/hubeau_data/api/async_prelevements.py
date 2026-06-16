from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.prelevements import (
    ChroniquePrelevement,
    ChroniquePrelevementParams,
    OuvrageParams,
    OuvragePrelevement,
    PointPrelevement,
    PointPrelevementParams,
)
from hubeau_data.utils import extract_next_cursor


class AsyncPrelevementsAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/prelevements"

    async def get_ouvrages(
        self, params: Optional[OuvrageParams] = None
    ) -> PagedResponse[OuvragePrelevement]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/ouvrages",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[OuvragePrelevement](
            count=body["count"],
            data=[OuvragePrelevement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_points_prelevement(
        self, params: Optional[PointPrelevementParams] = None
    ) -> PagedResponse[PointPrelevement]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/points_prelevement",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[PointPrelevement](
            count=body["count"],
            data=[PointPrelevement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_chroniques(
        self, params: Optional[ChroniquePrelevementParams] = None
    ) -> PagedResponse[ChroniquePrelevement]:
        resp = await self._get(
            f"{self.BASE_URL}/chroniques",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniquePrelevement](
            count=body["count"],
            data=[ChroniquePrelevement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
