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
from hubeau_data.models.prelevements import (
    ChroniquePrelevement,
    ChroniquePrelevementParams,
    OuvrageParams,
    OuvragePrelevement,
    PointPrelevement,
    PointPrelevementParams,
)
from hubeau_data.utils import extract_next_cursor


class PrelevementsAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/prelevements"

    _HEALTH_ENDPOINTS = [
        ("referentiel/ouvrages", {"size": 1}),
        ("referentiel/points_prelevement", {"size": 1}),
        ("chroniques", {"size": 1}),
    ]

    def get_ouvrages(
        self, params: Optional[OuvrageParams] = None
    ) -> PagedResponse[OuvragePrelevement]:
        resp = self._get(
            f"{self.BASE_URL}/referentiel/ouvrages",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[OuvragePrelevement](
            count=body["count"],
            data=[OuvragePrelevement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    def get_points_prelevement(
        self, params: Optional[PointPrelevementParams] = None
    ) -> PagedResponse[PointPrelevement]:
        resp = self._get(
            f"{self.BASE_URL}/referentiel/points_prelevement",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[PointPrelevement](
            count=body["count"],
            data=[PointPrelevement(**item) for item in body.get("data", [])],
            next_cursor=extract_next_cursor(body.get("next")),
        )

    def get_chroniques(
        self, params: Optional[ChroniquePrelevementParams] = None
    ) -> PagedResponse[ChroniquePrelevement]:
        resp = self._get(
            f"{self.BASE_URL}/chroniques",
            params.model_dump(exclude_none=True) if params else None,
        )
        body = resp.json()
        return PagedResponse[ChroniquePrelevement](
            count=body["count"],
            data=[ChroniquePrelevement(**item) for item in body.get("data", [])],
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
        checked_at = datetime.now(timezone.utc)
        if code_ouvrage is not None:
            ouvrage_codes = [code_ouvrage]
            random_sample = False
        else:
            ouvrages_page = self.get_ouvrages(
                params=OuvrageParams(size=500 if random else n_ouvrages)
            )
            if random and len(ouvrages_page.data) >= n_ouvrages:
                ouvrage_list = random_module.sample(ouvrages_page.data, n_ouvrages)
            else:
                ouvrage_list = ouvrages_page.data[:n_ouvrages]
            ouvrage_codes = [o.code_ouvrage for o in ouvrage_list if o.code_ouvrage]
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
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="chroniques",
                        count=body.get("count"),
                        latest=str(data[0].get("annee")) if data else None,
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
