"""Budget / request gate for live eval (accounting only; does not call APIs)."""
from __future__ import annotations

from dataclasses import dataclass, field

from adapti_guard.evaluation.target_model import GenerationRequest, GenerationResult, TargetModel


@dataclass
class BudgetLedger:
    max_requests: int | None = None
    max_usd: float | None = None
    requests_used: int = 0
    estimated_cost_usd: float | None = None  # None => UNKNOWN
    hard_stop: bool = True

    def check_allowed(self, *, additional_requests: int = 1) -> tuple[bool, str]:
        if self.max_requests is not None:
            if self.requests_used + additional_requests > self.max_requests:
                return False, "budget_failure: max_requests exceeded"
        if self.max_usd is not None and self.estimated_cost_usd is not None:
            if self.estimated_cost_usd > self.max_usd:
                return False, "budget_failure: max_usd exceeded"
        return True, "ok"

    def record_requests(self, count: int, *, retry_count: int = 0) -> None:
        """Count includes retries (each HTTP attempt counts)."""
        total = max(0, count) + max(0, retry_count)
        self.requests_used += total

    def record_cost_unknown(self) -> None:
        self.estimated_cost_usd = None

    def to_dict(self) -> dict:
        return {
            "max_requests": self.max_requests,
            "max_usd": self.max_usd,
            "requests_used": self.requests_used,
            "estimated_cost": self.estimated_cost_usd if self.estimated_cost_usd is not None else "UNKNOWN",
            "hard_stop": self.hard_stop,
        }


class BudgetGatedTargetModel(TargetModel):
    """Wrap TargetModel: authorization-adjacent request accounting (fail closed)."""

    def __init__(
        self,
        inner: TargetModel,
        ledger: BudgetLedger,
        *,
        provider: str = "unknown",
    ) -> None:
        self._inner = inner
        self._ledger = ledger
        self.provider = provider

    def generate(self, request: GenerationRequest) -> GenerationResult:
        max_attempts = int(getattr(self._inner, "max_retries", 0)) + 1
        allowed, reason = self._ledger.check_allowed(additional_requests=max_attempts)
        if not allowed and self._ledger.hard_stop:
            return GenerationResult(
                text="",
                model_id=request.model_id or getattr(self._inner, "model_id", ""),
                latency_ms=0.0,
                error=reason,
                raw={"failure_kind": "budget_exhausted", "http_attempts": 0},
            )
        result = self._inner.generate(request)
        attempts = 1
        if result.raw and isinstance(result.raw.get("http_attempts"), int):
            attempts = max(1, int(result.raw["http_attempts"]))
        if not result.cache_hit:
            self._ledger.record_requests(1, retry_count=max(0, attempts - 1))
        return result
