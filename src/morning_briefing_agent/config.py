from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SlackConfig:
    token: str | None
    channel_id: str | None
    username: str

    @property
    def is_configured(self) -> bool:
        return bool(self.token and self.channel_id)


def load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_slack_config() -> SlackConfig:
    load_dotenv()
    return SlackConfig(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        channel_id=os.environ.get("SLACK_CHANNEL_ID"),
        username=os.environ.get("SLACK_USERNAME", "Morning Briefing Agent"),
    )
