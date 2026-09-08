---
name: vault-doctor
description: Audits and repairs an Obsidian vault's structural health — broken [[wikilinks]], ambiguous duplicate filenames, missing or malformed frontmatter, stale status markers, and hub notes whose state sections have gone cold. Use when the user asks about vault health, broken links, vault cleanup, dead links, orphan notes, tag consistency, or says the vault feels messy or out of date. Trigger phrases include "vault health", "broken links", "clean up the vault", "audit the vault", "is the vault current". Read-only by default; every repair is proposed before it is made.
license: MIT
---

# Vault doctor

Most Obsidian vaults have **no git and no undo**, and many are live-synced through iCloud, OneDrive, or Dropbox. Treat every write as irreversible. Confirm the vault's actual backup situation before touching anything, read before you overwrite, prefer targeted edits over whole-file rewrites, and never run a rapid write loop — on a synced folder it produces conflict copies.

## Scan

Walk `.md` files, skipping `node_modules`, `.git`, `.obsidian`, and any build or scratch directories the vault has accumulated. Build the set of link targets from **every** file basename (attachments included, not just `.md`), then extract `[[targets]]`, stripping `|alias`, `#heading`, and `^block` suffixes.

Record a baseline — note count, distinct broken targets, total broken references, duplicated basenames — so later runs can show movement rather than repeating the same census.

## Classify before repairing

A raw broken-link count is not a defect list. Sort every hit into one of four buckets:

**1. Cross-system references — do not "fix".** Some targets are not vault notes at all: agent memory IDs, ticket keys, or identifiers from another tool that happen to be written in wikilink syntax. They will never resolve. Converting them to plain text is defensible; creating stub notes to satisfy them is not.

**2. Documentation of a broken link — never touch.** Some notes cite a broken link deliberately, as an example or as ground truth for an exercise ("if your tool doesn't find this, your tool is wrong"). Editing these breaks the thing they teach. Wikilink syntax quoted inside prose is the same class.

**3. Name drift — fix at the target, not the source.** When many references point at a short name and the note is filed under a longer one, **prefer adding `aliases: [ShortName]` to the target's frontmatter over editing every referring file.** One edit, a native Obsidian mechanism, no risk of mangling surrounding context.

**4. Genuinely missing notes.** The target never existed. Report it; do not auto-create. An empty stub is worse than a broken link because it looks answered.

## The find-and-replace prohibition

**Never repair links with an unscoped find-and-replace.** A blind replacement across a vault will mangle folder names, URLs, code blocks, and tag vocabularies that happen to contain the search string — and because there is no undo, the damage is permanent. Fix per-file, with the surrounding line read first.

## Other checks

- **Duplicate basenames** make links ambiguous vault-wide, because Obsidian resolves `[[links]]` by filename across the whole vault. The usual culprit is a code project or dependency tree living inside the vault, contributing thousands of phantom `.md` files. Flag it; the fix is moving the project out of the vault or adding an exclusion. **Do not delete anything without asking.**

- **Frontmatter must actually parse.** Run every block through a real YAML parser — do not eyeball it. The dominant failure is an unquoted plain scalar containing `: ` (colon-space), which fails at that character and **takes every key below it with it**, making the whole block invisible to Obsidian's Properties panel and to Dataview. A second common failure: an unquoted value beginning with `|` or `>` opens a YAML block scalar.

  Fixing means quoting values, which on a large load-bearing note can touch hundreds of keys — **propose it, never do it unprompted**, and back the file up first. Until it is fixed, match the existing (broken) convention rather than introducing a second style; a lone valid key inside an invalid block buys nothing.

- **Tags** belong in YAML as a list, not as inline hashtags — check against the vault's real vocabulary rather than an idealized one. Report drift; don't unilaterally re-tag.

- **Stale state** — notes carrying `PAUSED`/`STALLED`/`TODO` markers whose project has since moved on. Report them; do not resolve them yourself.

- **Cold hubs** — a hub note whose newest state section predates its project's latest activity is out of date. Report the gap.

## Output

A report, ordered by bucket, with counts and exact `file:line` references. Propose repairs; make only the ones the user approves.

State plainly which findings are **verified** and which are **inferred from naming** — a target that looks like drift may be a note they intend to write.
