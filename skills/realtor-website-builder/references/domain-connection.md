# Domain connection and launch receipt

Read during custom-domain work. Keep the owner's instructions simple; use this checklist for the assistant's technical work. Recheck official instructions at execution time rather than treating saved DNS values as current.

## Read the actual setup

- Confirm account identity, exact domain, registrar, authoritative nameservers, existing root/`www` behavior, host project and deployment, and desired canonical hostname.
- Read the host's current custom-domain page and official documentation. Get the required type, name, value, and verification records from that specific project. Do not reuse another customer's IP, domain, or validation token.
- Use the actual DNS provider. GoDaddy's [DNS management guide](https://www.godaddy.com/help/manage-dns-records-680) locates management according to nameservers; the registrar and DNS provider may differ.
- Save the relevant existing records and their TTLs in a local change plan without session secrets. Identify records used by email, existing subdomains, verification, and other services.

## Prepare the exact change

Use a small table, filled from live evidence:

| Field | Record in the change plan |
|---|---|
| Target | Exact domain, DNS provider account, and destination host project |
| Before | Current record type, name, value, and TTL, or confirmed absence |
| After | Host-required record type, name, value, and TTL |
| Reason | Which website hostname or host verification this connects |
| Dependencies | Existing website, email, other services, and relevant conflicts |
| Restore | Saved original values and the precise reversal for this change |
| Authority | Existing user instruction covering the exact change, or pending approval |

For GoDaddy, consult its [A record instructions](https://www.godaddy.com/help/add-or-edit-an-a-record-42546) or [CNAME instructions](https://www.godaddy.com/help/add-a-cname-record-19236) only as needed for the selected host's requirements. Do not replace host values with examples from help articles.

Treat these as dependencies to inspect, not a generic zone-cleanup job:

- MX records and their referenced mail hostnames, including an MX target that resolves through the root A record.
- SPF, DKIM, and DMARC TXT/CNAME records; other mail verification records.
- Nameservers, existing subdomains, certificate validation, forwarding, and third-party verification records.

Changing a website A record can affect mail when mail relies on that hostname; preserving MX alone is insufficient. Resolve a conflicting dependency before applying the plan. A separate mail or nameserver migration is not implied by a request to connect the website.

## Execute within authority

Use only documented, available tools or browser controls in the authenticated session. Let the owner enter credentials, complete multi-factor verification, and approve account security challenges. Do not export cookies, tokens, or passwords.

Apply only the reviewed authorized record changes. Record what was saved and when. If a tool fails or the browser blocks the action, inspect the actual state before retrying; an unknown outcome is not a successful change. Provide current official manual steps if automation is unavailable.

## Verify the finished path

Record each result as observed, pending, failed, or not tested:

| Check | Evidence to capture |
|---|---|
| Destination deployment | Correct host project and deployment state; actual page at host URL |
| Host domain verification | Provider confirms the intended domain belongs to the intended project |
| DNS | Authoritative answer and a fresh resolver answer match required records |
| HTTPS | Intended hostname loads with a valid certificate and no mixed-content failure |
| Root and `www` | Both follow the agreed canonical/redirect behavior without a loop |
| Content | Fresh custom-domain load shows this agent and the intended build |
| Form | Authorized designated test produces the saved lead with source/consent fields |
| Delivery | Required asset or confirmation arrives at the designated test destination |
| Booking | Correct event and timezone; only mark a booking confirmed after a provider-confirmed authorized test |
| Email dependencies | Relevant records and referenced hostname resolution remain intact; actual mail delivery only if an authorized test was performed |

Do not infer global propagation from one resolver or claim email delivery from unchanged MX records. Give the owner the actual working URL, precise outstanding condition, and a restoration plan if a change failed.
