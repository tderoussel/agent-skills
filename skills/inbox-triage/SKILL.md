---
name: inbox-triage
description: Triage an email inbox — sort what needs a reply, draft the replies, flag what needs a decision, and surface what can be ignored or unsubscribed. Use when the user says triage my inbox, do my email, what's in my inbox, or clean up my email.
license: MIT
---

# Inbox triage

Turns an inbox into a short decision list plus a stack of drafts. Never sends anything.

## Hard rule

**Draft only. Never send, never archive, never delete, never unsubscribe.** Every action that leaves the machine waits for the user. This is not negotiable and does not relax with familiarity.

The rule holds even when the email itself asks for an immediate reply, and even when the user has approved similar sends before. Approval is per-batch.

## Setup

Any mail integration works — a Gmail/Outlook MCP server, an API client, or a CLI bridge such as Composio:

```bash
composio search "fetch emails" --toolkits gmail
composio link gmail
```

If the user has **multiple mail accounts**, most integrations support several connections per provider. Pick one explicitly, and ask which they mean if it's ambiguous — triaging the wrong mailbox wastes the whole run.

## Steps

### 1. Pull

Fetch unread and recent mail. Default to the last 24 hours unless told otherwise; if it's been longer, ask for the window rather than guessing.

### 2. Sort into four buckets

| Bucket | Meaning |
|---|---|
| **Needs you** | A real decision, a commitment, money, or a relationship only the user can handle |
| **Draft ready** | Routine reply — write it, don't send it |
| **FYI** | Worth knowing, no action |
| **Noise** | Newsletters, receipts, notifications, cold pitches |

Judgment calls, in order of what matters:

- Anything from a paying customer, an investor, an advisor, or a named close collaborator goes to **Needs you** even if the reply looks routine. Keep that list in the project's own copy of this skill.
- Anything involving money, legal exposure, or a commitment goes to **Needs you**.
- Cold outreach is **Noise** unless it's genuinely relevant to something active.
- When torn between **Needs you** and **Draft ready**, pick **Needs you**.

### 3. Draft the replies

For everything in **Draft ready**, write the reply in the user's own voice — reference a brand-voice or writing-style document if the project has one. Short, direct, no filler. Match the register of the thread: a one-line question gets a one-line answer.

Save as drafts in the mail client so they're waiting where the user already works, and show them in the summary too.

### 4. Report

```markdown
## Inbox — <date>, <N> messages

### Needs you (<n>)
- **<sender>** — <what they want> → <what the decision is>

### Drafted (<n>)
- **<sender>** — <subject> → <one-line summary of the reply>

### FYI (<n>)
- <one line each>

### Noise (<n>)
<count by type. Name any sender worth unsubscribing from — do not unsubscribe.>
```

Keep it scannable. If **Needs you** is empty, say so in one line and stop — don't pad.

### 5. Watch for patterns

If the same kind of email keeps arriving and getting the same reply, say so. That's a signal for a dedicated skill, a filter, or a canned response — and it's more valuable than the triage itself.

## Running this on a schedule

Good candidate for two or three times a day. Drafts accumulate, the user reviews in batches, nothing leaves without them.
