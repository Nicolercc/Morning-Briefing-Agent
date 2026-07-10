# Credential Setup

## What Goes In `.env`

The `.env` file should contain configuration and secret references for your
local machine only. It is ignored by git.

Use `.env.example` as the template:

```bash
cp .env.example .env
```

## Slack

For the current app, you need:

- `SLACK_BOT_TOKEN`: the Bot User OAuth token or User OAuth token.
- `SLACK_CHANNEL_ID`: the channel, private channel, or DM conversation ID.
- `SLACK_USERNAME`: optional display name.

You do not need the Slack Client Secret, Signing Secret, or Verification Token
for the current local sender. Those are used for OAuth install flows, request
signature verification, slash commands, interactivity, and public app flows.

Best practice: use a bot token for sending daily briefings. Give it the
smallest scopes needed, starting with `chat:write`.

## Gmail

For personal Gmail accounts, use user OAuth, not a service account.

You create one OAuth desktop client JSON file for the app:

```text
credentials/google_oauth_client.json
```

Then each Gmail mailbox gets its own token file after that person logs in and
approves access:

```text
tokens/google/personal.json
tokens/google/job_search.json
tokens/google/mom.json
```

This lets one app safely monitor multiple accounts without mixing identities.

## Do You Need One Google Credential For Every Email?

No. You usually need:

1. One OAuth client file for the app.
2. One generated token file per Gmail account.

For your mom's Gmail, she should approve the OAuth prompt herself or explicitly
give you permission to do it with her. Treat that account as a separate profile
in the app.

## What About The Service Account?

The service account email and unique ID are not enough for personal Gmail.

Service accounts are for server-to-server workflows. They can access user Gmail
only in a Google Workspace domain when a Workspace super administrator grants
domain-wide delegation and the app explicitly impersonates a user.

If these are normal Gmail accounts, keep:

```text
GOOGLE_AUTH_MODE=oauth_user
```

Do not put the service-account JSON key in the repo. If you downloaded a private
key file, store it under `credentials/` only if you truly need Workspace
delegation; otherwise do not use it for this project.
