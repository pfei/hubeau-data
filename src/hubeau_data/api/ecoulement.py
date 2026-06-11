import random as random_module
import time
from datetime import datetime, timezone
from typing import List, Optional

import httpx

from hubeau_data.base import HubeauBaseAPI
from hubeau_data.models.ecoulement import (
    CampagneEcoulement,
    CampagneEcoulementParams,
    ObservationEcoulement,
    ObservationEcoulementParams,
    StationEcoulement,
    StationEcoulementParams,
)
from hubeau_data.models.health import (
    CoverageReport,
    DataWindow,
    EndpointStatus,
    HealthReport,
)


class EcoulementAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/ecoulement"

    _HEALTH_ENDPOINTS = [
        ("stations", {"size": 1}),
        ("observations", {"size": 1}),
        ("campagnes", {"size": 1}),
    ]

    def get_stations(
        self, params: Optional[StationEcoulementParams] = None
    ) -> List[StationEcoulement]:
        resp = self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [StationEcoulement(**item) for item in resp.json().get("data", [])]

    def get_observations(
        self, params: Optional[ObservationEcoulementParams] = None
    ) -> List[ObservationEcoulement]:
        resp = self._get(
            f"{self.BASE_URL}/observations",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [ObservationEcoulement(**item) for item in resp.json().get("data", [])]

    def get_campagnes(
        self, params: Optional[CampagneEcoulementParams] = None
    ) -> List[CampagneEcoulement]:
        resp = self._get(
            f"{self.BASE_URL}/campagnes",
            params.model_dump(exclude_none=True) if params else None,
        )
        return [CampagneEcoulement(**item) for item in resp.json().get("data", [])]

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
            api="ecoulement",
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
            stations = self.get_stations(
                params=StationEcoulementParams(size=500 if random else n_stations)
            )
            if random and len(stations) >= n_stations:
                stations = random_module.sample(stations, n_stations)
            else:
                stations = stations[:n_stations]
            station_codes = [s.code_station for s in stations if s.code_station]
            random_sample = random
        windows: List[DataWindow] = []
        for code in station_codes:
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/observations",
                    params={"code_station": code, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="observations",
                        count=body.get("count"),
                        latest=data[0].get("date_observation") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="observations",
                        error=type(e).__name__,
                    )
                )
        return CoverageReport(
            api="ecoulement",
            checked_at=checked_at,
            stations_sampled=len(station_codes),
            random_sample=random_sample,
            windows=windows,
        )
