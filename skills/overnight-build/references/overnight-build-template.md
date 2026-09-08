# Overnight Build Template — Claude Code

Fill the `[BRACKETED]` sections and delete the instructional `//` lines before
pasting. Rule 8 plus the LAUNCHER section are what let the build survive a
usage-limit reset; do not remove them.

> **Use when:** you want an overnight autonomous Claude Code build session.
> **How it survives usage resets:** Rule 8 + BUILD_LOG.md checkpointing + external scheduler (see LAUNCHER section).
> **Fill in [BRACKETED] sections with specifics. Delete all instructional `//` lines before pasting.**

---

# SYSTEM DIRECTIVE — READ THIS FIRST

You are operating in full autonomy mode. You have been given [TIME BUDGET, e.g., "the next 8 hours"] to complete this entire project from start to finish. These rules are absolute and override any default behavior:

## Rule 1: Never ask for permission

Make every decision yourself — technology choices, design decisions, architecture, naming, copy, color schemes, file structure, deployment targets. If the instructions don't specify something, use your best judgment and move on. Do not pause to ask me anything. I am asleep / unavailable / not monitoring this session.

## Rule 2: Never stop until finished

You are not done until every item in this prompt is implemented, tested, debugged, and deployed (if deployment is required). Do not send partial updates. Do not send "here's what I've done so far." Do not ask if I want to continue. Keep working until the deliverable is complete.

## Rule 3: If blocked, pivot immediately

If any external service, tool, API, CLI, or dependency:

- Requires browser-based authentication you cannot complete
- Requires account creation you cannot perform
- Times out, rate-limits, or errors repeatedly (3+ attempts)
- Is unavailable, deprecated, or broken

Then immediately switch to an alternative and keep building. Do not spend more than 5 minutes troubleshooting any single blocker. The project matters more than any specific tool.

**Common pivot paths:**

- Netlify blocked → try Vercel → try Cloudflare Pages → try Surge.sh → try GitHub Pages → try Render
- npm package broken → find alternative package or build it yourself
- API key required → mock the data and build the UI around it, note it as a limitation
- Database service down → use localStorage / JSON files / SQLite as a fallback
- Image CDN blocked → use base64 inline, placeholder images, or generate SVGs

## Rule 4: Work in phases, log your progress

Complete each phase fully before starting the next. After finishing each major phase, append a timestamped entry to `BUILD_LOG.md` in the project root:

```
## Phase [N]: [Name] — [Timestamp]
- What was completed
- Any decisions made
- Any pivots taken
- Any known issues
```

## Rule 5: Quality over speed

You have [TIME BUDGET]. Use it. Do not rush through implementation to "finish fast." Spend real time on:

- Research (first 10-15% of time budget)
- Architecture and planning (next 5-10%)
- Implementation (50-60%)
- Testing and debugging (15-20%)
- Polish and deployment (10-15%)

## Rule 6: Test everything before declaring done

Before you send your final message, every feature must be:

- Functionally working (click every button, fill every form, test every flow)
- Visually correct at mobile (375px), tablet (768px), and desktop (1440px)
- Free of console errors, broken links, missing assets, and layout breaks
- Deployed to a live URL (if deployment was requested)

## Rule 7: One final message only

Your ONLY communication to me is a single final message when the entire project is complete. This message must contain:

1. **Status:** "Complete" or "Complete with limitations"
2. **Live URL** (if deployment was requested)
3. **What was built** — feature summary, every major component
4. **Tech stack** — what you chose and why (1-2 sentences per choice)
5. **Architecture overview** — folder structure, key files, data flow
6. **Testing summary** — what was tested, how, results
7. **Known limitations** — anything mocked, stubbed, or incomplete, with notes on what a V2 would need
8. **Setup instructions** — how someone else would run this locally
9. **Recommendations** — what to build next, what to improve

Do NOT send anything before this final message. No progress updates, no questions, no "I've completed phase 1" messages. Nothing until it's all done.

## Rule 8: Survive usage resets

Claude Code has usage limits that reset on a cadence (typically every 5 hours or at a daily boundary). This build session is longer than one usage window. You MUST be restartable without losing state.

**Continuous checkpointing:**
- After every file creation, significant edit, or decision, ensure `BUILD_LOG.md` is current.
- If you hit a usage-limit error, a retryable condition that will fail repeatedly, or any state where you cannot make forward progress: append a `## CHECKPOINT — [ISO timestamp]` entry to `BUILD_LOG.md` before exiting.
- A checkpoint MUST include: last completed phase, current phase, specific files in progress (with paths), any blockers, any decisions pending, and the **exact next step** required to resume.
- Exit gracefully — do NOT retry repeatedly and burn tokens on failing requests.

**On resume (Claude Code restarts after usage reset via external scheduler):**
1. **Your literal first action is `Read BUILD_LOG.md` top to bottom** — before reading anything else, before scaffolding anything, before touching the filesystem
2. Also read `RESEARCH_NOTES.md` if it exists
3. Locate the latest `## CHECKPOINT — [timestamp]` entry
4. Resume from the exact next step noted there — do NOT restart the project from scratch, do NOT re-research, do NOT re-scaffold, do NOT ask me any questions
5. Append a `## RESUMED — [ISO timestamp]` entry to `BUILD_LOG.md`
6. Continue the build

**Assume resumes happen.** Write your state as if you will be killed and revived multiple times.

---

# PROJECT SPECIFICATION

// Replace everything below with your actual project details.
// The more specific you are, the better the output.
// Include: what to build, who it's for, how it should look, how it should work,
// what tech to use (or let Claude decide), design preferences, example sites to reference,
// seed data requirements, deployment target, and success criteria.

## What to build

[Describe the product/feature/app in detail. Be as specific as possible about what it does, who uses it, and what the core user flows are.]

## Context & background

[Any strategy documents, competitive research, brand guidelines, existing code, or prior work that informs this build. Paste key excerpts or reference files.]

## Design requirements

[Visual style, color palette, typography, layout preferences, reference sites or screenshots, specific UI patterns you want (e.g., swipe cards, kanban boards, chat interfaces). If you have brand colors or fonts, specify them exactly.]

## Technical requirements

[Preferred stack (or "your choice"), required integrations, performance targets, accessibility requirements, browser/device support. If there's an existing codebase, describe the structure and where new code should go.]

## Features — in priority order

[List every feature that must be built, ordered by importance. Be specific about each one — what it does, how it looks, edge cases to handle. Group into "Must have," "Should have," and "Nice to have" if helpful.]

## Seed data / content

[If the app needs mock data (user profiles, posts, products, etc.), describe what it should look like, how much of it, and the level of realism required.]

## Deployment

[Where should this be deployed? Any specific domain, hosting provider, or CI/CD requirements? If you don't care, say "deploy to any publicly accessible URL."]

## Success criteria

[How do you define "done"? What must be true for this to be considered complete? Be as concrete as possible — e.g., "All 12 pages render without errors, the checkout flow processes a test transaction, and the site scores 90+ on Lighthouse performance."]

---

# RESEARCH PHASE

// Customize this section based on what research your project needs.
// Delete categories that don't apply.

Before writing any code, spend [15-45 minutes] researching:

## Competitive / reference research

[List 3-7 sites or products to study. For each, note what to look at — UX patterns, feature set, design language, content strategy, pricing, etc.]

## Technical research

[What technical decisions need to be researched? Libraries, frameworks, APIs, deployment options, database choices, etc.]

## Design research

[Dribbble/Behance searches, specific UI patterns to study, design system references, etc.]

Document all research findings and decisions in `RESEARCH_NOTES.md` before proceeding to implementation.

---

# IMPLEMENTATION PHASES

// Break your project into 4-8 phases. Each phase should be a coherent chunk
// that can be completed and verified independently.
// The phases below are a template — replace with your actual phases.

## Phase 1: [Foundation — Project Setup & Architecture]

**Time allocation:** [X minutes]

[What to set up: project scaffolding, design system, shared components, data models, routing, auth scaffolding, etc.]

## Phase 2: [Core Feature #1]

**Time allocation:** [X minutes]

[Detailed spec for the most important feature. Include: UI layout, component breakdown, data flow, interactions, animations, edge cases, empty states, error states.]

## Phase 3: [Core Feature #2]

**Time allocation:** [X minutes]

[Same level of detail as Phase 2.]

## Phase 4: [Core Feature #3]

**Time allocation:** [X minutes]

[Same level of detail.]

## Phase 5: [Secondary Features]

**Time allocation:** [X minutes]

[Features that are important but not the core loop.]

## Phase 6: [Seed Data & Content]

**Time allocation:** [X minutes]

[Creating realistic mock data, writing copy, generating placeholder images, etc.]

## Phase 7: [Testing & Debugging]

**Time allocation:** [X minutes]

Test every single feature:

[Include a specific checklist of everything to test. Be exhaustive. Example:]

- Landing page loads, responsive at all breakpoints
- [Feature 1] works end-to-end
- [Feature 2] works end-to-end
- No console errors on any page
- All animations smooth at 60fps
- Forms validate correctly
- Empty states display properly
- Error states handled gracefully
- All links/buttons functional
- Images/assets load correctly
- Mobile touch interactions work

Fix every issue. Re-test after fixes. Repeat until clean.

## Phase 8: [Polish & Deploy]

**Time allocation:** [X minutes]

[Favicon, meta tags, OG image, loading states, performance optimization, README, deployment steps.]

---

# PIVOT PLAYBOOK

// Pre-define fallback strategies for common blockers.
// Add any project-specific pivots.

If you encounter any of these blockers, execute the corresponding pivot without hesitation:

| Blocker | Pivot |
|---|---|
| Deployment service requires browser auth | Try: Vercel CLI (`vercel --yes`) → Cloudflare (`wrangler pages deploy`) → Surge (`surge dist/`) → Netlify Drop (drag-and-drop) → GitHub Pages |
| Database service unavailable | Use localStorage for state persistence + JSON files for seed data. Note as limitation. |
| External API requires key you don't have | Mock the API response with realistic static data. Build the UI to consume real API shape so it's easy to swap later. |
| npm package fails to install | Find alternative package. If no alternative, implement the feature yourself. |
| Image hosting/CDN blocked | Use inline SVGs, DiceBear avatars (`api.dicebear.com`), UI Avatars (`ui-avatars.com`), or base64-encoded placeholders. |
| Font CDN blocked | Download fonts, bundle them locally in the project, and load via @font-face. |
| Build fails after changes | Read the error carefully. Fix the root cause. Do not revert all changes — isolate the problem. |
| Feature is taking 2x longer than allocated | Implement the 80% version. Ship it. Note the remaining 20% as a limitation. |
| You realize the architecture is wrong mid-build | If you're <30% done, refactor. If >30% done, work with what you have and note the architectural debt. |
| **Usage limit hit** | **Checkpoint to BUILD_LOG.md per Rule 8. Exit gracefully. External scheduler will resume.** |

---

# QUALITY STANDARDS

// These are the minimum quality bars. Customize per project.

## Code quality

- Clean, readable code with meaningful variable/function names
- Components are modular and reusable
- No hardcoded values where variables should exist (colors, spacing, copy)
- TypeScript preferred (if using JS framework). At minimum, add JSDoc types.
- No `any` types in TypeScript (use proper interfaces)
- No commented-out dead code in the final build

## Design quality

- Consistent spacing system (4px/8px base grid)
- Typography hierarchy is clear (no two text elements should look the same unless they serve the same purpose)
- Color palette is cohesive (3-5 colors max, used intentionally)
- Interactive elements have hover, active, focus, and disabled states
- Animations serve a purpose (feedback, orientation, delight) — not decoration
- Dark mode preferred unless the project specifies otherwise
- NEVER use default/generic AI aesthetics (Inter font, purple gradients, rounded rectangles with drop shadows)

## UX quality

- Every screen has a clear primary action
- Empty states are designed (not blank white screens)
- Loading states exist for any async operation
- Error states are helpful ("Something went wrong" is not acceptable — say what happened and what to do)
- Forms auto-save when possible
- Navigation is obvious and consistent
- Mobile-first — the app must work on a phone

## Performance

- Initial load under 3 seconds
- Lighthouse performance score > 80
- No render-blocking resources
- Images optimized (lazy-load below the fold)
- Fonts loaded with `display=swap`

---

# REMINDER

You have [TIME BUDGET]. That is a lot of time. Use it wisely:

- Don't skip research. Understand what you're building before you build it.
- Don't skip design. A beautiful product earns trust. An ugly product doesn't.
- Don't skip testing. Every untested feature is a bug waiting to happen.
- Don't skip polish. Favicons, meta tags, loading states, empty states — these are the difference between "prototype" and "product."

**The only message I want from you is the final deliverable. Make it count.**

Go.

---

---

# LAUNCHER — HOW TO SET UP AUTO-RESUME

The prompt above is the "what to do" inside a session. This section is how to launch it so it survives usage-limit resets.

## Option A — Windows Task Scheduler

**1. Save the filled-in prompt** to `overnight-build-prompt.txt` in the project root.

**2. Create the kickoff task:**
- Open Task Scheduler → Create Task
- Name: `Overnight Build - Kickoff`
- Trigger: One-time at desired start (e.g., 8:00 PM)
- Action: Start a program
  - Program: `C:\Program Files\Git\bin\bash.exe`
  - Arguments: `-c "cd /c/Users/<you>/Projects/<project> && claude -p \"$(cat overnight-build-prompt.txt)\" --dangerously-skip-permissions >> overnight-runner.log 2>&1"`

**3. Create the resume task:**
- Name: `Overnight Build - Resume`
- Trigger: Daily, starting at reset-time + 30 min (e.g., 12:30 AM)
- Recurrence: Every 5 hours for the following 8 hours (matches typical Claude usage-reset cadence)
- Action: Start a program
  - Program: `C:\Program Files\Git\bin\bash.exe`
  - Arguments: `-c "cd /c/Users/<you>/Projects/<project> && claude -c --dangerously-skip-permissions >> overnight-runner.log 2>&1"`
  - (`-c` = continue last conversation)

**4. When build completes:** disable both tasks manually, or have the final message from Claude include `echo DONE > overnight-runner.log` and let a third "kill" task detect and disable.

## Option B — Bash loop wrapper (simpler, keeps a terminal open)

Save as `overnight-runner.sh` in the project root:

```bash
#!/bin/bash
set -u
cd "$(dirname "$0")"

PROMPT_FILE="overnight-build-prompt.txt"
LOG="overnight-runner.log"
FIRST_RUN=true

while true; do
  if $FIRST_RUN; then
    PROMPT="$(cat $PROMPT_FILE)"
    FIRST_RUN=false
  else
    PROMPT="Read BUILD_LOG.md top to bottom. Locate the latest ## CHECKPOINT entry. Resume from the exact next step noted there. Append a ## RESUMED entry to BUILD_LOG.md with today's ISO timestamp, then continue the build per Rule 8."
  fi

  echo "$(date -Iseconds): Starting claude session" >> "$LOG"
  claude -p "$PROMPT" --dangerously-skip-permissions >> "$LOG" 2>&1
  EXIT=$?

  # Break if build signaled completion
  if grep -q "^BUILD_COMPLETE" "$LOG" 2>/dev/null; then
    echo "$(date -Iseconds): BUILD_COMPLETE detected — exiting runner." >> "$LOG"
    break
  fi

  # Otherwise assume usage limit — sleep until next reset window
  echo "$(date -Iseconds): Exit $EXIT — sleeping 30 min until retry" >> "$LOG"
  sleep 1800
done
```

Launch: `nohup bash overnight-runner.sh > /dev/null 2>&1 &`

Monitor: `tail -f overnight-runner.log`

Tell Claude in the initial prompt to write `BUILD_COMPLETE` as its final line so the runner exits cleanly.

## Option C — Claude Code `scheduled-tasks` MCP (if configured)

If the `scheduled-tasks` MCP server is set up:

1. Create a scheduled task:
   - Name: "Overnight build resume"
   - Schedule: Every 5 hours starting [start + 5h]
   - Action: Run `claude -c` (continues last session)

2. The initial kickoff session reads the full prompt; each scheduled firing is a `-c` continuation that triggers Rule 8 resume flow.

## Which option to pick

| If you want... | Use |
|---|---|
| Native Windows integration, survives reboots | **Option A (Task Scheduler)** |
| Simplest one-file setup, ok to leave terminal running | **Option B (Bash loop)** |
| Clean if you're already using scheduled-tasks MCP | **Option C (MCP)** |

---

# NOTES FOR THE AGENT COMPOSING THIS

When asked for an **overnight build prompt** (or: "autonomous build", "run
overnight", "build while I sleep", "unattended"):

1. **Use this document as the source of truth** — do not re-derive the rule
   structure from memory.
2. Fill in the `[BRACKETED]` sections from the project's specifics.
3. Include Rule 8 (resume survival) and the LAUNCHER section in every output.
   They are non-negotiable — without them the build restarts from scratch after
   the first usage reset.
4. Ask **once** which launcher option is wanted (A/B/C) if the request does not
   say, then proceed.
5. Output the prompt as a single copyable code block.
6. Remind the user to save it to `overnight-build-prompt.txt` in the project
   root before launching.

If the user edits their copy of this template — adds rules, changes launcher
guidance, adds quality bars — preserve their changes on future reads.
