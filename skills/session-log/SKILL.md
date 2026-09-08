---
name: session-log
description: Write a durable record of a work session — what was built, root-caused, or shipped — into the project's notes. Use when the user says log this session, write a session log, record this, or when a substantial piece of work has just finished and needs to be handed off to a future session.
license: MIT
---

# Session log

Writes a durable record of a work session. These logs get treated as ground truth by whoever reads them next — including you, six weeks from now, with none of this context. **Accuracy matters more than polish.**

## When to run this

- A build, fix, audit, or research wave just finished
- A session is ending and there's state the next one would need
- Something was root-caused and the mechanism is worth keeping

Don't run it for trivial work. A one-line fix doesn't need a log.

## Where it goes

Wherever the project keeps its session records — a `docs/sessions/` directory, a notes vault, a wiki. Ask once if it isn't obvious, then stay consistent.

A filename carrying the date and a short description sorts and scans well: `YYYY-MM-DD Short Description.md`.

## Steps

### 1. Gather the facts before writing

**Do not write from memory of the conversation alone.** Collect:

- PR numbers, commit SHAs, migration timestamps, deploy IDs
- What was actually verified, and by what command
- What failed, and what's still open
- Anything only a human can do

If a fact can't be confirmed, mark it unconfirmed rather than dropping it or asserting it.

### 2. Write the body

```markdown
# YYYY-MM-DD — <what was root-caused or shipped>

<One line naming how the work was run: who planned, who built, who reviewed.>

## What happened

- Mechanism first. Why this happened, not just what.
- Concrete evidence: PR numbers, SHAs, timestamps, row counts, log lines.
- Distinguish proven from inferred, explicitly.

## Fix

1. Numbered steps. Each states what was verified and how.

## Standing DO-NOT rules
<Only if the session produced prohibitions. Ground each in the incident that caused it.>

## Remaining items — needs a human

- [ ] Things only they can do

Links: <related documents>
```

If the notes system uses frontmatter, include an `outcome` field: **one full sentence stating what is now true that wasn't before.** It is the most-read line in the file. Make it a real claim, not a label.

### 3. The two sections everyone drops

**`## Remaining items` and the links footer are required.** They are the two sections that carry value forward and the two most often omitted — in one vault, measured across 230 existing logs, they appeared in only ~21% and ~28% of them.

Write both, every time. If nothing is genuinely held for a human, write `None — nothing is held.` rather than deleting the heading.

### 4. Mark every claim

Label each one `VERIFIED (how)` or `ASSUMED (why not checked)` inline. Do not blur them.

"Verified" should mean a human or a command actually confirmed it. **A claim about production requires a query against production** — not a passing test, not a merged PR, not a green deploy.

### 5. Resolve every link before saving

Check each link target against a real file before writing it. A notes system accumulates broken references fast, and a log full of dead links is a log nobody trusts.

### 6. Update the project's state

If the work changed a project's status, add a dated state section to that project's main document — **newest first, prepend, never overwrite history.**

If the work advanced a program with a handoff document, update it in place so the next session picks up correctly.

### 7. Feed the lessons back

If the user corrected something during the session, write the lesson somewhere durable — a rules file, a memory store, this skill itself. That is how corrections stop repeating.

## House style

- Specific and falsifiable. Vague summaries are worse than nothing here.
- Never claim a status without saying how it was checked.
- Lead with bad news. Don't bury it.
- Write for a reader with none of your context.

## Do not

- Do not overwrite an existing log. Read first, then edit.
- Do not write into machine-generated directories.
- Do not create scratch files or build output alongside the notes.
