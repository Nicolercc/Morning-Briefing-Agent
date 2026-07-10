from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Owner(str, Enum):
    YOU = "you"
    MOM = "mom"


class Source(str, Enum):
    EMAIL = "email"
    CALENDAR = "calendar"
    SLACK = "slack"


class Category(str, Enum):
    URGENT = "urgent"
    UPCOMING_EVENT = "upcoming_event"
    JOB_APPLICATION = "job_application"
    NEWSLETTER = "newsletter"
    MOM_WATCH = "mom_watch"
    SLACK_HIGHLIGHT = "slack_highlight"
    OTHER = "other"


@dataclass(frozen=True)
class AccountProfile:
    id: str
    owner: Owner
    label: str
    source: Source
    address_or_handle: str


@dataclass(frozen=True)
class SourceItem:
    id: str
    source: Source
    owner: Owner
    account_label: str
    title: str
    sender: str
    body: str
    timestamp: datetime
    url: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class BriefItem:
    source_item: SourceItem
    category: Category
    priority: int
    reason: str
    suggested_action: str


@dataclass(frozen=True)
class Brief:
    generated_at: datetime
    items: list[BriefItem]

    def by_category(self, category: Category) -> list[BriefItem]:
        return [item for item in self.items if item.category == category]
