from __future__ import annotations

import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from morning_briefing_agent.classifier import build_brief
from morning_briefing_agent.models import Category
from morning_briefing_agent.sample_data import load_sample_items


class ClassifierTest(unittest.TestCase):
    def test_build_brief_prioritizes_urgent_items(self) -> None:
        now = datetime(2026, 7, 7, 8, 0, tzinfo=ZoneInfo("America/New_York"))

        brief = build_brief(load_sample_items(now))

        self.assertEqual(Category.URGENT, brief.items[0].category)
        self.assertEqual(
            "Action required: portfolio interview availability",
            brief.items[0].source_item.title,
        )

    def test_build_brief_separates_mom_items(self) -> None:
        now = datetime(2026, 7, 7, 8, 0, tzinfo=ZoneInfo("America/New_York"))

        brief = build_brief(load_sample_items(now))

        mom_items = brief.by_category(Category.MOM_WATCH)
        self.assertEqual(1, len(mom_items))
        self.assertEqual("mom gmail", mom_items[0].source_item.account_label)


if __name__ == "__main__":
    unittest.main()
