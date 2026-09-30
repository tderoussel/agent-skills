# Contact preparation contract

Read this before using `scripts/prepare_contacts.py`. Convert each permitted source to UTF-8 CSV with the following canonical headers; retain all other columns because the source ledger keeps them.

| Header | Meaning |
|---|---|
| `full_name` | Person's supplied name; join supplied given/family components when reliable |
| `emails` | Supplied emails separated by `|`; do not invent or strip aliases |
| `phones` | Supplied phone values separated by `|`; preserve country notation and extensions |
| `source_contact_id` | Original source ID, if available |
| `relationship` | Supplied relationship label; blank means unknown |
| `last_contact` | Supplied timestamp; do not guess the timezone or meaning |
| `do_not_contact` | Global flag: true/yes/1, false/no/0, or blank unknown |
| `email_opt_out` | Same flag grammar, scoped to email |
| `sms_opt_out` | Same flag grammar, scoped to SMS |
| `call_opt_out` | Same flag grammar, scoped to calls |

Require `full_name` plus at least one of `emails` or `phones` as headers; blank cell values are allowed. Distinguish source consent evidence from these suppression flags; absence of an opt-out is not consent. An unrecognized nonblank flag is treated conservatively as suppressed and listed for review.

The helper merges only full names containing at least two supplied name tokens with an exact normalized, non-shared email or phone. It does not use addresses, fuzzy similarity, last names, or household relationships. It preserves original phone strings and compares compact digits while retaining an explicit `+` and any extension. It does not infer national dialing rules. It refuses repeated input paths and identical source filenames because ambiguous provenance would be unsafe.

Outputs:

- `contacts.csv`: locally deduplicated candidates with alternate values, inherited suppressions, endpoint suppressions, merge count, and field conflicts. This is an intermediate file, not a universal CRM import.
- `identity-review.csv`: ambiguous shared endpoints, incomplete identities, and merged-field disagreements. Preserve separate people until the review resolves them.
- `source-rows.csv`: original rows as JSON plus the intermediate contact ID and source row. Protect this as personal data.
- `suppression-index.csv`: channel and normalized endpoint pairs excluded by an explicit or conservatively interpreted source suppression.
- `summary.json`: input and output counts with units; no provider or network activity occurs.

An email or phone found by enrichment must be added to the relevant person's restrictions before CRM import. The script cannot know newly discovered identifiers or runtime consent rules. The agent must reconcile those later additions and CRM suppression semantics.

Intermediate `contact_id` values identify the source-row cluster in this preparation run. They are not persistent person IDs across reordered or new exports. Match existing CRM IDs or use an approved identity mapping before an update/import; never treat these hashes as the CRM's primary key.

Keep generated CSVs as machine data. They intentionally preserve original strings, including potentially dangerous spreadsheet-leading characters. Use a separate sanitized viewing copy if opening them in spreadsheet software; do not weaken provenance or corrupt international phone notation in the import copy.
