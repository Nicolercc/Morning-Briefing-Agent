from __future__ import annotations

import unittest

from morning_briefing_agent.config import SlackConfig
from morning_briefing_agent.delivery import DeliveryChannel, deliver


class DeliveryTest(unittest.TestCase):
    def test_slack_dry_run_does_not_require_credentials(self) -> None:
        result = deliver(
            "Morning brief",
            DeliveryChannel.SLACK,
            dry_run=True,
            slack_config=SlackConfig(
                token=None,
                channel_id=None,
                username="Morning Briefing Agent",
            ),
        )

        self.assertTrue(result.ok)
        self.assertEqual("Slack dry run printed locally.", result.detail)

    def test_slack_requires_token_and_channel_when_not_dry_run(self) -> None:
        result = deliver(
            "Morning brief",
            DeliveryChannel.SLACK,
            dry_run=False,
            slack_config=SlackConfig(
                token=None,
                channel_id=None,
                username="Morning Briefing Agent",
            ),
        )

        self.assertFalse(result.ok)
        self.assertIn("SLACK_BOT_TOKEN", result.detail)

    def test_slack_treats_placeholders_as_missing(self) -> None:
        result = deliver(
            "Morning brief",
            DeliveryChannel.SLACK,
            dry_run=False,
            slack_config=SlackConfig(
                token="replace-with-your-slack-bot-or-user-oauth-token",
                channel_id="replace-with-your-slack-channel-or-dm-id",
                username="Morning Briefing Agent",
            ),
        )

        self.assertFalse(result.ok)
        self.assertIn("SLACK_BOT_TOKEN", result.detail)


if __name__ == "__main__":
    unittest.main()
