---
name: fleet-brief
description: Authors a workstream brief for dispatching multiple parallel build agents across one codebase, with per-lane file ownership, shared-ground warnings, and a derived DO-NOT list. Use whenever work is about to be split across concurrent agents, workers, lanes, or waves — even if the user does not say "write a brief". Trigger phrases include "fan out", "parallel agents", "orchestrate this", "split into lanes", "workstreams", "run these in parallel", "review-gated build". Produces the brief; does not dispatch.
license: MIT
---

# Fleet brief

Parallel agents fail on **shared ground** — two lanes editing one file. The brief exists to make that collision impossible before dispatch. Derive the boundaries from the real file map; never assume them.

## Build the brief in this order

### 1. Map the files first

Before defining lanes, list the files each proposed change would touch. Read them. A lane defined without reading its files is a collision waiting to happen.

### 2. Assign exclusive ownership

Every file has **exactly one owning lane**. Produce this table:

| Lane | Owns (writes) | Reads only |
|---|---|---|
| W1 — <name> | `path/a.ts`, `path/b.ts` | `path/shared.ts` |

If two lanes need to write one file, you have three options — pick one explicitly, never leave it ambiguous:

- **Sequence** them (W2 waits for W1's merge)
- **Collapse** them into one lane
- **Seam** it: one lane adds an extension point, the other consumes it

### 3. Name the shared ground

List every file that more than one lane *reads*, and state who may write it.

Derive this list from the codebase in front of you — do not carry another project's list over. The recurring shapes worth checking for:

- **The live inbound path.** Whatever receives webhooks or user traffic. Concurrent edits here fail in production, not in tests.
- **Engine and dispatcher modules** that several features call into.
- **Append-only manifests** — deploy configs, route tables, function lists. Platforms impose limits (function counts, file sizes); two lanes appending independently can breach one.
- **Widely-imported exports.** Extend additively; a rename ripples through every caller.
- **Generated or vendored files** no lane should hand-edit.

A file that has caused a collision once is shared ground permanently. Record it in the brief so the next fleet inherits the knowledge.

### 4. Derive the DO-NOT list

Each DO-NOT names a file or behavior **and the reason**. Bare prohibitions get ignored; grounded ones hold.

Entries that generalize across most codebases:

- Never `git add -A` during conflict resolution — it stages the conflict markers and other lanes' work.
- Workers do not commit in linked worktrees; the orchestrator commits.
- If the test suite mocks the database globally, a green unit test proves nothing about the database. Say so explicitly.
- Do not add dependencies without a one-line justification.
- Do not apply schema migrations from inside a lane. Defer them to a single reviewed step.
- Watch for CLI calls that fail silently — e.g. `gh pr create` needs an explicit `--base`, and chained heredocs can swallow errors.

Then add the project-specific ones. Every incident that cost you a night belongs here, with its reason attached.

### 5. Set the gate

State explicitly, per lane: what "done" means, what evidence proves it, and who reviews before merge.

The default worth keeping is **review-before-live** — build, then independent line review, then must-fix rounds, then merge. Never merge a lane on its own author's say-so. The author's agent is the worst possible reviewer of its own diff.

### 6. Mark what is held

A `Deliberately NOT done — needs a human` section. Items held for an explicit go are held on purpose. **Do not let a lane execute one because it looks ready.**

## Isolation

Run builds in git worktrees, never the main checkout — a fleet that shares one working directory will interleave edits. If lanes mutate overlapping files despite the map, give each its own worktree.

## Sizing

Lanes should be independently mergeable. If a lane cannot merge without another lane's PR, it is not a lane — it is a phase. Sequence phases; parallelize lanes.

## Output

Write the brief to wherever the project keeps its plans, and open it with a "verify, never assume" warning. Status lines in any source document are checkpoints, not authority — re-check the live commit, database state, PR checks, and worktree heads before dispatching against them.
