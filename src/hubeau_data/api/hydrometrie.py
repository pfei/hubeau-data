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
from hubeau_data.models.hydrometrie import (
    ObsElab,
    ObsElabParams,
    ObservationTr,
    ObservationTrParams,
    Site,
    SiteParams,
    Station,
    StationParams,
)
from hubeau_data.models.pagination import PagedResponse


class HydrometrieAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"

    _HEALTH_ENDPOINTS: list[tuple[str, dict[str, str | int]]] = [
        ("referentiel/sites", {"size": 1}),
        ("referentiel/stations", {"size": 1}),
        ("observations_tr", {"size": 1}),
        ("obs_elab", {"size": 1}),
    ]

    def get_sites(self, params: Optional[SiteParams] = None) -> PagedResponse[Site]:
        resp = self._get(
            f"{self.BASE_URL}/referentiel/sites",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[Site](
            count=body["count"],
            data=[Site(**item) for item in body.get("data", [])],
            next_cursor=self._extract_next_cursor(body.get("next")),
        )

    def get_stations(
        self, params: Optional[StationParams] = None
    ) -> PagedResponse[Station]:
        resp = self._get(
            f"{self.BASE_URL}/referentiel/stations",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[Station](
            count=body["count"],
            data=[Station(**item) for item in body.get("data", [])],
            next_cursor=self._extract_next_cursor(body.get("next")),
        )

    def get_observations_tr(
        self, params: Optional[ObservationTrParams] = None
    ) -> PagedResponse[ObservationTr]:
        resp = self._get(
            f"{self.BASE_URL}/observations_tr",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ObservationTr](
            count=body["count"],
            data=[ObservationTr(**item) for item in body["data"]],
            next_cursor=self._extract_next_cursor(body.get("next")),
        )

    def get_obs_elab(
        self, params: Optional[ObsElabParams] = None
    ) -> PagedResponse[ObsElab]:
        resp = self._get(
            f"{self.BASE_URL}/obs_elab",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ObsElab](
            count=body["count"],
            data=[ObsElab(**item) for item in body["data"]],
            next_cursor=self._extract_next_cursor(body.get("next")),
        )

    # --- Health & Coverage — pas de retry : on mesure les erreurs ---

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
                    EndpointStatus(
                        name=endpoint,
                        ok=False,
                        error=error or "unknown",
                    )
                )

        ok_count = sum(s.ok for s in statuses)
        return HealthReport(
            api="hydrometrie",
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
                params=StationParams(size=500 if random else n_stations)
            )
            if random and len(stations_page.data) >= n_stations:
                station_list = random_module.sample(stations_page.data, n_stations)
            else:
                station_list = stations_page.data[:n_stations]
            station_codes = [s.code_station for s in station_list if s.code_station]
            random_sample = random

        windows: List[DataWindow] = []

        for code in station_codes:
            for endpoint, date_field in [
                ("observations_tr", "date_obs"),
                ("obs_elab", "date_obs_elab"),
            ]:
                try:
                    resp = httpx.get(
                        f"{self.BASE_URL}/{endpoint}",
                        params={"code_entite": code, "size": 1, "sort": "desc"},
                        timeout=10,
                    )
                    resp.raise_for_status()
                    body = resp.json()
                    data = body.get("data", [])
                    windows.append(
                        DataWindow(
                            station_code=code,
                            endpoint=endpoint,
                            count=body.get("count"),
                            latest=data[0].get(date_field) if data else None,
                        )
                    )
                except Exception as e:
                    windows.append(
                        DataWindow(
                            station_code=code,
                            endpoint=endpoint,
                            error=type(e).__name__,
                        )
                    )

        return CoverageReport(
            api="hydrometrie",
            checked_at=checked_at,
            stations_sampled=len(station_codes),
            random_sample=random_sample,
            windows=windows,
        )
