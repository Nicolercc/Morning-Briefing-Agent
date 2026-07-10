# Morning Briefing Agent

This is a local-first prototype for a personal morning briefing agent.

The first version uses sample data so the product behavior can be tuned before
connecting private Gmail, Calendar, and Slack accounts.

## Product Decision

Use Slack as the primary daily delivery channel, with email as the archive.

Slack is better for the morning "what needs my attention?" moment because it is
short, scannable, and can later support buttons like `Snooze`, `Mark done`, and
`Open email`. Email is better as a backup copy and searchable history.

## Run

```bash
PYTHONPATH=src python3 -m morning_briefing_agent --delivery console
```

Preview the Slack message without sending anything:

```bash
PYTHONPATH=src python3 -m morning_briefing_agent --delivery slack --dry-run
```

Send to Slack after configuring `.env`:

```bash
cp .env.example .env
# Fill in SLACK_BOT_TOKEN and SLACK_CHANNEL_ID.
PYTHONPATH=src python3 -m morning_briefing_agent --delivery slack
```

Check local configuration:

```bash
PYTHONPATH=src python3 -m morning_briefing_agent.doctor
```

From the project root, either install in editable mode:

```bash
python3 -m pip install -e .
morning-briefing --delivery console
```

Or run directly:

```bash
PYTHONPATH=src python3 -m morning_briefing_agent --delivery console
```

## Test

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Slack Delivery

Recommended delivery is a Slack DM or private channel:

- `SLACK_BOT_TOKEN`: token with permission to call `chat.postMessage`.
- `SLACK_CHANNEL_ID`: the channel, private channel, or DM conversation ID.
- `SLACK_USERNAME`: optional display name for the message sender.

Best practice: use a bot token for delivery and keep read tokens separate from
write tokens. For local personal prototypes, a user token can work, but it
represents you directly and should not be used in shared production systems.

## Gmail Credentials

For personal Gmail accounts, use user OAuth. You need one OAuth client file for
the app and one generated token file per mailbox. A Google service account is
only appropriate for Google Workspace domain-wide delegation.

See [docs/credential-setup.md](docs/credential-setup.md) for the exact `.env`
shape and the difference between OAuth client credentials, token files, and
service accounts.

## Architecture

```text
connectors -> normalized inbox -> classifier/ranker -> brief renderer -> delivery
```

- `connectors`: Gmail, Calendar, Slack, and future sources.
- `models`: Shared data objects so every source speaks the same language.
- `classifier`: Converts raw items into product categories and priorities.
- `renderer`: Produces a human-readable briefing.
- `delivery`: Sends to console today and Slack when configured.

## Real Integrations To Add Next

1. Gmail read-only connector with one OAuth token per account.
2. Calendar read-only connector for your schedule.
3. Slack read connector for important channels.
4. Connect Slack delivery to your real channel or DM.
5. Email delivery as an archive and fallback.

Keep all tokens out of git. Use `.env`, `.gitignore`, and eventually macOS
Keychain or a managed secrets store.
