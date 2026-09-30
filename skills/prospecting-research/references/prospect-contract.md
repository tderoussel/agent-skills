# Prospect and claim contract

Produce the fields the source can actually support. Keep unavailable values blank with a reason rather than inventing a complete-looking file.

## `prospects.csv`

| Field group | Required content |
|---|---|
| Identity | `opportunity_id`, `property_id`, parcel/listing ID when available, complete address and unit, `contact_id` if verified |
| Strategy | Strategy name, exact observed qualifying facts, and query version |
| Status | Raw listing status, normalized status if useful, status effective date, last verified timestamp, representation status including unknown |
| Ownership | Owner-of-record value, person/entity distinction, ownership source and date, match confidence expressed as a reason |
| Property signals | Actual acquisition/build dates or mailing mismatch; distinguish fact from interpretation |
| Contacts | Verified contact fields, source, match basis, last checked date, and confidence reason; keep candidates separate |
| Eligibility | Suppression flags, available consent evidence, restricted path, and why a record is held |
| Priority | Research-ready/needs-verification/hold, factual factors, and no demographic score |
| Action | Useful offer, next research or conversation action, and assigned date if requested |
| Provenance | Original record URLs or IDs, source dates, retrieval timestamps, and claim-ledger links |

Store one opportunity per property/strategy combination. Retain a separate owner table or contact IDs to avoid repeatedly treating one owner as several new prospects. Preserve unit numbers and source IDs as text.

## `claims.csv`

Use `claim_id, opportunity_id, field, claim, status, original_value, source_url_or_id, source_effective_date, retrieved_at, limitation`.

- **Verified:** the inspected source directly supports this statement, within the date and access limits stated.
- **Inferred:** evidence suggests this interpretation but does not establish it. State the reasoning and what would disprove it.
- **Unknown:** insufficient evidence, inaccessible source, or unresolved contradiction. Do not bury it in a confidence percentage.

Do not call a debt-free property verified from ownership tenure or the absence of a mortgage in an incomplete dataset. Do not infer age or selling motivation from house size, stairs, household composition, or name.

## Market calculations

For any local statistic, record area, property filters, observation period, eligible sample size, exclusion rules, source date, and definition of the metric. Distinguish original and cumulative days on market. Separate list-to-sale ratio, offer count, sale price, and buyer demand; none is interchangeable with another.

If a sample is too small or the market includes unlike property types, show the records and the uncertainty instead of an authoritative-looking headline. A known buyer requirement should have its own current agent-supplied evidence rather than being inferred from market averages.

## `research-review.csv`

Use `opportunity_id, issue, conflicting_sources, observed_values, consequence, exact_next_check, status`.

Prioritize issues that could change the contact or the claim: active relisting, wrong unit, wrong owner, entity/person mismatch, shared phone, stale contact field, and a field incorrectly treated as intent. Resolve these before releasing a contact-ready batch.
