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
from hubeau_data.models.prelevements import (
    ChroniquePrelevement,
    ChroniquePrelevementParams,
    OuvrageParams,
    OuvragePrelevement,
    PointPrelevement,
    PointPrelevementParams,
)


class PrelevementsAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/prelevements"

    _HEALTH_ENDPOINTS = [
        ("referentiel/ouvrages", {"size": 1}),
        ("referentiel/points_prelevement", {"size": 1}),
        ("chroniques", {"size": 1}),
    ]

    def get_ouvrages(
        self, params: Optional[OuvrageParams] = None
    ) -> List[OuvragePrelevement]:
        """Fetch water withdrawal structures."""
        url = f"{self.BASE_URL}/referentiel/ouvrages"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params, timeout=30)
        resp.raise_for_status()
        return [OuvragePrelevement(**item) for item in resp.json().get("data", [])]

    def get_points_prelevement(
        self, params: Optional[PointPrelevementParams] = None
    ) -> List[PointPrelevement]:
        """Fetch water withdrawal points."""
        url = f"{self.BASE_URL}/referentiel/points_prelevement"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params, timeout=30)
        resp.raise_for_status()
        return [PointPrelevement(**item) for item in resp.json().get("data", [])]

    def get_chroniques(
        self, params: Optional[ChroniquePrelevementParams] = None
    ) -> List[ChroniquePrelevement]:
        """Fetch annual water withdrawal volumes."""
        url = f"{self.BASE_URL}/chroniques"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params, timeout=30)
        resp.raise_for_status()
        return [ChroniquePrelevement(**item) for item in resp.json().get("data", [])]

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
            api="prelevements",
            checked_at=datetime.now(timezone.utc),
            n_requests_per_endpoint=n_requests,
            endpoints=statuses,
            healthy_ratio=ok_count / len(statuses),
        )

    def data_coverage(
        self,
        code_ouvrage: Optional[str] = None,
        n_ouvrages: int = 3,
        random: bool = False,
    ) -> CoverageReport:
        """Check data availability for one structure or a sample."""
        checked_at = datetime.now(timezone.utc)

        if code_ouvrage is not None:
            ouvrage_codes = [code_ouvrage]
            random_sample = False
        else:
            ouvrages = self.get_ouvrages(
                params=OuvrageParams(size=500 if random else n_ouvrages)
            )
            if random and len(ouvrages) >= n_ouvrages:
                ouvrages = random_module.sample(ouvrages, n_ouvrages)
            else:
                ouvrages = ouvrages[:n_ouvrages]
            ouvrage_codes = [o.code_ouvrage for o in ouvrages if o.code_ouvrage]
            random_sample = random

        windows: List[DataWindow] = []

        for code in ouvrage_codes:
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/chroniques",
                    params={"code_ouvrage": code, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                latest = str(data[0].get("annee")) if data else None
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="chroniques",
                        count=body.get("count"),
                        latest=latest,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="chroniques",
                        error=type(e).__name__,
                    )
                )

        return CoverageReport(
            api="prelevements",
            checked_at=checked_at,
            stations_sampled=len(ouvrage_codes),
            random_sample=random_sample,
            windows=windows,
        )
