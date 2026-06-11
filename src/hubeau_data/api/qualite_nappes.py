import random as random_module
import time
from datetime import datetime, timezone
from typing import List, Optional

import httpx

from hubeau_data.base import HubeauBaseAPI
from hubeau_data.models.health import (
    CoverageReport,
    DataWindow,
    EndpointStatus,
    HealthReport,
)
from hubeau_data.models.qualite_nappes import (
    AnalyseNappe,
    AnalyseNappeParams,
    StationNappe,
    StationNappeParams,
)


class QualiteNappesAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/qualite_nappes"

    _HEALTH_ENDPOINTS = [
        ("stations", {"size": 1}),
        ("analyses", {"size": 1}),
    ]

    def get_stations(
        self, params: Optional[StationNappeParams] = None
    ) -> List[StationNappe]:
        resp = self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationNappe(**item) for item in resp.json().get("data", [])]

    def get_analyses(
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
            resp = self._get(url, query_params)
            data = resp.json().get("data", [])
            if not data:
                break
            results.extend([AnalyseNappe(**item) for item in data])
            if len(data) < page_size:
                break
            page += 1
        return results[:max_records]

    def check_health(self, n_requests: int = 3) -> HealthReport:
        statuses: List[EndpointStatus] = []
        for endpoint, probe_params in self._HEALTH_ENDPOINTS:
            url = f"{self.BASE_URL}/{endpoint}"
            latencies: List[float] = []
            error: Optional[str] = None
            for _ in range(n_requests):
                try:
                    t0 = time.perf_counter()
                    resp = httpx.get(url, params=probe_params, timeout=10)
                    resp.raise_for_status()
                    latencies.append((time.perf_counter() - t0) * 1000)
                except Exception as e:
                    error = type(e).__name__
                    break
            if latencies and error is None:
                statuses.append(
                    EndpointStatus(
                        name=endpoint,
                        ok=True,
                        latency_ms_avg=round(sum(latencies) / len(latencies), 1),
                        latency_ms_min=round(min(latencies), 1),
                        latency_ms_max=round(max(latencies), 1),
                    )
                )
            else:
                statuses.append(
                    EndpointStatus(name=endpoint, ok=False, error=error or "unknown")
                )
        ok_count = sum(s.ok for s in statuses)
        return HealthReport(
            api="qualite_nappes",
            checked_at=datetime.now(timezone.utc),
            n_requests_per_endpoint=n_requests,
            endpoints=statuses,
            healthy_ratio=ok_count / len(statuses),
        )

    def data_coverage(
        self,
        bss_id: Optional[str] = None,
        n_stations: int = 3,
        random: bool = False,
    ) -> CoverageReport:
        checked_at = datetime.now(timezone.utc)
        if bss_id is not None:
            station_ids = [bss_id]
            random_sample = False
        else:
            stations = self.get_stations(
                params=StationNappeParams(size=500 if random else n_stations)
            )
            if random and len(stations) >= n_stations:
                stations = random_module.sample(stations, n_stations)
            else:
                stations = stations[:n_stations]
            station_ids = [s.bss_id for s in stations if s.bss_id]
            random_sample = random
        windows: List[DataWindow] = []
        for sid in station_ids:
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/analyses",
                    params={"bss_id": sid, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=sid,
                        endpoint="analyses",
                        count=body.get("count"),
                        latest=data[0].get("date_debut_prelevement") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=sid,
                        endpoint="analyses",
                        error=type(e).__name__,
                    )
                )
        return CoverageReport(
            api="qualite_nappes",
            checked_at=checked_at,
            stations_sampled=len(station_ids),
            random_sample=random_sample,
            windows=windows,
        )
