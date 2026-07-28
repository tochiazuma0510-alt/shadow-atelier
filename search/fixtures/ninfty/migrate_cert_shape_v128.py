#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/fixtures/ninfty/migrate_cert_shape_v128.py

Migration tool (kept, not throwaway -- documents how the toy cert fixtures
were reshaped): reshapes cert_pos/neg_0{1,2,3}.json's seven witness fields
from this implementer's PRE-裁定128 shape (one combined object/array
covering "both objects implicitly") into the 裁定128 interim-interface
shape (docs/notes/cert_shape_interpretation_v1.md): flat arrays with a
`divisor_object` tag on every entry, using spec's own literal
`ramification_divisor_on_C_ref` / `branch_divisor_on_P1_ref` tokens as tag
values; "singular" witnesses (component_bijection,
total_coverage_and_no_extra_component_witness,
pushforward_compatibility_witness) become exactly a 2-entry array (one
entry per token, content duplicated since these toy fixtures do not
distinguish genuinely different content between the two native objects).

Idempotent: running twice on an already-migrated file leaves the *_v2
witness fields alone (detected via presence of "divisor_object" tag on
existing entries / the field already being the target shape).
"""
import copy
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PLURAL_FIELDS = [
    "exact_point_equality_witnesses",
    "distinctness_witnesses",
    "multiplicity_equalities",
    "chart_overlap_witnesses",
]
SINGULAR_FIELDS = [
    "component_bijection",
    "total_coverage_and_no_extra_component_witness",
    "pushforward_compatibility_witness",
]
TOKENS = ("ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref")

FIXTURE_FILES = [
    "cert_pos_01.json", "cert_pos_02.json", "cert_pos_03.json",
    "cert_neg_01.json", "cert_neg_02.json", "cert_neg_03.json",
]


def already_migrated_plural(value):
    return isinstance(value, list) and all(
        isinstance(e, dict) and "divisor_object" in e for e in value
    ) and len(value) > 0


def already_migrated_singular(value):
    return isinstance(value, list) and len(value) > 0 and all(
        isinstance(e, dict) and "divisor_object" in e for e in value
    )


def migrate_plural(value):
    """Old shape: flat list of entries with no divisor_object tag.
    New shape: same entries, duplicated once per token, each tagged."""
    if value is None:
        return None
    if not isinstance(value, list):
        return value  # already malformed/non-list; leave for the verifier to reject
    if already_migrated_plural(value):
        return value
    out = []
    for tok in TOKENS:
        for entry in value:
            e = copy.deepcopy(entry)
            if isinstance(e, dict):
                e["divisor_object"] = tok
            out.append(e)
    return out


def migrate_singular(value):
    """Old shape: a single object. New shape: 2-entry array, one per token,
    content duplicated (toy fixtures do not distinguish the two objects)."""
    if value is None:
        return None
    if isinstance(value, list):
        if already_migrated_singular(value):
            return value
        # unexpected: already a list but not tagged -- leave as-is, the
        # verifier will report whatever malformation this represents.
        return value
    if not isinstance(value, dict):
        return value
    out = []
    for tok in TOKENS:
        e = copy.deepcopy(value)
        e["divisor_object"] = tok
        out.append(e)
    return out


def migrate_certificate(cert):
    for f in PLURAL_FIELDS:
        if f in cert:
            cert[f] = migrate_plural(cert[f])
    for f in SINGULAR_FIELDS:
        if f in cert:
            cert[f] = migrate_singular(cert[f])
    return cert


def main():
    for fname in FIXTURE_FILES:
        path = os.path.join(HERE, fname)
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        payload["certificate"] = migrate_certificate(payload["certificate"])
        payload["_shape_note"] = (
            "Certificate witness fields follow docs/notes/"
            "cert_shape_interpretation_v1.md (裁定128 interim interface): "
            "flat arrays with a 'divisor_object' tag per entry; "
            "component_bijection / total_coverage_and_no_extra_component_witness / "
            "pushforward_compatibility_witness are 2-entry arrays (one per token). "
            "Migrated by search/fixtures/ninfty/migrate_cert_shape_v128.py."
        )
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, indent=2, ensure_ascii=True)
            f.write("\n")
        print(f"migrated {fname}")


if __name__ == "__main__":
    main()
