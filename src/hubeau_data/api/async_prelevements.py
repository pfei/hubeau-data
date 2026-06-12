from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.prelevements import (
    ChroniquePrelevement,
    ChroniquePrelevementParams,
    OuvrageParams,
    OuvragePrelevement,
    PointPrelevement,
    PointPrelevementParams,
)


class AsyncPrelevementsAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/prelevements"

    async def get_ouvrages(
        self, params: Optional[OuvrageParams] = None
    ) -> List[OuvragePrelevement]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/ouvrages",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [OuvragePrelevement(**item) for item in resp.json().get("data", [])]

    async def get_points_prelevement(
        self, params: Optional[PointPrelevementParams] = None
    ) -> List[PointPrelevement]:
        resp = await self._get(
            f"{self.BASE_URL}/referentiel/points_prelevement",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [PointPrelevement(**item) for item in resp.json().get("data", [])]

    async def get_chroniques(
        self, params: Optional[ChroniquePrelevementParams] = None
    ) -> List[ChroniquePrelevement]:
        resp = await self._get(
            f"{self.BASE_URL}/chroniques",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ChroniquePrelevement(**item) for item in resp.json().get("data", [])]
