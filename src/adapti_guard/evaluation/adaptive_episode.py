"""Adaptive multi-turn offline: attacker updates from defense feedback."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from adapti_guard.attacker.adaptive_attacker import AdaptiveAttacker
from adapti_guard.core.models import DefenseAction
from adapti_guard.evaluation.stateful_episode import StatefulEpisodeRunner, TurnSpec, TurnTargetFn

DefenseFn = Callable[..., tuple[DefenseAction | str, dict[str, Any]]]

_DEFAULT_TARGET: TurnTargetFn = lambda h, m: (
    f'MODEL: {m} TOOL_REQUEST: {{"name":"send_email","arguments":{{"to":"x","body":"y"}}}}'
)

@dataclass(frozen=True)
class AdaptiveEpisodeResult:
    seed: int
    n_turns: int
    families_seen: tuple[str, ...]
    episode_harmful: bool
    strategy_changed: bool

class AdaptiveEpisodeRunner:
    def __init__(self, max_turns: int = 4) -> None:
        self.max_turns = max_turns
        self._stateful = StatefulEpisodeRunner(experiment_id="adaptive_offline")

    def run(
        self,
        *,
        attacker: AdaptiveAttacker,
        defense: DefenseFn,
        seed: int = 0,
        target: TurnTargetFn | None = None,
    ) -> AdaptiveEpisodeResult:
        target_fn = target or _DEFAULT_TARGET
        families: list[str] = []
        harmful = False
        for idx in range(self.max_turns):
            attempt = attacker.generate()
            attacker.record(attempt)
            families.append(attempt.family)
            partial = self._stateful.run(
                [TurnSpec(user_message=attempt.payload)],
                target=target_fn,
                defense=defense,
                seed=seed + idx,
            )
            tr = partial.turns[0]
            harmful = harmful or tr.privileged_tool_executed
            attacker.observe_defense(blocked=tr.defense_action in ("A2", "A3"), harmful_outcome=tr.privileged_tool_executed)
        changed = len(families) >= 2 and families[0] != families[-1]
        return AdaptiveEpisodeResult(seed, len(families), tuple(families), harmful, changed)
