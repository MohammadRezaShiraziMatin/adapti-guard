import json
from dataclasses import asdict, dataclass


@dataclass
class StandardRecord:
    id: str
    dataset: str
    split: str

    text: str | None = None
    instruction: str | None = None
    context: str | None = None
    response: str | None = None

    attack_family: str | None = None
    attack_type: str | None = None

    agent_task: str | None = None
    tool_use: bool = False
    tool_name: str | None = None

    injection_location: str | None = None

    label: str | None = None
    severity: str | None = None

    source_file: str | None = None
    source_index: int | None = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False
        )
