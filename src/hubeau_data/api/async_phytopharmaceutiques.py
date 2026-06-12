from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.phytopharmaceutiques import (
    AchatProduit,
    AchatProduitParams,
    AchatSubstance,
    AchatSubstanceParams,
    VenteProduit,
    VenteProduitParams,
    VenteSubstance,
    VenteSubstanceParams,
)

_DEFAULT_PARAMS = {"type_territoire": "National"}


class AsyncPhytopharmaceutiquesAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/vente_achat_phyto"

    async def get_achats_substances(
        self, params: Optional[AchatSubstanceParams] = None
    ) -> List[AchatSubstance]:
        resp = await self._get(
            f"{self.BASE_URL}/achats/substances",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [AchatSubstance(**item) for item in resp.json().get("data", [])]

    async def get_achats_produits(
        self, params: Optional[AchatProduitParams] = None
    ) -> List[AchatProduit]:
        resp = await self._get(
            f"{self.BASE_URL}/achats/produits",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [AchatProduit(**item) for item in resp.json().get("data", [])]

    async def get_ventes_substances(
        self, params: Optional[VenteSubstanceParams] = None
    ) -> List[VenteSubstance]:
        resp = await self._get(
            f"{self.BASE_URL}/ventes/substances",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [VenteSubstance(**item) for item in resp.json().get("data", [])]

    async def get_ventes_produits(
        self, params: Optional[VenteProduitParams] = None
    ) -> List[VenteProduit]:
        resp = await self._get(
            f"{self.BASE_URL}/ventes/produits",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [VenteProduit(**item) for item in resp.json().get("data", [])]
