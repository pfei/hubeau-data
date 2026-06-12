from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.eau_potable import (
    CommuneUdi,
    CommuneUdiParams,
    ResultatEauPotable,
    ResultatEauPotableParams,
)


class AsyncEauPotableAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable"

    async def get_communes_udi(
        self, params: Optional[CommuneUdiParams] = None
    ) -> List[CommuneUdi]:
        resp = await self._get(
            f"{self.BASE_URL}/communes_udi",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [CommuneUdi(**item) for item in resp.json().get("data", [])]

    async def get_resultats_dis(
        self, params: Optional[ResultatEauPotableParams] = None
    ) -> List[ResultatEauPotable]:
        resp = await self._get(
            f"{self.BASE_URL}/resultats_dis",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ResultatEauPotable(**item) for item in resp.json().get("data", [])]
