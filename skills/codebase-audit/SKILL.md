---
name: codebase-audit
description: Runs a ranked, evidence-backed audit of a product, codebase, or subsystem, ending in a verify list that separates proven findings from inferred ones. Use when the user asks for an audit, a gap analysis, a deep read, a bug hunt, a readiness check, a re-audit, a state reconciliation, or asks what they are not seeing. Trigger phrases include "audit", "gap analysis", "what am I missing", "deep audit", "readiness", "bug hunt", "review the whole thing". Produces findings and a verify list; does not fix.
license: MIT
---

# Codebase audit

An audit's value is the **ranking and the evidence**, not the length. A finding without a file path, query result, PR number, or row count is a hypothesis — label it as one.

## Ground the audit in code and production, not in documents

Project notes, plans, and status docs are **checkpoints, not authority**. Start from them to learn *what was claimed*, then verify against reality: the live commit, database state, PR checks, branch heads.

When the documents and the code disagree, **that disagreement is itself a finding** — often the most valuable one in the audit.

A claim about production requires a query against production. Pair this with a verification gate skill for the mechanics.

## Structure

```markdown
# <Scope> Audit (YYYY-MM-DD)

## TL;DR
<The three things that matter, and what you'd do first.>

## Part 1 — What you're not seeing (blind spots, ranked)
## Part 2 — Capabilities missing (ranked, each with a rough effort estimate)
## Part 3 — Existing capabilities that need improvement (ranked)
## Part 4 — Architecture changes (ranked, plain English)
## Part 5 — If I ran the next 30 days
## Verify list (discrepancies found during the audit)
```

**Rank everything.** An unranked list of 40 findings is an unactioned list of 40 findings.

## Check for dormant scaffolds before estimating

Attach a rough effort estimate to each gap and say what makes it cheap or expensive.

The single most valuable audit finding is usually this one: **most of the high-value "gaps" are days of work, not weeks, because the scaffolds already exist in the repo with no callers.** A feature that is already 80% built is a completely different decision from one that is not.

Grep for the thing before declaring it missing. A function with zero callers is the canonical case — the code is there, nothing invokes it, and every status document describes the feature as absent.

## The verify list

Every audit ends with the discrepancies it could not resolve. Each entry names:

- what was claimed
- what was observed
- what query or check would settle it

**This is the section the next session actually uses.** Write it even when it is short.

## The explicitly-not-worth-doing section

Name what you examined and deliberately rejected, with the reason.

Audits that only add to the backlog make the backlog useless. A finding you looked at and dismissed is worth more than one you never mention, because it stops the next audit from re-raising it.

## Held items are not gaps

Anything already marked as deliberately deferred, or held for an explicit human decision, is held **on purpose**. Do not list it as a gap.

Re-surfacing a deliberate hold as a finding is how held decisions get executed by accident.

## Output

Write the audit where the project keeps them. If it supersedes a prior audit, say **which one and what changed** — a folder of audits should stay readable as a sequence, not as a pile.
