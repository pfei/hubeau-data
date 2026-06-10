import random as random_module
import time
from datetime import datetime, timezone
from typing import List, Optional

import httpx

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


class HydrometrieAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v2/hydrometrie"

    # Endpoints to probe for health checks
    _HEALTH_ENDPOINTS = [
        ("referentiel/sites", {"size": 1}),
        ("referentiel/stations", {"size": 1}),
        ("observations_tr", {"size": 1}),
        ("obs_elab", {"size": 1}),
    ]

    def get_sites(self, params: Optional[SiteParams] = None) -> List[Site]:
        url = f"{self.BASE_URL}/referentiel/sites"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [Site(**item) for item in resp.json()["data"]]

    def get_stations(self, params: Optional[StationParams] = None) -> List[Station]:
        url = f"{self.BASE_URL}/referentiel/stations"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [Station(**item) for item in resp.json()["data"]]

    def get_observations_tr(
        self, params: Optional[ObservationTrParams] = None
    ) -> List[ObservationTr]:
        url = f"{self.BASE_URL}/observations_tr"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [ObservationTr(**item) for item in resp.json()["data"]]

    def get_obs_elab(self, params: Optional[ObsElabParams] = None) -> List[ObsElab]:
        url = f"{self.BASE_URL}/obs_elab"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params)
        resp.raise_for_status()
        return [ObsElab(**item) for item in resp.json()["data"]]

    # --- Health & Coverage ---

    def check_health(self, n_requests: int = 3) -> HealthReport:
        """Probe all endpoints N times and return latency stats."""
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
        """Check data availability for one station or a sample of stations."""
        checked_at = datetime.now(timezone.utc)

        if code_station is not None:
            station_codes = [code_station]
            random_sample = False
        else:
            stations = self.get_stations(
                params=StationParams(size=500 if random else n_stations)
            )
            if random and len(stations) >= n_stations:
                stations = random_module.sample(stations, n_stations)
            else:
                stations = stations[:n_stations]
            station_codes = [s.code_station for s in stations if s.code_station]
            random_sample = random

        windows: List[DataWindow] = []

        for code in station_codes:
            # observations_tr
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/observations_tr",
                    params={"code_station": code, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="observations_tr",
                        count=body.get("count"),
                        latest=data[0].get("date_obs") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="observations_tr",
                        error=type(e).__name__,
                    )
                )

            # obs_elab
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/obs_elab",
                    params={"code_station": code, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="obs_elab",
                        count=body.get("count"),
                        latest=data[0].get("date_obs_elab") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="obs_elab",
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
