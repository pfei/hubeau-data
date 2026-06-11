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
from hubeau_data.models.phytopharmaceutiques import (
    AchatProduit,
    AchatProduitParams,
    AchatSubstance,
    AchatSubstanceParams,
    VenteProduit,
    VenteProduitParams,
    VenteSubstance,
    VenteSubstanceParams,
)

_DEFAULT_PARAMS = {"type_territoire": "National"}


class PhytopharmaceutiquesAPI(HubeauBaseAPI):
    BASE_URL = "https://hubeau.eaufrance.fr/api/v1/vente_achat_phyto"

    _HEALTH_ENDPOINTS: list[tuple[str, dict[str, str | int]]] = [
        ("achats/substances", {"size": 1, "type_territoire": "National"}),
        ("achats/produits", {"size": 1, "type_territoire": "National"}),
        ("ventes/substances", {"size": 1, "type_territoire": "National"}),
        ("ventes/produits", {"size": 1, "type_territoire": "National"}),
    ]

    def get_achats_substances(
        self, params: Optional[AchatSubstanceParams] = None
    ) -> List[AchatSubstance]:
        resp = self._get(
            f"{self.BASE_URL}/achats/substances",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [AchatSubstance(**item) for item in resp.json().get("data", [])]

    def get_achats_produits(
        self, params: Optional[AchatProduitParams] = None
    ) -> List[AchatProduit]:
        resp = self._get(
            f"{self.BASE_URL}/achats/produits",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [AchatProduit(**item) for item in resp.json().get("data", [])]

    def get_ventes_substances(
        self, params: Optional[VenteSubstanceParams] = None
    ) -> List[VenteSubstance]:
        resp = self._get(
            f"{self.BASE_URL}/ventes/substances",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [VenteSubstance(**item) for item in resp.json().get("data", [])]

    def get_ventes_produits(
        self, params: Optional[VenteProduitParams] = None
    ) -> List[VenteProduit]:
        resp = self._get(
            f"{self.BASE_URL}/ventes/produits",
            params.model_dump(exclude_none=True) if params else _DEFAULT_PARAMS,
        )
        return [VenteProduit(**item) for item in resp.json().get("data", [])]

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
            api="phytopharmaceutiques",
            checked_at=datetime.now(timezone.utc),
            n_requests_per_endpoint=n_requests,
            endpoints=statuses,
            healthy_ratio=ok_count / len(statuses),
        )

    def data_coverage(self) -> CoverageReport:
        checked_at = datetime.now(timezone.utc)
        windows: List[DataWindow] = []
        for endpoint in ["ventes/substances", "achats/substances"]:
            try:
                resp = httpx.get(
                    f"{self.BASE_URL}/{endpoint}",
                    params={"type_territoire": "National", "size": 1, "sort": "desc"},
                    timeout=10,
                )
                resp.raise_for_status()
                body = resp.json()
                data = body.get("data", [])
                windows.append(
                    DataWindow(
                        station_code="National",
                        endpoint=endpoint,
                        count=body.get("count"),
                        latest=str(data[0].get("annee")) if data else None,
                    )
                )
            except Exception as e:
                windows.append(
                    DataWindow(
                        station_code="National",
                        endpoint=endpoint,
                        error=type(e).__name__,
                    )
                )
        return CoverageReport(
            api="phytopharmaceutiques",
            checked_at=checked_at,
            stations_sampled=1,
            random_sample=False,
            windows=windows,
        )
