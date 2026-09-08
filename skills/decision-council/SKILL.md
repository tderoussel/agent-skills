---
name: decision-council
description: Run a structured multi-perspective review of a decision instead of getting one agreeable answer. Use when the user says run a council, get me perspectives on this, should I do X, stress-test this decision, or is this a good idea.
license: MIT
---

# Decision council

## The problem this solves

Ask an agent "why is this a good idea?" and you get a well-argued case for yes. Ask "why is this a bad idea?" and you get an equally well-argued case for no. Both are fluent, neither is a judgment. A single agent is a bad advisor because it optimizes for a coherent answer rather than a correct one.

This runs several independent perspectives, has them reviewed by agents who don't know who wrote what, and produces one verdict.

## When to run it

Real forks with real cost: build vs. buy, ship vs. hold, pricing changes, whether a feature is premature, what to work on next. Not for questions with a known answer.

## Steps

### 1. State the decision precisely

Write it as one sentence with a real fork in it. If it can't be stated that way, the decision isn't clear enough to review yet — fix that first.

Gather what's actually known: constraints, what's already been tried, what's reversible and what isn't.

### 2. Spawn the council — in parallel, independent

Five agents, each with a genuinely different lens. They must not see each other's answers.

| Persona | Job |
|---|---|
| **The contrarian** | Assume this fails. What killed it? |
| **The optimist** | Assume it works. What did it unlock that's being undervalued? |
| **The operator** | Who does the work, what breaks, what's the real cost in the user's time? |
| **The customer** | Does the person paying actually care? Would they notice? |
| **The accountant** | What does this cost, what does it return, what's the opportunity cost? |

Each returns: a recommendation, the reasoning, and the one fact that would change its mind.

Swap a persona when the decision calls for it — a regulatory lens for a compliance fork, a security lens for an architecture one. Keep the lenses genuinely distinct.

### 3. Peer review, blind

Strip attribution and shuffle. Hand the anonymized set to fresh reviewers. Ask each: which argument is strongest, which is weakest, and what did all of them miss?

Blinding matters — it stops the review from deferring to whichever persona sounds most authoritative.

### 4. The chairman

One final agent reads the perspectives and the reviews and returns:

```markdown
## Decision: <the question>

**Verdict:** <the call, in one sentence>

**Confidence:** <high | medium | low> — <why>

**The reasoning that carried it:** <2-3 sentences>

**The strongest case against:** <state it fairly — do not strawman it>

**What would change this:** <the specific fact or event that flips the answer>

**If we proceed:** <first concrete step>
```

### 5. Report honestly

If the council split, **say it split.** A forced consensus is worse than a live disagreement — most people would rather see the real tension and make the call themselves.

Never manufacture agreement to look decisive.

## Scaling it

Five personas is the default. Three for a smaller call, seven for something expensive or hard to reverse. More personas only helps if the lenses are genuinely different — five distinct angles beat nine overlapping ones.

## Credit

The multi-persona-plus-blind-review-plus-chairman pattern comes from Ollie Leman, by way of Remy Gaskell's Open Residency episode on agent operating systems.
