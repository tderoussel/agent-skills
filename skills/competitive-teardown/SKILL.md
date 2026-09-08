---
name: competitive-teardown
description: Researches a competing product against your own and produces a ranked build-or-ignore verdict, plus optional comparison-page copy. Use when the user names a competitor or asks how their product stacks up against one. Trigger phrases include "vs us", "competitor", "what does X have", "should we copy", "competitive gap", "teardown", "are we behind". Produces a ranked verdict with effort estimates and an explicit not-worth-copying list.
license: MIT
---

# Competitive teardown

The output is a decision, not a feature inventory. Every gap gets a rank, an effort estimate, and a build-or-ignore verdict.

## Method

1. **Research the competitor's current state** — pricing, positioning, what shipped in the last 6 months, what their users complain about. Date every claim; most categories move faster than the write-up survives.

2. **Audit your own repo for what already exists.** This is the step that changes the answer. Repeatedly, the highest-value "gaps" turn out to be dormant scaffolds already in the codebase with no callers, or a feature shipped behind a flag nobody turned on. Grep before concluding anything is missing.

3. **Filter through the actual user.** Name who your product serves, specifically, and judge each gap against that person. A feature that impresses in an enterprise demo can be worthless to a solo user, and vice versa. State who each gap serves — if the answer is "someone we don't sell to," that is the verdict.

4. **Rank by value to that user**, with a rough effort estimate and what makes it cheap or expensive.

## Structure

```markdown
# <Competitor> vs <Us> — Competitive Gap Analysis (YYYY-MM-DD)

<One line naming the research mode used.>

## Headline
<What their real edge is — usually not the thing they market.>

## Ranked gaps
1. **<Gap>** (~effort) — evidence from the repo, why it matters to our user, what to build.

## Explicitly not worth copying
<Named, with reasons.>

## Strategic read
<The durable lesson, separate from the feature list.>
```

## The not-worth-copying section is mandatory

It is the section that keeps the backlog honest. Without it, a teardown is a list of work you now feel behind on.

Features that demo well and often serve nobody in particular: custom objects, visual workflow canvases, kanban boards, collaboration surfaces on single-player products, and enrichment aimed at a buyer you don't sell to. Reject them by name, with the reason, so the next teardown doesn't re-propose them.

## Distribution beats features

When the competitor is larger, the threat is usually **how they reach the user** — bundling, a default integration, an incumbent relationship — not their feature set. Weigh that explicitly. A teardown that only compares features will recommend the wrong work.

## Standing constraints

Carry a short list of prior rulings so the teardown does not re-litigate settled decisions: things leadership has already declined to build, positioning claims that have been ruled out, and structural bets that are not up for debate. Add to it as verdicts are made.

Record them in the project's own copy of this skill — the point is that a competitor doing something is not, by itself, an argument to reverse a decision.

## Comparison pages

If the ask includes marketing copy, match whatever house pattern already exists rather than inventing one. Keep every factual claim about the competitor **dated and sourced** — these pages are public and a stale claim is a liability.

Leave them as drafts. **Do not publish a comparison page without a human's explicit approval.**

## Output

Write the analysis where the project keeps its research. If the teardown changes strategy, add a dated section to the relevant hub or plan — do not silently supersede a prior verdict.
