from typing import List, Optional

from hubeau_data.async_base import AsyncHubeauBaseAPI
from hubeau_data.models.qualite_nappes import (
    AnalyseNappe,
    AnalyseNappeParams,
    StationNappe,
    StationNappeParams,
)


class AsyncQualiteNappesAPI(AsyncHubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/qualite_nappes"

    async def get_stations(
        self, params: Optional[StationNappeParams] = None
    ) -> List[StationNappe]:
        resp = await self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationNappe(**item) for item in resp.json().get("data", [])]

    async def get_analyses(
        self,
        params: Optional[AnalyseNappeParams] = None,
        max_records: int = 1000,
    ) -> List[AnalyseNappe]:
        url = f"{self.BASE_URL}/analyses"
        query_params = params.model_dump(exclude_none=True) if params else {}
        page_size = int(query_params.get("size", 100))
        query_params["size"] = page_size
        results: List[AnalyseNappe] = []
        page = 1
        while len(results) < max_records:
            query_params["page"] = page
            resp = await self._get(url, query_params)
            data = resp.json().get("data", [])
            if not data:
                break
            results.extend([AnalyseNappe(**item) for item in data])
            if len(data) < page_size:
                break
            page += 1
        return results[:max_records]
