---
name: ai-evals-architect
description: Design, run, or repair evaluations of AI prompts, retrieval, workflows, and agents. Use to compare versions, investigate recurring AI failures, calibrate graders, or establish an evidence-based release gate. Ordinary software unit testing alone does not require this skill.
license: MIT
---

# AI Evals Architect

Produce evidence for a specific decision about an AI system. A useful eval identifies which behavior changed, under what conditions, and whether the evidence is sufficient to act. It does not turn a subjective impression into an authoritative-looking average.

## Define the decision and tested boundary

Start with the current prompt or system, representative inputs, observed failures, and the user's acceptance criteria. Ask only for gaps that prevent a fair evaluation. State whether the test covers a component, retrieval step, workflow, or full agent run; do not use one layer's result to claim another layer works.

Record the primary behavior, important failure modes, intended users, baseline, proposed change, and relevant constraints such as latency, cost, or unauthorized actions. Declare the decision rule before inspecting candidate results. Use product-specific thresholds or label proposed thresholds for owner review; there is no universal passing score.

Version the system sufficiently to reproduce it: prompts, model/configuration, tool definitions, retrieval corpus or index, parsers, relevant environment, and permissions. Identify uncontrolled differences. Model names alone are not a complete run configuration.

## Build cases with provenance

Prefer observed successes and failures from authorized sources, supplemented by expert examples and clearly labeled synthetic cases. Minimize personal data. Keep a source reference rather than copying sensitive records when the eval can operate on a redacted fixture.

A case should contain:

```text
case_id, source_type, source_reference, input, available_context,
expected_behavior, unacceptable_behavior, reference_or_state,
grader_ids, severity, slice_tags, split
```

Expected behavior can allow several correct answers. For agent tasks, it may specify a final state and forbidden effects rather than a single ideal paragraph. Include counterexamples: cases where a tool should not be used, information should remain unknown, or an action should wait.

Separate development cases used for iteration from evaluation and held-out cases. Group near-duplicates and examples from the same underlying event before splitting. Use time-based separation when future behavior is the question. Prevent outcome information, reference answers, or held-out labels from leaking into system context, retrieval, examples, or tuning. Repeatedly inspecting a holdout converts it into development data; replace or reserve another decision set.

## Choose and calibrate graders

Use deterministic checks for schema, arithmetic, required fields, tool arguments, and observable state. Use a narrow anchored rubric for meaning-dependent judgments. Permit insufficient-evidence outcomes instead of forcing an arbitrary score.

A grader card states its criterion, allowed evidence, scoring rule, pass rule, critical-failure override, version, and known limitations. Model graders must treat candidate text as data, not instructions. Test clear passes, clear failures, borderline cases, and attempts to manipulate the grader.

Have an appropriate human label a calibration sample when judgment affects the decision. Compare automated and human judgments, inspect disagreements, and fix unclear cases or rubrics before optimizing the system. If no human review is available, mark the grader uncalibrated and limit the conclusion accordingly. Do not claim human equivalence from a few examples. For pairwise judging, hide configuration identity, vary presentation order, allow ties, and check order sensitivity on a sample.

## Run a fair comparison

Use the same cases and relevant conditions for baseline and candidate, changing only the intended variable where practical. For nondeterministic behavior, predeclare repeated trials and a seed policy where supported. Do not select only the best attempt.

The run manifest includes run ID, date, dataset/split version, tested configurations, grader versions, trial count, concurrency, timeouts, retry policy, and analysis rule. Set an execution budget; paid calls or external effects remain within existing authorization. Agent evals should use an isolated or dry-run environment unless the specific live action is authorized.

Store per-case outputs or permitted references, grader evidence, errors, latency, and usage where observable. Report transport failures, timeouts, invalid outputs, and task failures separately. A retry can demonstrate recovery, but must not erase the first failure. If execution is unavailable, deliver the harness/specification as **NOT RUN** without invented outputs or scores.

## Interpret and preserve the evidence

Report paired wins, losses, ties, and unchanged cases with denominators. Inspect meaningful slices and high-severity failures before aggregating. A gain on easy cases cannot cancel an unauthorized action or a serious regression. Distinguish measured quality from latency/cost tradeoffs.

Use uncertainty estimates only when the sample and method support them; explain the unit of analysis and limitations. Small or biased samples may justify an inconclusive result. Do not turn lack of statistical evidence into a claim of equality.

Return the eval brief, case bank, grader cards, run manifest or runnable instructions, comparison results, failure analysis, and **pass / fail / inconclusive** gate evidence. For confirmed defects, add a regression case and a nearby counterexample, then rerun affected and previously passing behavior. State what a human must still review and what evidence would change the decision.
