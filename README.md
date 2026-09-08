# Agent skills

Seven skills for [Claude Code](https://claude.com/claude-code) and other
agents that read `SKILL.md` files. They come out of running AI agents as the
labor layer across several businesses — each one exists because doing the work
without it went badly at least once.

They are process skills, not integrations. Nothing here calls a proprietary
API or needs an account.

## The skills

| Skill | What it does |
|---|---|
| **`ship-gate`** | Verification gate to run *before* claiming something is shipped, merged, deployed, or green. Every rule is a case where the obvious check returned a false pass. |
| **`fleet-brief`** | Writes the brief for splitting work across parallel agents — exclusive per-lane file ownership, shared-ground warnings, and a DO-NOT list with reasons attached. |
| **`decision-council`** | Runs a decision through five independent lenses, blind peer review, and a chairman verdict, instead of giving you one agreeable answer. |
| **`overnight-build`** | Composes an unattended build prompt that survives usage-limit resets via checkpointing, plus the launcher that restarts it. Ships the full template. |
| **`competitive-teardown`** | Turns a competitor into a ranked build-or-ignore verdict, with a mandatory not-worth-copying section. |
| **`vault-doctor`** | Audits an Obsidian vault for broken links, unparseable frontmatter, and ambiguous filenames — classifying findings before proposing any repair. |
| **`inbox-triage`** | Sorts an inbox into needs-you / drafted / FYI / noise and writes the replies. Drafts only; never sends. |

## Install

Copy the ones you want into your skills directory:

```bash
git clone https://github.com/tderoussel/agent-skills.git
cp -r agent-skills/skills/ship-gate ~/.claude/skills/
```

`~/.claude/skills/` makes a skill available everywhere. A project's own
`.claude/skills/` scopes it to that repo. Agents that read `AGENTS.md`
conventions generally also discover `.agents/skills/` — symlink rather than
copy if you want one source of truth:

```bash
ln -s ~/.claude/skills/ship-gate ~/.agents/skills/ship-gate
```

Take one skill or take all seven; they have no dependencies on each other.
`fleet-brief` and `overnight-build` compose well — derive the file ownership
first, then carry it into the unattended prompt.

## Adapt them

**These are meant to be edited.** Several skills have a spot where your own
project's specifics belong — `ship-gate`'s stack details, `fleet-brief`'s
shared-ground list, `competitive-teardown`'s prior rulings, `inbox-triage`'s
list of senders who always need you.

A skill gets sharper every time an incident is written into it with the reason
attached. Generic prohibitions get ignored; grounded ones hold. The versions
here have had the project-specific entries removed, which makes them portable
and slightly blunter than the originals.

## What is deliberately not here

Skills I use but did not write: [gstack](https://github.com/garrytan/gstack),
[superpowers](https://github.com/obra/superpowers), the
[Trail of Bits](https://github.com/trailofbits/claude-plugins) security
plugins, and Supabase's and Composio's official skills. Install those from
their own sources so you get their updates rather than a stale copy of mine.

## Credit

`decision-council`'s multi-persona-plus-blind-review-plus-chairman pattern
comes from Ollie Leman, by way of Remy Gaskell's Open Residency episode on
agent operating systems.

## License

MIT — see [LICENSE](LICENSE). Use them, change them, ship them in your own
tooling.
