from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SlackConfig:
    token: str | None
    channel_id: str | None
    username: str

    @property
    def is_configured(self) -> bool:
        return _has_real_value(self.token) and _has_real_value(self.channel_id)

    @property
    def has_token(self) -> bool:
        return _has_real_value(self.token)

    @property
    def has_channel_id(self) -> bool:
        return _has_real_value(self.channel_id)


@dataclass(frozen=True)
class GmailAccountConfig:
    id: str
    owner: str
    label: str
    token_file: Path
    email: str | None = None


@dataclass(frozen=True)
class GoogleConfig:
    auth_mode: str
    oauth_client_file: Path
    token_dir: Path
    accounts: list[GmailAccountConfig]
    service_account_file: Path | None
    delegated_subjects: list[str]


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


def load_google_config() -> GoogleConfig:
    load_dotenv()
    token_dir = Path(os.environ.get("GOOGLE_TOKEN_DIR", "tokens/google"))
    account_ids = _split_csv(os.environ.get("GMAIL_ACCOUNT_IDS", ""))

    return GoogleConfig(
        auth_mode=os.environ.get("GOOGLE_AUTH_MODE", "oauth_user"),
        oauth_client_file=Path(
            os.environ.get("GOOGLE_OAUTH_CLIENT_FILE", "credentials/google_oauth_client.json")
        ),
        token_dir=token_dir,
        accounts=[_load_gmail_account(account_id, token_dir) for account_id in account_ids],
        service_account_file=_optional_path(os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")),
        delegated_subjects=_split_csv(os.environ.get("GOOGLE_DELEGATED_SUBJECTS", "")),
    )


def _load_gmail_account(account_id: str, token_dir: Path) -> GmailAccountConfig:
    prefix = f"GMAIL_ACCOUNT_{_env_suffix(account_id)}"
    return GmailAccountConfig(
        id=account_id,
        owner=os.environ.get(f"{prefix}_OWNER", "you"),
        label=os.environ.get(f"{prefix}_LABEL", account_id.replace("_", " ").title()),
        token_file=Path(os.environ.get(f"{prefix}_TOKEN_FILE", str(token_dir / f"{account_id}.json"))),
        email=os.environ.get(f"{prefix}_EMAIL"),
    )


def _env_suffix(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")


def _split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def _optional_path(value: str | None) -> Path | None:
    if not value:
        return None
    return Path(value)


def _has_real_value(value: str | None) -> bool:
    if not value:
        return False

    normalized = value.strip().lower()
    if normalized in {"c0123456789", "xoxb-your-token-here", "xoxp-your-token-here"}:
        return False

    return not normalized.startswith("replace-with-")
