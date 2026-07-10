from __future__ import annotations

from .models import Brief, BriefItem, Category, Owner, Source, SourceItem

URGENT_TERMS = ("urgent", "action required", "deadline", "today", "confirm")
JOB_TERMS = ("application", "interview", "recruit", "resume", "portfolio")
NEWSLETTER_TERMS = ("newsletter", "digest", "weekly", "roundup")


def classify_item(item: SourceItem) -> BriefItem:
    text = f"{item.title} {item.body} {item.sender}".lower()

    if item.owner == Owner.MOM:
        return BriefItem(
            source_item=item,
            category=Category.MOM_WATCH,
            priority=90,
            reason="This belongs to your mom's monitored account and may need care coordination.",
            suggested_action="Review manually before taking action. Keep her privacy boundary explicit.",
        )

    if item.source == Source.CALENDAR:
        return BriefItem(
            source_item=item,
            category=Category.UPCOMING_EVENT,
            priority=80,
            reason="Calendar event coming up soon.",
            suggested_action="Confirm prep, location, and any materials needed.",
        )

    if item.source == Source.SLACK:
        return BriefItem(
            source_item=item,
            category=Category.SLACK_HIGHLIGHT,
            priority=70,
            reason="Recent Slack message appears to ask for your input.",
            suggested_action="Reply or add it to your task list.",
        )

    if any(term in text for term in URGENT_TERMS):
        return BriefItem(
            source_item=item,
            category=Category.URGENT,
            priority=100,
            reason="Contains urgency language or an explicit deadline.",
            suggested_action="Handle before routine inbox processing.",
        )

    if any(term in text for term in JOB_TERMS):
        return BriefItem(
            source_item=item,
            category=Category.JOB_APPLICATION,
            priority=75,
            reason="Related to your job search pipeline.",
            suggested_action="Log the status and schedule a follow-up reminder if needed.",
        )

    if any(term in text for term in NEWSLETTER_TERMS):
        return BriefItem(
            source_item=item,
            category=Category.NEWSLETTER,
            priority=30,
            reason="Newsletter or learning material.",
            suggested_action="Save for reading after priority work.",
        )

    return BriefItem(
        source_item=item,
        category=Category.OTHER,
        priority=40,
        reason="No strong priority signal detected.",
        suggested_action="Batch with normal inbox review.",
    )


def build_brief(items: list[SourceItem]) -> Brief:
    if not items:
        raise ValueError("Cannot build a briefing with no source items.")

    generated_at = max(item.timestamp for item in items)
    brief_items = sorted(
        (classify_item(item) for item in items),
        key=lambda item: item.priority,
        reverse=True,
    )
    return Brief(generated_at=generated_at, items=brief_items)
