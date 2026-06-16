from typing import Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.pagination import PagedResponse
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
from hubeau_data.utils import extract_next_cursor

_DEFAULT_PARAMS = {"type_territoire": "National"}


class AsyncPhytopharmaceutiquesAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/vente_achat_phyto"

    async def get_achats_substances(
        self, params: Optional[AchatSubstanceParams] = None
    ) -> PagedResponse[AchatSubstance]:
        resp = await self._get(
            f"{self.BASE_URL}/achats/substances",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        body = resp.json()
        return PagedResponse[AchatSubstance](
            count=body["count"],
            data=[AchatSubstance(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_achats_produits(
        self, params: Optional[AchatProduitParams] = None
    ) -> PagedResponse[AchatProduit]:
        resp = await self._get(
            f"{self.BASE_URL}/achats/produits",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        body = resp.json()
        return PagedResponse[AchatProduit](
            count=body["count"],
            data=[AchatProduit(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_ventes_substances(
        self, params: Optional[VenteSubstanceParams] = None
    ) -> PagedResponse[VenteSubstance]:
        resp = await self._get(
            f"{self.BASE_URL}/ventes/substances",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        body = resp.json()
        return PagedResponse[VenteSubstance](
            count=body["count"],
            data=[VenteSubstance(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    async def get_ventes_produits(
        self, params: Optional[VenteProduitParams] = None
    ) -> PagedResponse[VenteProduit]:
        resp = await self._get(
            f"{self.BASE_URL}/ventes/produits",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        body = resp.json()
        return PagedResponse[VenteProduit](
            count=body["count"],
            data=[VenteProduit(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )
