from __future__ import annotations

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from .classifier import build_brief
from .delivery import DeliveryChannel, deliver
from .renderer import render_brief
from .sample_data import load_sample_items


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a morning briefing.")
    parser.add_argument(
        "--delivery",
        choices=[channel.value for channel in DeliveryChannel],
        default=DeliveryChannel.CONSOLE.value,
        help="Where to send the briefing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview delivery behavior without sending external messages.",
    )
    args = parser.parse_args(argv)

    now = datetime.now(ZoneInfo("America/New_York"))
    items = load_sample_items(now)
    brief = build_brief(items)
    message = render_brief(brief)
    result = deliver(message, DeliveryChannel(args.delivery), dry_run=args.dry_run)

    if not result.ok:
        print(result.detail)
        return 2

    return 0
