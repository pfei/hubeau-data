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
from hubeau_data.models.pagination import PagedResponse
from hubeau_data.models.temperature import (
    ChroniqueTemperature,
    ChroniqueTemperatureParams,
    StationTemperature,
    StationTemperatureParams,
)
from hubeau_data.utils import extract_next_cursor


class TemperatureAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/temperature"

    _HEALTH_ENDPOINTS = [
        ("station", {"size": 1}),
        ("chronique", {"size": 1}),
    ]

    def get_stations(
        self, params: Optional[StationTemperatureParams] = None
    ) -> PagedResponse[StationTemperature]:
        resp = self._get(
            f"{self.BASE_URL}/station",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationTemperature](
            count=body["count"],
            data=[StationTemperature(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    def get_chronique(
        self, params: Optional[ChroniqueTemperatureParams] = None
    ) -> PagedResponse[ChroniqueTemperature]:
        resp = self._get(
            f"{self.BASE_URL}/chronique",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniqueTemperature](
            count=body["count"],
            data=[ChroniqueTemperature(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

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
            api="temperature",
            checked_at=datetime.now(timezone.utc),
            n_requests_per_endpoint=n_requests,
            endpoints=statuses,
            healthy_ratio=ok_count / len(statuses),
        )

    def data_coverage(
        self,
        code_station: Optional[str] = None,
        n_stations: int = 3,
        random: bool = False,
    ) -> CoverageReport:
        checked_at = datetime.now(timezone.utc)
        if code_station is not None:
            station_codes = [code_station]
            random_sample = False
        else:
            stations_page = self.get_stations(
                params=StationTemperatureParams(size=500 if random else n_stations)
            )
            if random and len(stations_page.data) >= n_stations:
                station_list = random_module.sample(stations_page.data, n_stations)
            else:
                station_list = stations_page.data[:n_stations]
            station_codes = [s.code_station for s in station_list if s.code_station]
            random_sample = random
        windows: List[DataWindow] = []
        for code in station_codes:
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/chronique",
                    params={"code_station": code, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="chronique",
                        count=body.get("count"),
                        latest=data[0].get("date_mesure_temp") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="chronique",
                        error=type(e).__name__,
                    )
                )
        return CoverageReport(
            api="temperature",
            checked_at=checked_at,
            stations_sampled=len(station_codes),
            random_sample=random_sample,
            windows=windows,
        )
