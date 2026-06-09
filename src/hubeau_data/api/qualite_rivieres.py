from typing import List, Optional

import httpx

from hubeau_data.models.qualite_rivieres import (
    AnalysePc,
    AnalysePcParams,
    StationPc,
    StationPcParams,
)


class QualiteRivieresAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres"

    def get_stations(self, params: Optional[StationPcParams] = None) -> List[StationPc]:
        """Fetch physico-chemical monitoring stations."""
        url = f"{self.BASE_URL}/station_pc"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params, timeout=30)
        resp.raise_for_status()
        return [StationPc(**item) for item in resp.json().get("data", [])]

    def get_analyses(
        self,
        params: Optional[AnalysePcParams] = None,
        max_records: int = 1000,
    ) -> List[AnalysePc]:
        """Fetch physico-chemical analyses, paginated. Returns up to max_records."""
        url = f"{self.BASE_URL}/analyse_pc"
        query_params = params.model_dump(exclude_none=True) if params else {}
        # ensure a page size — default 100 if not set
        page_size = query_params.get("size", 100)
        query_params["size"] = page_size
        results: List[AnalysePc] = []
        page = 1
        while len(results) < max_records:
            query_params["page"] = page
            resp = httpx.get(url, params=query_params, timeout=30)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                break
            results.extend([AnalysePc(**item) for item in data])
            if len(data) < page_size:
                break
            page += 1
        return results[:max_records]
