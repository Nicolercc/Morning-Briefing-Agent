from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from morning_briefing_agent.config import load_dotenv, load_google_config


class ConfigTest(unittest.TestCase):
    def test_load_dotenv_keeps_existing_environment_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text("EXAMPLE_KEY=from_file\n", encoding="utf-8")

            with patch.dict(os.environ, {"EXAMPLE_KEY": "from_env"}, clear=False):
                load_dotenv(env_file)

                self.assertEqual("from_env", os.environ["EXAMPLE_KEY"])

    def test_load_google_config_parses_multiple_gmail_profiles(self) -> None:
        env = {
            "GOOGLE_AUTH_MODE": "oauth_user",
            "GOOGLE_OAUTH_CLIENT_FILE": "credentials/google_oauth_client.json",
            "GOOGLE_TOKEN_DIR": "tokens/google",
            "GMAIL_ACCOUNT_IDS": "personal,mom",
            "GMAIL_ACCOUNT_PERSONAL_OWNER": "you",
            "GMAIL_ACCOUNT_PERSONAL_LABEL": "Personal Gmail",
            "GMAIL_ACCOUNT_MOM_OWNER": "mom",
            "GMAIL_ACCOUNT_MOM_LABEL": "Mom Gmail",
        }

        with patch.dict(os.environ, env, clear=True):
            config = load_google_config()

        self.assertEqual("oauth_user", config.auth_mode)
        self.assertEqual(2, len(config.accounts))
        self.assertEqual("Personal Gmail", config.accounts[0].label)
        self.assertEqual("tokens/google/mom.json", str(config.accounts[1].token_file))


if __name__ == "__main__":
    unittest.main()
