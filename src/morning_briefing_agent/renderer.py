from __future__ import annotations

from .models import Brief, BriefItem, Category

SECTION_ORDER = [
    ("URGENT", Category.URGENT),
    ("UPCOMING EVENTS", Category.UPCOMING_EVENT),
    ("JOB APPLICATIONS", Category.JOB_APPLICATION),
    ("MOM WATCH", Category.MOM_WATCH),
    ("SLACK HIGHLIGHTS", Category.SLACK_HIGHLIGHT),
    ("NEWSLETTERS", Category.NEWSLETTER),
    ("OTHER EMAILS", Category.OTHER),
]


def render_brief(brief: Brief) -> str:
    lines = [
        "Morning Briefing",
        f"Generated from {len(brief.items)} normalized items",
        "",
    ]

    for heading, category in SECTION_ORDER:
        section_items = brief.by_category(category)
        if not section_items:
            continue
        lines.append(heading)
        for item in section_items:
            lines.extend(_render_item(item))
        lines.append("")

    actions = [item for item in brief.items if item.priority >= 70]
    lines.append("SUGGESTED ACTIONS")
    if actions:
        for index, item in enumerate(actions, start=1):
            source = item.source_item
            lines.append(f"{index}. {item.suggested_action} [{source.account_label}: {source.title}]")
    else:
        lines.append("1. No high-priority actions found. Review newsletters later.")

    return "\n".join(lines).strip()


def _render_item(item: BriefItem) -> list[str]:
    source = item.source_item
    return [
        f"- {source.title}",
        f"  From: {source.sender} via {source.account_label}",
        f"  Why it matters: {item.reason}",
    ]
