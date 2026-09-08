---
name: overnight-build
description: Composes an autonomous unattended Claude Code build prompt that survives usage-limit resets via BUILD_LOG.md checkpointing, plus the launcher that restarts it. Use when the user asks for an overnight build, an autonomous build, a build to run while they sleep, an unattended or unsupervised session, or any long build they will not be monitoring. Trigger phrases include "overnight build", "run overnight", "build while I sleep", "autonomous build", "let it run", "unattended". Produces a single copyable prompt; does not run the build.
license: MIT
---

# Overnight build prompt

The full template lives at `references/overnight-build-template.md`. **Read it before composing.** Do not re-derive the rule structure from memory — fill its `[BRACKETED]` sections from the user's specifics, and preserve any edits they have made to their own copy.

## Non-negotiable

Every output must carry **Rule 8 (survive usage resets)** and the **LAUNCHER** section. They are what make the build restartable; a prompt without them silently restarts from scratch after the first usage reset and burns a night.

## Compose

1. **Read the template.** If the user keeps an edited copy, theirs wins — preserve their changes.
2. **Fill the specification** — what to build, context, design requirements, technical requirements, features in priority order, seed data, deployment, success criteria. Specificity here is the whole game; a vague spec produces a vague night.
3. **Set phases** — 4–8, each independently completable and verifiable, with time allocations that sum to the budget.
4. **Fill the pivot playbook** with project-specific blockers on top of the template's standing ones.
5. **Ask once** which launcher they want (A: OS scheduler · B: bash loop · C: a scheduled-task MCP) if the request doesn't say. Ask once — then proceed.
6. **Output as a single copyable code block**, and remind them to save it to `overnight-build-prompt.txt` in the project root before launching.

## Completion signalling

The prompt must instruct the build to emit `BUILD_COMPLETE` as its final line — the bash-loop runner greps for it to exit. State clearly, in the prompt, that **withholding `BUILD_COMPLETE` is correct** when any P0 criterion is genuinely unmet. A runner that exits on an unfinished build is worse than one that keeps going.

## Guardrails

An unattended agent has no one to ask, so the prompt must carry its own boundaries.

If the target is an existing production codebase, derive file ownership and a DO-NOT list first (the `fleet-brief` skill produces both) and carry the project's verification checks into the testing phase, so "done" means verified rather than merged.

**Never let an overnight prompt authorize** applying database migrations, pushing schema, deploying via a hosting CLI, purchasing or releasing phone numbers or domains, or sending outbound messages to real contacts. Those need a human awake. Add the project's own irreversible actions to that list.

## Deliverables the build must write

- `BUILD_LOG.md` — phase entries, decisions, pivots, known issues, and `## CHECKPOINT — <ISO>` blocks with the exact next step
- `RESEARCH_NOTES.md` — research findings before implementation begins

On resume, the build's literal first action is to read `BUILD_LOG.md` top to bottom and continue from the latest checkpoint — never re-research, re-scaffold, or restart.
