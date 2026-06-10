from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EndpointStatus(BaseModel):
    """Health status for a single API endpoint."""

    name: str
    ok: bool
    latency_ms_avg: Optional[float] = None
    latency_ms_min: Optional[float] = None
    latency_ms_max: Optional[float] = None
    error: Optional[str] = None


class HealthReport(BaseModel):
    """Aggregated health check result for an API."""

    api: str
    checked_at: datetime
    n_requests_per_endpoint: int
    endpoints: list[EndpointStatus]
    healthy_ratio: float = Field(
        description="Fraction of endpoints that responded successfully"
    )

    def is_healthy(self) -> bool:
        return self.healthy_ratio == 1.0

    def summary(self) -> str:
        lines = [
            f"[{self.api}] checked at {self.checked_at.isoformat()}",
            f"  healthy: {self.healthy_ratio:.0%} "
            f"({sum(e.ok for e in self.endpoints)}/{len(self.endpoints)} endpoints)",
        ]
        for e in self.endpoints:
            if e.ok:
                lines.append(
                    f"  ✓ {e.name:<35} "
                    f"avg={e.latency_ms_avg:.0f}ms "
                    f"min={e.latency_ms_min:.0f}ms "
                    f"max={e.latency_ms_max:.0f}ms"
                )
            else:
                lines.append(f"  ✗ {e.name:<35} error={e.error}")
        return "\n".join(lines)


class DataWindow(BaseModel):
    """Data availability window for one station and one endpoint."""

    station_code: str
    endpoint: str
    count: Optional[int] = None
    latest: Optional[str] = None
    oldest: Optional[str] = None
    error: Optional[str] = None

    def has_data(self) -> bool:
        return self.count is not None and self.count > 0

    def is_recent(self, max_days: int = 30) -> bool:
        """Check if the latest observation is within max_days."""
        if not self.latest:
            return False
        from datetime import timezone

        latest_dt = datetime.fromisoformat(self.latest.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - latest_dt
        return delta.days <= max_days


class CoverageReport(BaseModel):
    """Aggregated data coverage result for an API."""

    api: str
    checked_at: datetime
    stations_sampled: int
    random_sample: bool
    windows: list[DataWindow]

    def summary(self) -> str:
        lines = [
            f"[{self.api}] coverage checked at {self.checked_at.isoformat()}",
            f"  stations sampled: {self.stations_sampled} "
            f"({'random' if self.random_sample else 'first N'})",
        ]
        for w in self.windows:
            if w.error:
                lines.append(f"  ✗ {w.station_code} / {w.endpoint}: {w.error}")
            else:
                lines.append(
                    f"  ✓ {w.station_code} / {w.endpoint:<20} "
                    f"count={w.count} latest={w.latest}"
                )
        return "\n".join(lines)
