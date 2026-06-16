from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.eau_potable import (
    CommuneUdi,
    CommuneUdiParams,
    ResultatEauPotable,
    ResultatEauPotableParams,
)
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.utils import extract_next_cursor


class AsyncEauPotableAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable"

    async def get_communes_udi(
        self, params: Optional[CommuneUdiParams] = None
    ) -> PagedResponse[CommuneUdi]:
        resp = await self._get(
            f"{self.BASE_URL}/communes_udi",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[CommuneUdi](
            count=body["count"],
            data=[CommuneUdi(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_resultats_dis(
        self, params: Optional[ResultatEauPotableParams] = None
    ) -> PagedResponse[ResultatEauPotable]:
        resp = await self._get(
            f"{self.BASE_URL}/resultats_dis",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ResultatEauPotable](
            count=body["count"],
            data=[ResultatEauPotable(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
