# Agent skills

Eighteen skills and four subagents for [Claude Code](https://claude.com/claude-code),
Codex, and other agents that read `SKILL.md` files. The library includes a nine-skill
Realtor Starter Pack and nine process skills for research, decisions, development,
and operations.

Skills provide reusable instructions. They use the tools your assistant actually
has; installing a skill does not connect an account or grant permission to send
messages, spend money, publish a site, or change DNS. Each skill can be used on its
own. Connectors and existing account permissions determine what can be executed.

---

## Realtor Starter Pack

Give your assistant this repository link and ask:

> Install the Realtor Starter Pack from this repository using the skill location
> supported by my assistant. Preserve existing skills and install the complete
> folders. Show me which skills were installed and how to use them.

| Skill | What you get | Try asking |
|---|---|---|
| [copywriting](skills/copywriting/SKILL.md) | Original, source-grounded copy in your voice | Write a seller email using my notes and approved examples. |
| [funnel-building](skills/funnel-building/SKILL.md) | A connected journey from first visit through delivery and follow-up | Build the path from my buyer-guide post to a delivered guide and consultation. |
| [sphere-activation](skills/sphere-activation/SKILL.md) | Clean contacts, relationship segments, and personal follow-up drafts | Combine my contact exports and prepare a CRM import and reactivation plan. |
| [prospecting-research](skills/prospecting-research/SKILL.md) | Sourced property research and a usable prospect shortlist | Use my permitted MLS data to research this neighborhood and explain which prospects deserve a closer look. |
| [cold-call-coach](skills/cold-call-coach/SKILL.md) | Researched call patterns, original scripts, and realistic practice | Study public FSBO calls, help me develop my approach, and role-play with me. |
| [lead-magnet-builder](skills/lead-magnet-builder/SKILL.md) | A finished guide plus promotion and a request-scoped delivery plan | Create a Listing Prep Package and the social post and video script that introduce it. |
| [lead-follow-up](skills/lead-follow-up/SKILL.md) | The next useful reply, appointment preparation, and CRM tasks | Read this actual inquiry and its history, then prepare the right next step. |
| [community-group-builder](skills/community-group-builder/SKILL.md) | Your own local group concept, launch material, and growth plan | Help me create a community Facebook group people in my area will want to join. |
| [realtor-website-builder](skills/realtor-website-builder/SKILL.md) | A website with verified contact and booking paths | Build my realtor website, then help connect my GoDaddy domain using the signed-in browser. |

The research skills work from the authenticated sessions, connected tools, or
permitted exports you provide. They keep missing information visible and use
actual responses and outcomes to improve the work. Public engagement and a
creator's claimed results are not guarantees of leads.

## Install

For an agent performing a requested installation: follow the user's and project's
skill-location instructions first. Choose the requested pack or individual skills;
install the entire library only when requested. Use a fresh checkout, copy whole
skill directories, and verify every installed folder has its `SKILL.md` and
referenced resources. Compare an existing destination before changing it; preserve
local customizations and do not replace a managed symlink with a copied directory.

Clone the repository into an unused directory:

```bash
git clone https://github.com/tderoussel/agent-skills.git agent-skills
```

The nine Realtor Starter Pack folders are `copywriting`, `funnel-building`,
`sphere-activation`, `prospecting-research`, `cold-call-coach`,
`lead-magnet-builder`, `lead-follow-up`, `community-group-builder`, and
`realtor-website-builder`.

Claude Code commonly reads `~/.claude/skills/`; an agent that reads
`.agents/skills/` can use that location instead. Project-local installation is
also supported when the harness and project instructions use it. These are
plain skill folders; choose the location your assistant actually discovers.

**Copy whole directories, not just `SKILL.md`.** References, scripts, and UI
metadata travel with the skill. The complete library contains 18 skill folders.
Invoking a skill by name can help: “Use cold-call-coach to help me practice.”

### As a plugin

The complete library is also a Claude Code plugin marketplace:

```text
/plugin marketplace add tderoussel/agent-skills
/plugin install agent-skills@agent-skills
```

---

## Process skills

| Skill | What it does |
|---|---|
| **`ship-gate`** | Verification gate to run *before* claiming something is shipped, merged, deployed, or green. Every rule is a case where the obvious check returned a false pass. |
| **`fleet-brief`** | Writes the brief for splitting work across parallel agents — exclusive per-lane file ownership, shared-ground warnings, and a DO-NOT list with reasons attached. |
| **`decision-council`** | Runs a decision through five independent lenses, blind peer review, and a chairman verdict, instead of giving you one agreeable answer. |
| **`overnight-build`** | Composes an unattended build prompt that survives usage-limit resets via checkpointing, plus the launcher that restarts it. Ships the full template. |
| **`competitive-teardown`** | Turns a competitor into a ranked build-or-ignore verdict, with a mandatory not-worth-copying section. |
| **`vault-doctor`** | Audits an Obsidian vault for broken links, unparseable frontmatter, and ambiguous filenames — classifying findings before proposing any repair. |
| **`inbox-triage`** | Sorts an inbox into needs-you / drafted / FYI / noise and writes the replies. Drafts only; never sends. |
| **`codebase-audit`** | Ranked, evidence-backed audit ending in a verify list that separates what was proven from what was inferred. |
| **`session-log`** | Writes a durable session record the next session can trust — with the two carry-forward sections everyone drops. |

Skills load when their description matches what you are doing, so mostly you
just work and they fire. You can also invoke one by name — "use ship-gate
before you tell me that merged."

`fleet-brief` and `overnight-build` compose well: derive the file ownership
first, then carry it into the unattended prompt.

---

## The agents

Four subagents that implement the build loop the skills describe: plan, build
in lanes, review, and read-only recon. They pair with `fleet-brief` — the
planner derives the lane ownership, the builders stay inside it, the reviewer
checks that they did.

| Agent | Role |
|---|---|
| **`planner`** | Maps files, assigns one owning lane per file, writes the plan. Does not write product code. |
| **`builder`** | Builds exactly one lane inside a worktree. Never merges its own work. |
| **`reviewer`** | Reads the diff line by line and returns an explicit verdict. Read-only. |
| **`researcher`** | Read-only recon. Every finding carries evidence and a verified/assumed marker. |

Install the requested agent files from `agent-skills/agents/` into the agent
location your harness supports. Compare existing files first and preserve local
customizations. Claude Code commonly uses `~/.claude/agents/`.

The core idea they encode: **nothing merges on its author's say-so.** The agent
that wrote a diff is the worst possible reviewer of it.

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
