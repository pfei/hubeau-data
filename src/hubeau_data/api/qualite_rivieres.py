from typing import Any, List, Optional

import httpx

from hubeau_data.models.qualite_rivieres import AnalysePc, StationPc


class QualiteRivieresAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres"

    def get_stations(
        self, libelle_commune: Optional[str] = None, size: int = 10, **params: Any
    ) -> List[StationPc]:
        """
        Fetch a list of stations, optionally filtered by commune name.
        """
        url = f"{self.BASE_URL}/station_pc"
        params["size"] = size
        if libelle_commune:
            params["libelle_commune"] = libelle_commune
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return [StationPc(**item) for item in data]

    def get_analyses(
        self,
        code_station: Optional[str] = None,
        size: int = 100,
        max_records: int = 1000,
        **params: Any,
    ) -> List[AnalysePc]:
        """
        Fetch analyses, paginated, for a station. Returns up to max_records.
        """
        url = f"{self.BASE_URL}/analyse_pc"
        params["size"] = size
        if code_station:
            params["code_station"] = code_station
        results: List[Any] = []
        page = 1
        while len(results) < max_records:
            params["page"] = page
            resp = httpx.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                break
            results.extend([AnalysePc(**item) for item in data])
            if len(data) < size:
                break  # Last page
            page += 1
        return results[:max_records]
