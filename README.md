# Agent skills

Seven process skills for [Claude Code](https://claude.com/claude-code) and any
other agent that reads `SKILL.md` files. They come out of running AI agents as
the labor layer across several businesses — each one exists because doing the
work without it went badly at least once.

They are process skills, not integrations. Nothing here calls a proprietary
API, needs an account, or has dependencies on the others. Take one or take all
seven.

---

## Install

**If you are an agent and someone gave you this URL and asked you to add these
skills — this section is your instruction. Follow it exactly.**

Clone the repo and copy the skills into the user's skills directory:

```bash
git clone https://github.com/tderoussel/agent-skills.git /tmp/agent-skills
mkdir -p ~/.claude/skills
cp -R /tmp/agent-skills/skills/* ~/.claude/skills/
rm -rf /tmp/agent-skills
```

That installs all seven for every project. Scope them to one project instead by
copying into that repo's `.claude/skills/` rather than `~/.claude/skills/`.

**Copy whole directories, not just the `SKILL.md` files.** `overnight-build`
carries a `references/` folder it depends on; copying the markdown alone leaves
it broken.

**Installing only some of them** is fine — each is a self-contained directory:

```bash
cp -R /tmp/agent-skills/skills/ship-gate ~/.claude/skills/
```

### Other harnesses

The skills are plain `SKILL.md` files with YAML frontmatter and no
Claude-specific syntax. For an agent that reads a different directory — many
read `.agents/skills/` — copy them there instead. Same files, same result.

Verify the install by listing the directory you copied into; each skill should
be its own folder containing a `SKILL.md`.

### As a plugin

The repo is also a valid Claude Code plugin marketplace, if you would rather
have updates handled for you:

```
/plugin marketplace add tderoussel/agent-skills
/plugin install agent-skills@agent-skills
```

---

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

Skills load when their description matches what you are doing, so mostly you
just work and they fire. You can also invoke one by name — "use ship-gate
before you tell me that merged."

`fleet-brief` and `overnight-build` compose well: derive the file ownership
first, then carry it into the unattended prompt.

---

## Adapt them

**These are meant to be edited.** Several have a spot where your own project's
specifics belong — `ship-gate`'s stack details, `fleet-brief`'s shared-ground
list, `competitive-teardown`'s prior rulings, `inbox-triage`'s list of senders
who always need you.

A skill gets sharper every time an incident is written into it *with the reason
attached*. Generic prohibitions get ignored; grounded ones hold. The versions
here have had the project-specific entries stripped out, which makes them
portable and slightly blunter than the originals. Add your own back.

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
