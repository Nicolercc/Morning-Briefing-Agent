# Morning Briefing Agent Product Blueprint

## The Best Delivery Strategy

Use Slack as the primary morning briefing and email as the archive.

Slack is the better default for a morning command center because it is fast,
scannable, and actionable. Later, Slack can support buttons like `Snooze`,
`Mark done`, `Open email`, and `Add reminder`. Email is useful as a searchable
backup, but it is a weak primary channel because the whole product exists to
reduce inbox load.

Recommended setup:

1. Send one Slack DM every morning.
2. Send a matching email copy only as an archive.
3. Keep a tiny local/web dashboard for settings, account connections, and
   historical briefs.

## Product Vision

The app is not "an AI that summarizes email." It is a personal operations layer.

It watches your important streams, separates signal from noise, and gives you a
ranked daily plan:

- Urgent items
- Job application movement
- Newsletters worth saving
- Calendar prep
- Slack asks
- Your mom's important account events
- Suggested next actions

## Staff Engineer Architecture

```text
Sources
  Gmail account 1
  Gmail account 2
  Mom's Gmail
  Calendar
  Slack
        |
        v
Normalize every item into one shared schema
        |
        v
Classify by owner, source, category, urgency, and sensitivity
        |
        v
Rank by actionability and deadline
        |
        v
Render a brief with evidence and suggested actions
        |
        v
Deliver to Slack, archive to email, save history
```

## Best Practices

- Use OAuth. Never ask for or store email passwords.
- Use read-only Gmail and Calendar scopes until the product truly needs write
  access.
- Store one token per account and label each account by owner.
- Keep your mom's data in a separate profile with explicit boundaries.
- Never let the AI send, delete, or mark things done without approval.
- Classify and filter before sending data to the model.
- Show "why this was included" for every high-priority item.
- Start with mock data, then connect live accounts one at a time.

## MVP Build Plan

### Step 1: Prove the Product Loop

Build a mock-data prototype that can classify:

- Urgent email
- Job applications
- Newsletters
- Mom-related account items
- Calendar events
- Slack asks

### Step 2: Connect One Gmail Account

Use Gmail read-only OAuth. Fetch unread messages and recent messages from the
last 12 to 24 hours.

### Step 3: Add Multi-Account Profiles

Add account labels like:

- Personal Gmail
- Job Search Gmail
- Mom Gmail

Every item should carry `owner`, `account_label`, `source`, and `sensitivity`.

### Step 4: Add Calendar And Slack

Calendar provides time pressure. Slack provides work asks. These should be
separate connectors that return the same normalized item shape.

### Step 5: Add Delivery

Start with console output. Then add Slack DM delivery. Add email archive after
Slack works.

### Step 6: Add Feedback

The product becomes excellent when you can say:

- "Always show this sender"
- "Never show this newsletter"
- "This is job-search related"
- "This belongs to mom"
- "This was not urgent"

That feedback becomes your personal ranking layer.

## How To Explain It To Anybody

"It is a personal briefing agent. It reads my allowed sources, turns everything
into the same kind of item, ranks what matters, and sends me one clear morning
message. It does not replace my judgment. It reduces the amount of searching I
have to do before I can make good decisions."
