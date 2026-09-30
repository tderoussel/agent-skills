#!/usr/bin/env python3
"""Exercise contact identity and suppression edge cases with fictional local data."""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("prepare_contacts.py")
FIELDS = ["full_name", "emails", "phones", "relationship", "do_not_contact", "email_opt_out", "sms_opt_out", "call_opt_out"]


class ContactPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="realtor-contact-test-")
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_input(self, name, rows):
        path = self.base / name
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def run_helper(self, *inputs, output="prepared"):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, inputs), "--output-dir", str(self.base / output)],
                                capture_output=True, text=True)
        return result

    def read_rows(self, name):
        with (self.base / "prepared" / name).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_identity_shared_household_international_and_provenance(self):
        malicious = '=HYPERLINK("https://example.test","name")'
        path = self.write_input("contacts.csv", [
            {"full_name": "Alex Morgan", "emails": "alex@example.test", "phones": "15550101010", "relationship": "past client"},
            {"full_name": " alex   MORGAN ", "emails": "ALEX@example.test", "phones": "15550101011", "sms_opt_out": "true", "relationship": "known contact"},
            {"full_name": "Jamie Morgan", "emails": "family@example.test", "phones": "15550101012", "email_opt_out": "yes"},
            {"full_name": "Sam Morgan", "emails": "family@example.test", "phones": "15550101012", "call_opt_out": "true"},
            {"full_name": "Chris", "emails": "chris@example.test"},
            {"full_name": "Chris", "emails": "chris@example.test"},
            {"full_name": "Taylor Reed", "phones": "+44 20 7946 0001"},
            {"full_name": "Taylor Reed", "phones": "44 20 7946 0001"},
            {"full_name": "Zoë García", "emails": "zoe@example.test"},
            {"full_name": malicious, "emails": "formula@example.test", "do_not_contact": "review"},
        ])
        result = self.run_helper(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["input_contact_rows"], 10)
        self.assertEqual(summary["retained_source_rows"], 10)
        self.assertEqual(summary["output_contact_records"], 9)
        contacts = self.read_rows("contacts.csv")
        alex = next(row for row in contacts if row["full_name"] == "Alex Morgan")
        self.assertEqual(alex["merge_count"], "2")
        self.assertEqual(alex["sms_opt_out"], "true")
        self.assertIn("relationship", alex["field_conflicts"])
        self.assertEqual(alex["relationship"], "")
        self.assertEqual(len([row for row in contacts if row["full_name"] == "Chris"]), 2)
        self.assertEqual(len([row for row in contacts if row["full_name"] == "Taylor Reed"]), 2)
        for name in ("Jamie Morgan", "Sam Morgan"):
            person = next(row for row in contacts if row["full_name"] == name)
            self.assertEqual(person["email_opt_out"], "true")
            self.assertEqual(person["call_opt_out"], "true")
        source = self.read_rows("source-rows.csv")
        self.assertEqual(json.loads(source[-1]["original_json"])["full_name"], malicious)
        self.assertTrue(any(row["full_name"] == "Zoë García" for row in contacts))
        self.assertTrue(any(row["issue"] == "unknown_suppression_flag" for row in self.read_rows("identity-review.csv")))

    def test_opt_out_reaches_merged_and_shared_endpoints(self):
        path = self.write_input("contacts.csv", [
            {"full_name": "Alex Morgan", "emails": "alex@example.test", "phones": "15550101010", "sms_opt_out": "true"},
            {"full_name": "Alex Morgan", "emails": "alex@example.test", "phones": "15550101011"},
            {"full_name": "Sam Morgan", "phones": "15550101011"},
        ])
        result = self.run_helper(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        people = self.read_rows("contacts.csv")
        self.assertEqual(len(people), 2)
        sam = next(row for row in people if row["full_name"] == "Sam Morgan")
        self.assertEqual(sam["sms_opt_out"], "true")
        self.assertEqual(sam["call_opt_out"], "")
        self.assertTrue(any(row["channel"] == "sms" and row["normalized_endpoint"] == "15550101011"
                            for row in self.read_rows("suppression-index.csv")))

    def test_no_overwrite_or_ambiguous_source_provenance(self):
        path = self.write_input("contacts.csv", [{"full_name": "Alex Morgan", "emails": "alex@example.test"}])
        self.assertEqual(self.run_helper(path).returncode, 0)
        before = (self.base / "prepared" / "contacts.csv").read_bytes()
        self.assertNotEqual(self.run_helper(path).returncode, 0)
        self.assertEqual((self.base / "prepared" / "contacts.csv").read_bytes(), before)
        repeated = self.run_helper(path, path, output="other")
        self.assertNotEqual(repeated.returncode, 0)
        self.assertFalse((self.base / "other").exists())

    def test_malformed_csv_does_not_write_outputs(self):
        path = self.base / "broken.csv"
        path.write_text("full_name,emails\nAlex Morgan,alex@example.test,extra\n", encoding="utf-8")
        self.assertNotEqual(self.run_helper(path).returncode, 0)
        self.assertFalse((self.base / "prepared").exists())


if __name__ == "__main__":
    unittest.main()
