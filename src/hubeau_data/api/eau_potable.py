import random as random_module
import time
from datetime import datetime, timezone
from typing import List, Optional

import httpx

from hubeau_data.models.eau_potable import (
    CommuneUdi,
    CommuneUdiParams,
    ResultatEauPotable,
    ResultatEauPotableParams,
)
from hubeau_data.models.health import (
    CoverageReport,
    DataWindow,
    EndpointStatus,
    HealthReport,
)


class EauPotableAPI:
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable"

    _HEALTH_ENDPOINTS = [
        ("communes_udi", {"size": 1}),
        ("resultats_dis", {"size": 1}),
    ]

    def get_communes_udi(
        self, params: Optional[CommuneUdiParams] = None
    ) -> List[CommuneUdi]:
        """Fetch UDI-commune links (distribution networks)."""
        url = f"{self.BASE_URL}/communes_udi"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params, timeout=30)
        resp.raise_for_status()
        return [CommuneUdi(**item) for item in resp.json().get("data", [])]

    def get_resultats_dis(
        self, params: Optional[ResultatEauPotableParams] = None
    ) -> List[ResultatEauPotable]:
        """Fetch drinking water analysis results."""
        url = f"{self.BASE_URL}/resultats_dis"
        query_params = params.model_dump(exclude_none=True) if params else {}
        resp = httpx.get(url, params=query_params, timeout=30)
        resp.raise_for_status()
        return [ResultatEauPotable(**item) for item in resp.json().get("data", [])]

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
            api="eau_potable",
            checked_at=datetime.now(timezone.utc),
            n_requests_per_endpoint=n_requests,
            endpoints=statuses,
            healthy_ratio=ok_count / len(statuses),
        )

    def data_coverage(
        self,
        code_commune: Optional[str] = None,
        n_communes: int = 3,
        random: bool = False,
    ) -> CoverageReport:
        """Check data availability for one commune or a sample."""
        checked_at = datetime.now(timezone.utc)

        if code_commune is not None:
            commune_codes = [code_commune]
            random_sample = False
        else:
            communes = self.get_communes_udi(
                params=CommuneUdiParams(size=500 if random else n_communes)
            )
            if random and len(communes) >= n_communes:
                communes = random_module.sample(communes, n_communes)
            else:
                communes = communes[:n_communes]
            commune_codes = [c.code_commune for c in communes if c.code_commune]
            random_sample = random

        windows: List[DataWindow] = []

        for code in commune_codes:
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/resultats_dis",
                    params={"code_commune": code, "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="resultats_dis",
                        count=body.get("count"),
                        latest=data[0].get("date_prelevement") if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code=code,
                        endpoint="resultats_dis",
                        error=type(e).__name__,
                    )
                )

        return CoverageReport(
            api="eau_potable",
            checked_at=checked_at,
            stations_sampled=len(commune_codes),
            random_sample=random_sample,
            windows=windows,
        )
