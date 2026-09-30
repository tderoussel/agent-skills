#!/usr/bin/env python3
"""Prepare canonical contact CSVs locally; make only conservative duplicate merges."""
import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

FLAGS = ("do_not_contact", "email_opt_out", "sms_opt_out", "call_opt_out")
YES = {"true", "yes", "1"}
NO = {"false", "no", "0"}


def norm(value):
    return " ".join(unicodedata.normalize("NFC", value).split()).casefold()


def split_values(value):
    return list(dict.fromkeys(part.strip() for part in value.split("|") if part.strip()))


def email_key(value):
    value = norm(value)
    return value if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) else ""


def phone_key(value):
    value = value.strip()
    extension = re.search(r"(?:ext\.?|extension|x|#)\s*(\d+)\s*$", value, re.I)
    suffix = "x" + extension.group(1) if extension else ""
    base = value[:extension.start()].strip() if extension else value
    if not re.fullmatch(r"[+\d\s().-]+", base) or "+" in base[1:]:
        return ""
    digits = "".join(c for c in base if c.isdigit())
    if not 7 <= len(digits) <= 15:
        return ""
    return ("+" if base.startswith("+") else "") + digits + suffix


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    paths = [path.resolve() for path in args.inputs]
    if len(set(paths)) != len(paths) or len({p.name for p in paths}) != len(paths):
        parser.error("Use distinct input paths and distinct source filenames.")
    if args.output_dir.exists():
        parser.error("Output directory already exists; choose a new directory.")

    records, reviews, index, suppressions = [], [], defaultdict(list), defaultdict(set)
    for path in paths:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames or []
            if len(set(fields)) != len(fields):
                parser.error(f"Duplicate headers in {path.name}.")
            if "full_name" not in fields or not ({"emails", "phones"} & set(fields)):
                parser.error(f"{path.name} needs full_name and emails or phones headers.")
            for number, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    parser.error(f"Malformed CSV row {number} in {path.name}.")
                ref = f"{path.name}:{number}"
                record = {"row": row, "ref": ref, "source": path.name, "number": number,
                          "name": norm(row["full_name"]), "keys": [], "flags": {}}
                if len(record["name"].split()) < 2:
                    reviews.append(("incomplete_name", [ref], "full_name", [row["full_name"]]))
                for flag in FLAGS:
                    value = norm(row.get(flag, ""))
                    record["flags"][flag] = True if value and value not in NO else False
                    if value and value not in YES | NO:
                        reviews.append(("unknown_suppression_flag", [ref], flag, [row[flag]]))
                for kind, func in (("emails", email_key), ("phones", phone_key)):
                    for value in split_values(row.get(kind, "")):
                        key = func(value)
                        if not key:
                            reviews.append(("unparsed_contact_value", [ref], kind, [value]))
                            continue
                        pair = (kind, key)
                        record["keys"].append(pair)
                        index[pair].append(len(records))
                        channels = ("email",) if kind == "emails" else ("sms", "call")
                        for channel in channels:
                            if record["flags"]["do_not_contact"] or record["flags"][channel + "_opt_out"]:
                                suppressions[(channel, key)].add(ref)
                records.append(record)

    parent = list(range(len(records)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for (kind, key), indices in index.items():
        indices = sorted(set(indices))
        names = {records[i]["name"] for i in indices}
        if len(names) > 1:
            reviews.append(("shared_endpoint_keep_separate", [records[i]["ref"] for i in indices], kind, [key]))
            continue
        if len(next(iter(names)).split()) >= 2:
            for i in indices[1:]:
                parent[find(i)] = find(indices[0])

    groups = defaultdict(list)
    for i, record in enumerate(records):
        groups[find(i)].append(record)

    # Carry a person's explicit opt-outs onto all their merged endpoints before
    # applying endpoint restrictions to separate people sharing those endpoints.
    for group in groups.values():
        for channel, kind in (("email", "emails"), ("sms", "phones"), ("call", "phones")):
            restricted = any(r["flags"]["do_not_contact"] or r["flags"][channel + "_opt_out"] for r in group)
            if restricted:
                refs = {r["ref"] for r in group if r["flags"]["do_not_contact"] or r["flags"][channel + "_opt_out"]}
                for record in group:
                    for field, endpoint in record["keys"]:
                        if field == kind:
                            suppressions[(channel, endpoint)].update(refs)

    output, source_rows, contact_for_ref = [], [], {}
    for group in groups.values():
        refs = sorted(record["ref"] for record in group)
        contact_id = "contact_" + hashlib.sha256("\n".join(refs).encode()).hexdigest()[:16]
        for ref in refs:
            contact_for_ref[ref] = contact_id
        emails = sorted({v for r in group for v in split_values(r["row"].get("emails", ""))})
        phones = sorted({v for r in group for v in split_values(r["row"].get("phones", ""))})
        item = {"contact_id": contact_id, "full_name": group[0]["row"]["full_name"].strip(),
                "emails": "|".join(emails), "phones": "|".join(phones), "source_rows": "|".join(refs),
                "merge_count": len(group), "relationship": "", "last_contact": "", "field_conflicts": ""}
        conflicts = []
        for field in ("relationship", "last_contact"):
            values = sorted({r["row"].get(field, "").strip() for r in group} - {""})
            if len(values) == 1:
                item[field] = values[0]
            elif len(values) > 1:
                conflicts.append(field)
                reviews.append(("merged_field_conflict", refs, field, values))
        item["field_conflicts"] = "|".join(conflicts)
        global_suppressed = any(r["flags"]["do_not_contact"] for r in group)
        item["do_not_contact"] = "true" if global_suppressed else ""
        for channel, values, key_func in (("email", emails, email_key), ("sms", phones, phone_key), ("call", phones, phone_key)):
            excluded = {v for v in values if (channel, key_func(v)) in suppressions}
            # Conservatively suppress this channel if any endpoint is suppressed.
            # The endpoint index still retains the narrower reason and scope.
            suppressed = global_suppressed or bool(excluded) or any(r["flags"][channel + "_opt_out"] for r in group)
            item[channel + "_opt_out"] = "true" if suppressed else ""
            item[channel + "_suppressed_endpoints"] = "|".join(sorted(excluded))
        output.append(item)
        for record in group:
            source_rows.append({"contact_id": contact_id, "source": record["source"],
                                "source_row": record["number"], "source_contact_id": record["row"].get("source_contact_id", ""),
                                "original_json": json.dumps(record["row"], ensure_ascii=False, sort_keys=True)})

    review_rows = [{"issue": issue, "source_rows": "|".join(refs),
                   "contact_ids": "|".join(sorted({contact_for_ref[ref] for ref in refs})),
                   "field": field, "values_json": json.dumps(values, ensure_ascii=False), "decision": ""}
                  for issue, refs, field, values in reviews]
    suppression_rows = [{"channel": channel, "normalized_endpoint": endpoint, "source_rows": "|".join(sorted(refs))}
                        for (channel, endpoint), refs in sorted(suppressions.items())]
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)
    contact_fields = ["contact_id", "full_name", "emails", "phones", "source_rows", "merge_count",
                      "relationship", "last_contact", "field_conflicts", *FLAGS,
                      "email_suppressed_endpoints", "sms_suppressed_endpoints", "call_suppressed_endpoints"]
    write_csv(out / "contacts.csv", contact_fields, output)
    write_csv(out / "source-rows.csv", ["contact_id", "source", "source_row", "source_contact_id", "original_json"], source_rows)
    write_csv(out / "identity-review.csv", ["issue", "source_rows", "contact_ids", "field", "values_json", "decision"], review_rows)
    write_csv(out / "suppression-index.csv", ["channel", "normalized_endpoint", "source_rows"], suppression_rows)
    summary = {"input_files": len(paths), "input_contact_rows": len(records), "retained_source_rows": len(source_rows),
               "output_contact_records": len(output), "rows_combined_by_conservative_merge": len(records) - len(output),
               "identity_review_items": len(review_rows), "suppressed_endpoint_channel_pairs": len(suppression_rows),
               "globally_suppressed_contact_records": sum(item["do_not_contact"] == "true" for item in output),
               "network_calls": 0, "note": "Intermediate contacts, not outreach permission or a destination CRM import."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, csv.Error) as error:
        print(f"Contact preparation failed: {error}", file=sys.stderr)
        sys.exit(1)
