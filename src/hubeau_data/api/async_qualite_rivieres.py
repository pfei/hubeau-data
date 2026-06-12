from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.qualite_rivieres import (
    AnalysePc,
    AnalysePcParams,
    StationPc,
    StationPcParams,
)


class AsyncQualiteRivieresAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres"

    async def get_stations(
        self, params: Optional[StationPcParams] = None
    ) -> List[StationPc]:
        resp = await self._get(
            f"{self.BASE_URL}/station_pc",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationPc(**item) for item in resp.json().get("data", [])]

    async def get_analyses(
        self,
        params: Optional[AnalysePcParams] = None,
        max_records: int = 1000,
    ) -> List[AnalysePc]:
        """Fetch physico-chemical analyses, paginated. Returns up to max_records."""
        url = f"{self.BASE_URL}/analyse_pc"
        query_params = params.model_dump(exclude_none=True) if params else {}
        page_size = int(query_params.get("size", 100))
        query_params["size"] = page_size
        results: List[AnalysePc] = []
        page = 1
        while len(results) < max_records:
            query_params["page"] = page
            resp = await self._get(url, query_params)
            data = resp.json().get("data", [])
            if not data:
                break
            results.extend([AnalysePc(**item) for item in data])
            if len(data) < page_size:
                break
            page += 1
        return results[:max_records]
