from __future__ import annotations

from datetime import datetime, timedelta

from .models import Owner, Source, SourceItem


def load_sample_items(now: datetime) -> list[SourceItem]:
    return [
        SourceItem(
            id="email-001",
            source=Source.EMAIL,
            owner=Owner.YOU,
            account_label="personal gmail",
            title="Action required: portfolio interview availability",
            sender="recruiting@startup.example",
            body="Can you confirm availability for a final portfolio interview by 2pm today?",
            timestamp=now - timedelta(hours=2),
            metadata={"folder": "inbox"},
        ),
        SourceItem(
            id="email-002",
            source=Source.EMAIL,
            owner=Owner.YOU,
            account_label="job search gmail",
            title="Application received: Product Engineer",
            sender="jobs@company.example",
            body="Thanks for applying. We received your application and will review it shortly.",
            timestamp=now - timedelta(hours=6),
            metadata={"company": "Company Example"},
        ),
        SourceItem(
            id="email-003",
            source=Source.EMAIL,
            owner=Owner.YOU,
            account_label="personal gmail",
            title="AI product strategy newsletter",
            sender="newsletter@product.example",
            body="This week: agent UX, memory, trust, and delivery patterns.",
            timestamp=now - timedelta(hours=9),
        ),
        SourceItem(
            id="email-004",
            source=Source.EMAIL,
            owner=Owner.MOM,
            account_label="mom gmail",
            title="Lab results are available",
            sender="portal@clinic.example",
            body="A new document is available in the patient portal. Please review when possible.",
            timestamp=now - timedelta(hours=4),
            metadata={"sensitivity": "health"},
        ),
        SourceItem(
            id="cal-001",
            source=Source.CALENDAR,
            owner=Owner.YOU,
            account_label="personal calendar",
            title="Mock interview prep",
            sender="calendar",
            body="30 minute prep block before tomorrow's interview.",
            timestamp=now + timedelta(hours=3),
            metadata={"location": "Google Meet"},
        ),
        SourceItem(
            id="slack-001",
            source=Source.SLACK,
            owner=Owner.YOU,
            account_label="work slack",
            title="#launch: copy review needed",
            sender="alex",
            body="Can you review the launch copy before the end of day?",
            timestamp=now - timedelta(hours=1),
            metadata={"channel": "launch"},
        ),
    ]
