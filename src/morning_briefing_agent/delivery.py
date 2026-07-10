from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum

from .config import SlackConfig, load_slack_config


class DeliveryChannel(str, Enum):
    CONSOLE = "console"
    SLACK = "slack"
    EMAIL = "email"


@dataclass(frozen=True)
class DeliveryResult:
    channel: DeliveryChannel
    ok: bool
    detail: str


def deliver(
    message: str,
    channel: DeliveryChannel,
    *,
    dry_run: bool = False,
    slack_config: SlackConfig | None = None,
) -> DeliveryResult:
    if channel == DeliveryChannel.CONSOLE:
        print(message)
        return DeliveryResult(channel=channel, ok=True, detail="Printed to console.")

    if channel == DeliveryChannel.SLACK:
        return deliver_to_slack(message, dry_run=dry_run, config=slack_config)

    if channel == DeliveryChannel.EMAIL:
        return DeliveryResult(
            channel=channel,
            ok=False,
            detail="Email delivery is intentionally stubbed until SMTP or Gmail send is configured.",
        )

    raise ValueError(f"Unsupported delivery channel: {channel}")


def deliver_to_slack(
    message: str,
    *,
    dry_run: bool = False,
    config: SlackConfig | None = None,
) -> DeliveryResult:
    config = config or load_slack_config()

    if dry_run:
        print(_format_slack_preview(message, config))
        return DeliveryResult(
            channel=DeliveryChannel.SLACK,
            ok=True,
            detail="Slack dry run printed locally.",
        )

    if not config.is_configured:
        return DeliveryResult(
            channel=DeliveryChannel.SLACK,
            ok=False,
            detail="Set SLACK_BOT_TOKEN and SLACK_CHANNEL_ID in .env to send Slack briefings.",
        )

    payload = {
        "channel": config.channel_id,
        "text": message,
        "username": config.username,
        "mrkdwn": True,
    }
    request = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return DeliveryResult(
            channel=DeliveryChannel.SLACK,
            ok=False,
            detail=f"Slack request failed: {exc.reason}",
        )

    if not body.get("ok"):
        return DeliveryResult(
            channel=DeliveryChannel.SLACK,
            ok=False,
            detail=f"Slack API rejected the message: {body.get('error', 'unknown_error')}",
        )

    return DeliveryResult(
        channel=DeliveryChannel.SLACK,
        ok=True,
        detail=f"Sent Slack briefing to {config.channel_id}.",
    )


def _format_slack_preview(message: str, config: SlackConfig) -> str:
    target = config.channel_id or "SLACK_CHANNEL_ID not set"
    return f"Slack dry run -> {target}\n\n{message}"
