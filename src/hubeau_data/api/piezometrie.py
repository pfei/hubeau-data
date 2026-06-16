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
from hubeau_data.models.piezometrie import (
    ChroniquePiezo,
    ChroniquePiezoParams,
    ChroniquePiezoTr,
    ChroniquePiezoTrParams,
    StationPiezo,
    StationPiezoParams,
)
from hubeau_data.utils import extract_next_cursor


class PiezometrieAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/niveaux_nappes"

    _HEALTH_ENDPOINTS = [
        ("stations", {"size": 1}),
        ("chroniques", {"size": 1}),
        ("chroniques_tr", {"size": 1}),
    ]

    def get_stations(
        self, params: Optional[StationPiezoParams] = None
    ) -> PagedResponse[StationPiezo]:
        resp = self._get(
            f"{self.BASE_URL}/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[StationPiezo](
            count=body["count"],
            data=[StationPiezo(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    def get_chroniques(
        self, params: Optional[ChroniquePiezoParams] = None
    ) -> PagedResponse[ChroniquePiezo]:
        resp = self._get(
            f"{self.BASE_URL}/chroniques",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniquePiezo](
            count=body["count"],
            data=[ChroniquePiezo(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    def get_chroniques_tr(
        self, params: Optional[ChroniquePiezoTrParams] = None
    ) -> PagedResponse[ChroniquePiezoTr]:
        resp = self._get(
            f"{self.BASE_URL}/chroniques_tr",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniquePiezoTr](
            count=body["count"],
            data=[ChroniquePiezoTr(**item) for item in body.get("data", [])],
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
            api="piezometrie",
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
            stations_page = self.get_stations(
                params=StationPiezoParams(size=500 if random else n_stations)
            )
            if random and len(stations_page.data) >= n_stations:
                station_list = random_module.sample(stations_page.data, n_stations)
            else:
                station_list = stations_page.data[:n_stations]
            station_ids = [s.bss_id for s in station_list if s.bss_id]
            random_sample = random
        windows: List[DataWindow] = []
        for sid in station_ids:
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/chroniques",
                    params={"bss_id": sid, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=sid,
                        endpoint="chroniques",
                        count=body.get("count"),
                        latest=data[0].get("date_mesure") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=sid,
                        endpoint="chroniques",
                        error=type(e).__name__,
                    )
                )
        return CoverageReport(
            api="piezometrie",
            checked_at=checked_at,
            stations_sampled=len(station_ids),
            random_sample=random_sample,
            windows=windows,
        )
