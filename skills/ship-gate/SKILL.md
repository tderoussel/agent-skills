---
name: ship-gate
description: Verification gate for a Next.js-on-Vercel + Supabase + GitHub Actions stack, to run before claiming anything is shipped, deployed, live, merged, passing, or done. Use before saying a change is in production, before merging a PR, before reporting CI green, and before writing any status into a document — even if the user does not ask for verification. Trigger phrases include "is it live", "did it deploy", "ship it", "merge it", "is CI green", "confirm prod", "did that work". Encodes traps where the obvious check returns a false pass.
license: MIT
---

# Ship gate

Every rule here exists because the obvious check once returned a false pass. Run the gate before the claim, not after.

Adapt the specifics to your stack; the shape — *what would make this claim false?* — is the transferable part.

## The claim rule

**A claim about production requires a query against production.**

A passing test is not prod. A merged PR is not prod. A green deploy is not prod. Each of those is a claim about a different system than the one you are asserting on.

If no human has eyeballed the result, it is not "verified" — say what you actually checked instead.

## Deploy verification

- **Know what actually triggers a deploy.** On a git-integrated host it is the push, not a CLI invocation. Deploying by CLI when the project deploys by push produces a build that is not the one users get.
- **Check the account that owns the project.** A locally logged-in CLI may be authenticated as a personal account that does not own the production project — every command then succeeds against the wrong target, silently.
- Verify with commit status against the **deployed SHA**, not a dashboard glance.
- Confirm the deployment that is *current production*, not merely one that is READY. Several can be ready at once.
- **Edge/serverless functions deploy separately from the app.** A merged PR does not deploy an edge function; check its version explicitly.
- Client-only changes may need **no** function deploy — don't wait for one that will never come.
- Re-fetch the live manifest before asserting a version. Parallel work bumps versions underneath you.

## CI verification

- Gate on **every required context**, not the first green one.
- **Never gate on a piped command.** `some-check | tail` reports the exit code of `tail`, masking the real failure. In shells without `PIPESTATUS` (zsh differs from bash here), this is easy to get wrong — check the command's own status.
- **`steps: 0` means the job never ran**, not that it passed. A checks API can report a conclusion for a job that did no work.
- A suspiciously fast failure with no steps is usually a **billing or permissions** problem, not a YAML problem.
- Re-running only failed jobs replays a **stale snapshot** of the branch. Update the branch first, then re-run.
- **A checks list omits jobs that were never created.** Absence of a failure is not evidence of a pass.
- `gh pr create` requires an explicit `--base`. Chained heredocs around it can fail silently.

## Type and lint gates

- Large TypeScript projects may need an **increased Node heap**; without it `tsc` dies in a way that looks like a code error.
- **Know which directories your typechecker and linter actually cover.** Edge-function directories are frequently excluded from both. If they run on a different runtime, check them with that runtime's own checker — a test job is not a type gate.
- Build in worktrees or clean checkouts, not a working directory with uncommitted drift.

## Database

- **Never** push schema or run migrations casually against production. Apply schema through the reviewed path the project has chosen, once.
- **Call new stored procedures against the real database before believing them.** Mocks hide runtime errors that only appear with real types and real ambiguity.
- If the test suite mocks the database globally, **a passing unit test proves nothing about the database.**
- Never compare-and-set on a trigger-managed column — the trigger changes it underneath the write.
- **Measure a change's blast radius against production data before merging.** A filter that looks narrow against a local seed can match a very different share of real rows.

## Environment traps

- **Never assume the machine's timezone — run `date`.** Date-dependent tests fail on the offset, and the failure looks like a code bug.
- An unset git identity can block deploys and surface as an unrelated network error.
- Set host environment variables from a file rather than inline assignment; shells and CLIs can embed trailing newlines that corrupt the value invisibly.
- Scheduled-job success is not job-effect success: a runner reporting `succeeded` means the invocation returned, not that the work happened. Verify the effect.

## Output

State each gate as **PASS (evidence)** or **NOT CHECKED (why)**.

Never imply a gate ran when it did not. If any gate fails or is unchecked, say plainly that the change is not verified — **withholding the claim is correct.**
