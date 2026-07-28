#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_legacy_normalizer.py

Self-made unit test suite for search/ninfty-legacy-normalizer.py (裁定152
item 2, sol/裁定_152_便78検収.md). Exercises:
  1. already-canonical entries pass through unconverted (converted=False,
     identical digests).
  2. legacy shapes (per_overlap_witnesses key, free-text/absent status)
     convert to the 追補(n) v2 canonical {status, entries} form, with
     status correctly RE-DERIVED from the witness array's own emptiness
     (never trusted from the legacy status value).
  3. genuinely self-contradictory legacy data (status=ABSENT + non-empty
     array) is refused (UnconvertibleLegacyEntry), never silently resolved.
  4. shapes with neither array key at all are refused.
  5. whole-certificate normalize_certificate_w4: only chart_overlap_witnesses
     changes; every other field is byte-identical; the original certificate
     object passed in is never mutated; digests are recorded correctly.
  6. the CLI entry point (main()) round-trips a legacy payload via stdin.

Run: python search/test_ninfty_legacy_normalizer.py
Exits 0 iff all checks PASS; prints a PASS/FAIL table and returns nonzero
on any failure.
"""
import copy
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_module(name, relpath):
    path = os.path.join(HERE, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


norm = _load_module("ninfty_legacy_normalizer", "ninfty-legacy-normalizer.py")

RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append((name, ok, detail))


# --------------------------------------------------------------------------
# 1. is_canonical_w4_entry / already-canonical passthrough
# --------------------------------------------------------------------------
canonical_absent = {"divisor_object": "ramification_divisor_on_C_ref", "status": "ABSENT", "entries": []}
canonical_present = {
    "divisor_object": "ramification_divisor_on_C_ref", "status": "PRESENT",
    "entries": [{"chart_pair": ["chart-A", "chart-B"], "component_in_chart_a": "pt-x1", "component_in_chart_b": "pt-x1"}],
}

record("is_canonical_w4_entry: canonical ABSENT entry -> True", norm.is_canonical_w4_entry(canonical_absent) is True)
record("is_canonical_w4_entry: canonical PRESENT entry -> True", norm.is_canonical_w4_entry(canonical_present) is True)
record("is_canonical_w4_entry: legacy entry (per_overlap_witnesses key) -> False",
       norm.is_canonical_w4_entry({"divisor_object": "x", "status": "agree", "per_overlap_witnesses": []}) is False)

out_entry, rec1 = norm.normalize_w4_entry(canonical_absent)
record("normalize_w4_entry: already-canonical ABSENT -> converted=False", rec1["converted"] is False, rec1)
record("normalize_w4_entry: already-canonical -> legacy_digest == canonical_digest",
       rec1["legacy_digest"] == rec1["canonical_digest"], rec1)
record("normalize_w4_entry: already-canonical -> output equals input (value-wise)",
       out_entry == canonical_absent, out_entry)
record("normalize_w4_entry: already-canonical -> output is NOT the same object (defensive copy)",
       out_entry is not canonical_absent, "same object" if out_entry is canonical_absent else "distinct object")

out_entry2, rec2 = norm.normalize_w4_entry(canonical_present)
record("normalize_w4_entry: already-canonical PRESENT -> converted=False", rec2["converted"] is False, rec2)


# --------------------------------------------------------------------------
# 2. legacy shape conversions
# --------------------------------------------------------------------------

# 2a: legacy structured-ABSENT marker (裁定145 shape: per_overlap_witnesses
# key, status='ABSENT', empty array) -> canonical ABSENT, entries renamed.
legacy_absent = {
    "divisor_object": "ramification_divisor_on_C_ref",
    "status": "ABSENT",
    "per_overlap_witnesses": [],
    "reason": "lane A native declares a single chart; no second chart exists",
}
canon, rec = norm.normalize_w4_entry(legacy_absent)
record("normalize_w4_entry: legacy ABSENT marker -> converted=True", rec["converted"] is True, rec)
record("normalize_w4_entry: legacy ABSENT marker -> canonical status=ABSENT", canon.get("status") == "ABSENT", canon)
record("normalize_w4_entry: legacy ABSENT marker -> canonical entries=[] (renamed key)",
       canon.get("entries") == [] and "per_overlap_witnesses" not in canon, canon)
record("normalize_w4_entry: legacy ABSENT marker -> extra 'reason' key preserved",
       canon.get("reason") == legacy_absent["reason"], canon)
record("normalize_w4_entry: legacy ABSENT marker -> divisor_object preserved",
       canon.get("divisor_object") == legacy_absent["divisor_object"], canon)

# 2b: legacy shape with NO status field at all, empty array (oldest,
# pre-裁定145 ambiguous shape) -> canonical ABSENT (status re-derived from
# emptiness, not from an absent field).
legacy_no_status_empty = {"divisor_object": "branch_divisor_on_P1_ref", "per_overlap_witnesses": []}
canon2, rec2b = norm.normalize_w4_entry(legacy_no_status_empty)
record("normalize_w4_entry: legacy no-status + empty array -> converted=True", rec2b["converted"] is True, rec2b)
record("normalize_w4_entry: legacy no-status + empty array -> canonical status=ABSENT",
       canon2.get("status") == "ABSENT", canon2)

# 2c: legacy free-text status ("agree") + NON-empty array (the pre-追補(n)
# producer-claim convention used by this repo's own old self-made
# fixtures) -> canonical PRESENT, status DISCARDED and re-derived, entries
# renamed, data preserved exactly.
overlap_data = [
    {"chart_pair": ["chart-A", "chart-B"], "component_in_chart_a": "pt-x1", "component_in_chart_b": "pt-x1"},
    {"chart_pair": ["chart-A", "chart-B"], "component_in_chart_a": "pt-x2", "component_in_chart_b": "pt-x2"},
]
legacy_agree = {"divisor_object": "ramification_divisor_on_C_ref", "status": "agree", "per_overlap_witnesses": overlap_data}
canon3, rec3 = norm.normalize_w4_entry(legacy_agree)
record("normalize_w4_entry: legacy status='agree' + non-empty -> converted=True", rec3["converted"] is True, rec3)
record("normalize_w4_entry: legacy status='agree' + non-empty -> canonical status=PRESENT (re-derived, not 'agree')",
       canon3.get("status") == "PRESENT", canon3)
record("normalize_w4_entry: legacy status='agree' -> entries data preserved exactly",
       canon3.get("entries") == overlap_data, canon3)

# 2d: legacy free-text status ("PASS", the ninfty-witness-gen.py pre-裁定152
# convention) + non-empty array -> same treatment as 2c.
legacy_pass_status = {"divisor_object": "branch_divisor_on_P1_ref", "status": "PASS", "per_overlap_witnesses": overlap_data}
canon4, rec4 = norm.normalize_w4_entry(legacy_pass_status)
record("normalize_w4_entry: legacy status='PASS' + non-empty -> canonical status=PRESENT",
       canon4.get("status") == "PRESENT", canon4)


# --------------------------------------------------------------------------
# 3. genuinely self-contradictory legacy data -> refused, never resolved
# --------------------------------------------------------------------------
legacy_contradiction = {
    "divisor_object": "ramification_divisor_on_C_ref",
    "status": "ABSENT",
    "per_overlap_witnesses": overlap_data,  # non-empty, contradicts status=ABSENT
}
try:
    norm.normalize_w4_entry(legacy_contradiction)
    _raised_contradiction = False
except norm.UnconvertibleLegacyEntry:
    _raised_contradiction = True
record("normalize_w4_entry: status=ABSENT + non-empty legacy array -> UnconvertibleLegacyEntry "
       "(refused, not silently resolved)",
       _raised_contradiction, "raised" if _raised_contradiction else "did NOT raise (BUG)")


# --------------------------------------------------------------------------
# 4. shapes with neither array key -> refused
# --------------------------------------------------------------------------
try:
    norm.normalize_w4_entry({"divisor_object": "x", "status": "ABSENT"})
    _raised_neither = False
except norm.UnconvertibleLegacyEntry:
    _raised_neither = True
record("normalize_w4_entry: neither legacy nor canonical array key present -> UnconvertibleLegacyEntry",
       _raised_neither, "raised" if _raised_neither else "did NOT raise (BUG)")

try:
    norm.normalize_w4_entry("not-a-dict")
    _raised_not_dict = False
except norm.UnconvertibleLegacyEntry:
    _raised_not_dict = True
record("normalize_w4_entry: entry is not a dict -> UnconvertibleLegacyEntry",
       _raised_not_dict, "raised" if _raised_not_dict else "did NOT raise (BUG)")

try:
    norm.normalize_chart_overlap_witnesses("not-a-list")
    _raised_field_not_list = False
except norm.UnconvertibleLegacyEntry:
    _raised_field_not_list = True
record("normalize_chart_overlap_witnesses: field is not a list -> UnconvertibleLegacyEntry",
       _raised_field_not_list, "raised" if _raised_field_not_list else "did NOT raise (BUG)")


# --------------------------------------------------------------------------
# 5. whole-array / whole-certificate normalization
# --------------------------------------------------------------------------
legacy_field = [legacy_absent, legacy_agree]
canonical_field, records = norm.normalize_chart_overlap_witnesses(legacy_field)
record("normalize_chart_overlap_witnesses: 2-entry legacy field -> 2 canonical entries + 2 records",
       len(canonical_field) == 2 and len(records) == 2, (canonical_field, records))
record("normalize_chart_overlap_witnesses: entry order preserved",
       canonical_field[0].get("divisor_object") == "ramification_divisor_on_C_ref"
       and canonical_field[1].get("divisor_object") == "ramification_divisor_on_C_ref",
       canonical_field)

fake_certificate = {
    "candidate_ref": "test-cert",
    "chart_ids": ["x-chart-single"],
    "chart_overlap_witnesses": copy.deepcopy(legacy_field),
    "some_other_field": {"nested": [1, 2, 3]},
}
original_snapshot = copy.deepcopy(fake_certificate)
new_cert, report = norm.normalize_certificate_w4(fake_certificate)

record("normalize_certificate_w4: original certificate object NOT mutated",
       fake_certificate == original_snapshot, fake_certificate)
record("normalize_certificate_w4: chart_overlap_witnesses converted to canonical shape",
       all(norm.is_canonical_w4_entry(e) for e in new_cert["chart_overlap_witnesses"]),
       new_cert["chart_overlap_witnesses"])
record("normalize_certificate_w4: unrelated fields byte-identical",
       new_cert["candidate_ref"] == fake_certificate["candidate_ref"]
       and new_cert["chart_ids"] == fake_certificate["chart_ids"]
       and new_cert["some_other_field"] == fake_certificate["some_other_field"],
       new_cert)
record("normalize_certificate_w4: any_conversion_performed == True (legacy data was present)",
       report["any_conversion_performed"] is True, report)
record("normalize_certificate_w4: legacy_certificate_digest == sha256(original)",
       report["legacy_certificate_digest"] == norm.sha256_of(original_snapshot), report)
record("normalize_certificate_w4: canonical_certificate_digest == sha256(new_certificate)",
       report["canonical_certificate_digest"] == norm.sha256_of(new_cert), report)
record("normalize_certificate_w4: legacy_certificate_digest != canonical_certificate_digest "
       "(a genuine conversion happened, digests must differ)",
       report["legacy_certificate_digest"] != report["canonical_certificate_digest"], report)
record("normalize_certificate_w4: w4_entry_records has one record per input entry",
       len(report["w4_entry_records"]) == 2, report["w4_entry_records"])

# already-canonical certificate -> no conversion, but digests still recorded
# (and, since nothing changed, legacy == canonical digest at the cert level too).
already_canonical_cert = {
    "candidate_ref": "already-canonical",
    "chart_overlap_witnesses": [canonical_absent, canonical_present],
}
snap2 = copy.deepcopy(already_canonical_cert)
new_cert2, report2 = norm.normalize_certificate_w4(already_canonical_cert)
record("normalize_certificate_w4: already-canonical certificate -> any_conversion_performed=False",
       report2["any_conversion_performed"] is False, report2)
record("normalize_certificate_w4: already-canonical certificate -> legacy_digest == canonical_digest",
       report2["legacy_certificate_digest"] == report2["canonical_certificate_digest"], report2)
record("normalize_certificate_w4: already-canonical certificate -> original object still not mutated",
       already_canonical_cert == snap2, already_canonical_cert)

# certificate with NO chart_overlap_witnesses field at all -> passthrough,
# no crash, any_conversion_performed=False, w4_entry_records=[].
no_w4_cert = {"candidate_ref": "no-w4-field"}
new_cert3, report3 = norm.normalize_certificate_w4(no_w4_cert)
record("normalize_certificate_w4: certificate with no chart_overlap_witnesses field -> no crash, "
       "any_conversion_performed=False",
       report3["any_conversion_performed"] is False and report3["w4_entry_records"] == [], report3)

try:
    norm.normalize_certificate_w4("not-a-dict")
    _raised_cert_not_dict = False
except norm.UnconvertibleLegacyEntry:
    _raised_cert_not_dict = True
record("normalize_certificate_w4: certificate is not a dict -> UnconvertibleLegacyEntry",
       _raised_cert_not_dict, "raised" if _raised_cert_not_dict else "did NOT raise (BUG)")


# --------------------------------------------------------------------------
# 6. CLI entry point round-trip (stdin '-')
# --------------------------------------------------------------------------
_cli_payload = {"certificate": copy.deepcopy(fake_certificate), "native_a": {"stub": True}}
_stdin_backup = sys.stdin
_stdout_backup = sys.stdout
try:
    sys.stdin = io.StringIO(json.dumps(_cli_payload))
    _captured = io.StringIO()
    sys.stdout = _captured
    _rc = norm.main(["-"])
finally:
    sys.stdin = _stdin_backup
    sys.stdout = _stdout_backup

record("CLI main(['-']): exits 0", _rc == 0, f"rc={_rc}")
_cli_out = json.loads(_captured.getvalue())
record("CLI main(['-']): output carries _legacy_normalization report",
       isinstance(_cli_out.get("_legacy_normalization"), dict), _cli_out.get("_legacy_normalization"))
record("CLI main(['-']): output certificate.chart_overlap_witnesses is canonical",
       all(norm.is_canonical_w4_entry(e) for e in _cli_out["certificate"]["chart_overlap_witnesses"]),
       _cli_out["certificate"]["chart_overlap_witnesses"])
record("CLI main(['-']): sibling fields (e.g. native_a) preserved through the wrapper",
       _cli_out.get("native_a") == {"stub": True}, _cli_out.get("native_a"))


# --------------------------------------------------------------------------
# 7. 裁定177 F80-4.2 (sol/sol_reply_80_math7.md): Sol's five adversarial
#    inputs, directly reproduced against normalize_w4_entry. Before this
#    repair, all five were WRONGLY accepted/converted; kept here as
#    NEGATIVE regression (all five must now be refused, not silently
#    resolved) -- the pre-existing 42 tests above remain as ordinary
#    regression but are NOT, on their own, adversarial coverage (Sol's own
#    framing: "42/42 は回帰として残すが、adversarial coverage の証明には
#    用いない").
# --------------------------------------------------------------------------
print()  # (no-op, keeps this section visually separated when run standalone)

# F80-4.2 adversarial 1: status=ABSENT, entries=[...] (non-empty) -- the
# prior `is_canonical_w4_entry` wrongly accepted this as "already canonical,
# converted=false" (status/entries correspondence was never checked).
try:
    norm.normalize_w4_entry({
        "divisor_object": "ramification_divisor_on_C_ref", "status": "ABSENT",
        "entries": [{"chart_pair": ["a", "b"], "component_in_chart_a": "x", "component_in_chart_b": "x"}],
    })
    _f80_1_raised = False
except norm.UnconvertibleLegacyEntry:
    _f80_1_raised = True
record("裁定177 F80-4.2 adversarial 1: status=ABSENT + entries non-empty (canonical KEYS, "
       "contradictory VALUES) -> UnconvertibleLegacyEntry (was wrongly ACCEPTed before)",
       _f80_1_raised, "raised" if _f80_1_raised else "did NOT raise (BUG)")

# F80-4.2 adversarial 2: status=PRESENT, entries=[] -- prior bug: wrongly
# accepted as "already canonical, converted=false".
try:
    norm.normalize_w4_entry({"divisor_object": "ramification_divisor_on_C_ref", "status": "PRESENT", "entries": []})
    _f80_2_raised = False
except norm.UnconvertibleLegacyEntry:
    _f80_2_raised = True
record("裁定177 F80-4.2 adversarial 2: status=PRESENT + entries=[] (canonical KEYS, "
       "contradictory VALUES) -> UnconvertibleLegacyEntry (was wrongly ACCEPTed before)",
       _f80_2_raised, "raised" if _f80_2_raised else "did NOT raise (BUG)")

# F80-4.2 adversarial 3: status MISSING, entries=[] (no legacy key at all)
# -- prior bug: silently treated as legacy and converted to ABSENT (wrong:
# this never had the retired per_overlap_witnesses key, so it is not a
# legacy shape -- refuse, per conditions 2/3).
try:
    norm.normalize_w4_entry({"divisor_object": "ramification_divisor_on_C_ref", "entries": []})
    _f80_3_raised = False
except norm.UnconvertibleLegacyEntry:
    _f80_3_raised = True
record("裁定177 F80-4.2 adversarial 3: status missing + entries=[] (new key, no legacy key) "
       "-> UnconvertibleLegacyEntry (was wrongly converted to ABSENT before -- 'legacy' "
       "requires the frozen per_overlap_witnesses key, conditions 2/3)",
       _f80_3_raised, "raised" if _f80_3_raised else "did NOT raise (BUG)")

# F80-4.2 adversarial 4: old per_overlap_witnesses AND new entries BOTH
# present (byte-identical content) -- prior bug: silently picked the
# legacy array and converted to PRESENT. Must be ambiguous-refused
# regardless of agreement.
_coexist_entries = [{"chart_pair": ["a", "b"], "component_in_chart_a": "x", "component_in_chart_b": "x"}]
try:
    norm.normalize_w4_entry({
        "divisor_object": "ramification_divisor_on_C_ref",
        "per_overlap_witnesses": _coexist_entries,
        "entries": _coexist_entries,
    })
    _f80_4_raised = False
except norm.UnconvertibleLegacyEntry:
    _f80_4_raised = True
record("裁定177 F80-4.2 adversarial 4: per_overlap_witnesses AND entries co-present "
       "(byte-identical) -> UnconvertibleLegacyEntry (was wrongly resolved by silently "
       "preferring the legacy array before -- condition 4)",
       _f80_4_raised, "raised" if _f80_4_raised else "did NOT raise (BUG)")

# co-presence with DISAGREEING content must ALSO be refused (not just the
# equal case) -- same condition 4, different data.
try:
    norm.normalize_w4_entry({
        "divisor_object": "ramification_divisor_on_C_ref",
        "per_overlap_witnesses": _coexist_entries,
        "entries": [],
    })
    _f80_4b_raised = False
except norm.UnconvertibleLegacyEntry:
    _f80_4b_raised = True
record("裁定177 F80-4.2 adversarial 4b: per_overlap_witnesses AND entries co-present "
       "(DISAGREEING) -> UnconvertibleLegacyEntry (ambiguous either way, condition 4)",
       _f80_4b_raised, "raised" if _f80_4b_raised else "did NOT raise (BUG)")

# F80-4.2 adversarial 5: legacy status=PRESENT, per_overlap_witnesses=[]
# (empty) -- prior bug: silently converted to ABSENT (discarding the
# legacy data's own self-contradiction). Must refuse instead.
try:
    norm.normalize_w4_entry({
        "divisor_object": "ramification_divisor_on_C_ref", "status": "PRESENT", "per_overlap_witnesses": [],
    })
    _f80_5_raised = False
except norm.UnconvertibleLegacyEntry:
    _f80_5_raised = True
record("裁定177 F80-4.2 adversarial 5: legacy status=PRESENT + per_overlap_witnesses=[] "
       "-> UnconvertibleLegacyEntry (was wrongly converted to ABSENT before, discarding the "
       "legacy data's own self-contradiction)",
       _f80_5_raised, "raised" if _f80_5_raised else "did NOT raise (BUG)")

# is_canonical_w4_entry itself, probed directly (matching Sol's own
# direct-probe style): must reject all the canonical-looking-but-broken
# shapes above, standalone.
record("裁定177 F80-4.2: is_canonical_w4_entry(status=ABSENT, entries=non-empty) -> False",
       norm.is_canonical_w4_entry({"status": "ABSENT", "entries": _coexist_entries}) is False)
record("裁定177 F80-4.2: is_canonical_w4_entry(status=PRESENT, entries=[]) -> False",
       norm.is_canonical_w4_entry({"status": "PRESENT", "entries": []}) is False)
record("裁定177 F80-4.2: is_canonical_w4_entry(retired key co-present alongside valid entries) -> False",
       norm.is_canonical_w4_entry({"status": "PRESENT", "entries": _coexist_entries,
                                    "per_overlap_witnesses": _coexist_entries}) is False)


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
def main():
    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    n_total = len(RESULTS)
    width = max(len(name) for name, _, _ in RESULTS)
    for name, ok, detail in RESULTS:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name.ljust(width)}  {detail}")
    print(f"\n{n_pass}/{n_total} checks passed.")
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
