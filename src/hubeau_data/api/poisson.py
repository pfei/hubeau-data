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
from hubeau_data.models.poisson import (
    IndicateurPoisson,
    IndicateurPoissonParams,
    ObservationPoisson,
    ObservationPoissonParams,
    OperationPoisson,
    OperationPoissonParams,
    StationPoisson,
    StationPoissonParams,
)


class PoissonAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/etat_piscicole"

    _HEALTH_ENDPOINTS = [
        ("stations", {"size": 1}),
        ("indicateurs", {"size": 1}),
        ("observations", {"size": 1}),
        ("operations", {"size": 1}),
    ]

    def get_stations(
        self, params: Optional[StationPoissonParams] = None
    ) -> PagedResponse[StationPoisson]:
        resp = self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationPoisson](
            count=body["count"],
            data=[StationPoisson(**item) for item in body.get("data", [])],
            next_cursor=self._extract_next_cursor(body.get("next")),
        )

    def get_indicateurs(
        self, params: Optional[IndicateurPoissonParams] = None
    ) -> PagedResponse[IndicateurPoisson]:
        resp = self._get(
            f"{self.BASE_URL}/indicateurs",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[IndicateurPoisson](
            count=body["count"],
            data=[IndicateurPoisson(**item) for item in body.get("data", [])],
            next_cursor=self._extract_next_cursor(body.get("next")),
        )

    def get_observations(
        self, params: Optional[ObservationPoissonParams] = None
    ) -> PagedResponse[ObservationPoisson]:
        resp = self._get(
            f"{self.BASE_URL}/observations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ObservationPoisson](
            count=body["count"],
            data=[ObservationPoisson(**item) for item in body.get("data", [])],
            next_cursor=self._extract_next_cursor(body.get("next")),
        )

    def get_operations(
        self, params: Optional[OperationPoissonParams] = None
    ) -> PagedResponse[OperationPoisson]:
        resp = self._get(
            f"{self.BASE_URL}/operations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[OperationPoisson](
            count=body["count"],
            data=[OperationPoisson(**item) for item in body.get("data", [])],
            next_cursor=self._extract_next_cursor(body.get("next")),
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
            api="poisson",
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
                params=StationPoissonParams(size=500 if random else n_stations)
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
                    f"{self.BASE_URL}/indicateurs",
                    params={"code_station": code, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="indicateurs",
                        count=body.get("count"),
                        latest=data[0].get("date_operation") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="indicateurs",
                        error=type(e).__name__,
                    )
                )
        return CoverageReport(
            api="poisson",
            checked_at=checked_at,
            stations_sampled=len(station_codes),
            random_sample=random_sample,
            windows=windows,
        )
