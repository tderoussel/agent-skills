---
name: agent-workflow-builder
description: Design, build, or repair a bounded AI workflow for a recurring job, with tool contracts, state, recovery, and observable completion. Use when connecting several steps into a working assistant or agent. Do not turn a simple question or a requested prompt draft into a system build.
license: MIT
---

# Agent Workflow Builder

Build the smallest workflow that completes a defined job and can explain what happened. Preserve the user's chosen platform and existing authorization. A design request produces a design; an implementation request carries the authorized work through verification.

## Define one useful run

Inspect the current procedure, representative inputs, and available environment before selecting an architecture. Identify the trigger, intended user, desired artifact or state, destination, and owner of exceptions. Reuse confirmed context instead of requiring a standard setup interview.

Write a compact completion contract containing:

- Input and output shapes, with a representative example.
- Authoritative sources and freshness requirements.
- Allowed actions and actions held for a person.
- A success check someone can observe.
- Time, turn, retry, or cost limits appropriate to the job.
- Conditions that require clarification, cancellation, or escalation.

Keep unknowns explicit. If tool access or execution is unavailable, complete the independent design work and identify the exact missing capability. Do not substitute a mock connection for a working integration or imply that a background service exists.

## Choose workflow edges before agent freedom

Encode known steps deterministically: parsing a file, validating a schema, retrieving a named record, calculating a total, or routing a known status should not require an open-ended model decision.

Use a model for the uncertain portion: interpreting a request, extracting ambiguous information, proposing a draft, or choosing a next step from evidence. Bound its choices with typed inputs and outputs. Add a loop only when the next action depends on an observed result; a fixed chain is usually easier to verify and recover.

Keep the existing harness when it can satisfy the contract. Check current official documentation for implementation-sensitive behavior rather than inventing tool names, lifecycle events, or persistence guarantees. Parallelize independent work only when it reduces useful elapsed time without shared-state conflicts.

## Make handoffs explicit

For each step specify its input, permitted tool or function, output, verifier, and next state. A useful state record includes a stable run ID, configuration version, source references, completed steps, pending action, and final stop reason.

Use states that expose unresolved work, such as waiting for input or approval, failed, cancelled, and complete. A queued request, a generated draft, and a completed external action are different states. Resume from the last confirmed checkpoint, not from a confident summary.

Give tools narrow contracts: validated arguments, scoped identity, structured results, timeouts, and meaningful errors. Distinguish a missing record from an unavailable service. Keep credentials in the platform's supported secret storage. Log the evidence needed to debug a run while minimizing personal data and full payload copies.

For external effects, define an idempotency key tied to the logical operation, not a new random key on each retry. Persist its status and receipt where the environment supports it. After an uncertain timeout, inspect the destination before retrying. If the destination cannot confirm whether the effect happened, hold that operation for a person rather than risk duplicating it. Read-only steps may be replayed when their source/version rules allow it.

## Bound failure and authority

Retry transient failures within an explicit attempt and elapsed-time budget. A validation failure needs a corrected input; a permission denial needs a legitimate access decision; neither benefits from blind retries. Stop on success, exhausted budget, repeated equivalent failure, cancellation, or a required human decision. Escalation should include the failed step, evidence, completed work, and safest next action.

Enforce critical rules outside model prose when the platform supports it. A pre-tool check may validate scope or an approval receipt; a post-tool check can verify schema or a resulting state. Use a hook, wrapper, or ordinary function only at a real supported boundary. Do not claim a logging callback can block execution. Preserve already-granted authorization without adding repeated approval ceremonies.

## Verify the whole path

Implement and test locally or in an appropriate isolated environment within the authorized scope. Use representative normal inputs and targeted cases for missing data, invalid model output, tool failure, duplicate delivery, uncertain timeout, and resume after interruption. Include instruction-in-data cases when external content influences actions. Use synthetic fixtures when real records are unnecessary, and label them.

Check both the artifact and the handoff: who receives it, whether the state changed once, and whether a failure remains visible. Capture run IDs, configuration, observed results, and limitations. Simulated recovery does not prove a live connector works; a live read does not prove an external write was delivered.

Return the workflow or implementation, input/output contracts, configuration and permission needs, verification evidence, and an operator's resume/disable/rollback path. Mark unexecuted checks **NOT RUN** and stop short of claiming operational readiness when the critical path remains unverified.
