from __future__ import annotations

from pathlib import Path

from .config import GoogleConfig, SlackConfig, load_google_config, load_slack_config


def main() -> int:
    slack = load_slack_config()
    google = load_google_config()

    print("Morning Briefing Agent config check")
    print("")
    _print_slack(slack)
    print("")
    _print_google(google)

    return 0


def _print_slack(config: SlackConfig) -> None:
    print("Slack")
    print(_status("SLACK_BOT_TOKEN", config.has_token))
    print(_status("SLACK_CHANNEL_ID", config.has_channel_id))
    print(f"- SLACK_USERNAME: {config.username}")


def _print_google(config: GoogleConfig) -> None:
    print("Google")
    print(f"- GOOGLE_AUTH_MODE: {config.auth_mode}")

    if config.auth_mode == "oauth_user":
        print(_path_status("GOOGLE_OAUTH_CLIENT_FILE", config.oauth_client_file))
        print(f"- GOOGLE_TOKEN_DIR: {config.token_dir}")
        print(f"- Gmail account profiles: {len(config.accounts)}")
        for account in config.accounts:
            print(f"  - {account.id}: {account.label} ({account.owner}) -> {account.token_file}")
        if not config.accounts:
            print("  - Add GMAIL_ACCOUNT_IDS to .env before connecting Gmail.")
        return

    if config.auth_mode == "service_account":
        print(_path_status("GOOGLE_SERVICE_ACCOUNT_FILE", config.service_account_file))
        print(f"- GOOGLE_DELEGATED_SUBJECTS: {len(config.delegated_subjects)} configured")
        print("- Use this only for Google Workspace domain-wide delegation.")
        return

    print("- Unknown auth mode. Use oauth_user or service_account.")


def _status(name: str, ok: bool) -> str:
    return f"- {name}: {'set' if ok else 'missing'}"


def _path_status(name: str, path: Path | None) -> str:
    if path is None:
        return f"- {name}: missing"
    return f"- {name}: {path} ({'found' if path.exists() else 'not found yet'})"


if __name__ == "__main__":
    raise SystemExit(main())
