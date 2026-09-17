from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DefenseAction(StrEnum):
    NO_INTERVENTION = "A0"
    SANITIZE = "A1"
    TOOL_RESTRICTION = "A2"
    BLOCK = "A3"


class AttackerType(StrEnum):
    STATIC = "static"
    ADAPTIVE = "adaptive"


@dataclass
class Interaction:
    interaction_id: str
    task_id: str
    user_input: str
    external_context: str = ""
    tool_sensitive: bool = False
    attack_family: str | None = None
    attacker_type: AttackerType = AttackerType.STATIC
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectionResult:
    injection_probability: float
    indicators: list[str] = field(default_factory=list)

    @property
    def is_injection(self) -> bool:
        return self.injection_probability >= 0.25

    @property
    def score(self) -> float:
        return self.injection_probability

    def __post_init__(self):
        self.injection_probability = max(
            0.0, min(1.0, self.injection_probability)
        )


@dataclass
class RiskAssessment:
    score: float
    level: RiskLevel
    features: dict[str, float] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.score = max(0.0, min(1.0, self.score))


@dataclass
class DefenseDecision:
    action: DefenseAction
    expected_security: float
    expected_utility: float
    expected_cost: float
    objective_value: float
    reason: str = ""


@dataclass
class AgentOutcome:
    attack_success: bool
    harmful_action: bool
    task_success: bool
    false_positive: bool
    latency_ms: float
    model_calls: int = 1
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class Feedback:
    security_signal: float
    utility_signal: float
    cost_signal: float
    reward: float


@dataclass
class EpisodeResult:
    interaction: Interaction
    detection: DetectionResult
    risk: RiskAssessment
    decision: DefenseDecision
    outcome: AgentOutcome
    feedback: Feedback
    episode_id: int
