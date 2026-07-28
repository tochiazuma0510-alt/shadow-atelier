#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-legacy-normalizer.py

Versioned legacy-shape -> canonical-shape (追補(n) v2, 裁定152 item 2,
sol/裁定_152_便78検収.md) normalizer for W-4 (chart_overlap_witnesses)
entries.

Role / independence discipline (mirrors this codebase's search-vs-
crosscheck separation, adapted for a rescue tool rather than a verifier):
this module lives OUTSIDE the frozen certificate. It reads an OLD-shape
certificate/entry and produces a NEW canonical blob as a SEPARATE
artifact, alongside a record of (a) whether a conversion actually
happened, (b) the legacy blob's own digest, (c) the canonical blob's
digest. It NEVER mutates a certificate in place (normalize_certificate_w4
deep-copies) and NEVER writes any file itself (the CLI only prints to
stdout). It NEVER makes either verifier more permissive: it does not
change what ninfty-verifier-b.py's _validate_w4_entry accepts.
ninfty-verifier-b.py continues to REJECT (MALFORMED) any certificate that
still carries the legacy shape -- a certificate must be normalized here
FIRST, as an explicit, separately recorded step, before being fed to
either verifier. This is deliberate: rescuing old fixtures must never
become a backdoor that quietly widens the verifier's own accepted schema.

Recognized legacy shapes for a single chart_overlap_witnesses entry
(a divisor_object-tagged dict):
  - {divisor_object, status: <any free-text, e.g. "agree"/"disagree"/
     "PASS">, per_overlap_witnesses: [...]}  (裁定133(i)/裁定139 item 7
    shape, and 追補(n) v1's tolerated bare-[]-with-no-status variant).
  - `status` key missing entirely, `per_overlap_witnesses` present
    (empty or not) -- the oldest, pre-裁定145 ambiguous shape.

Canonical shape produced (追補(n) v2, docs/notes/
cert_shape_interpretation_v3_addendum_n.md v2):
  {divisor_object, status: "ABSENT"|"PRESENT", entries: [...]}
  `status` is DERIVED from entries' OWN emptiness (never trusted from the
  legacy status value -- every prior repair note in this codebase already
  documented the old status field as an untrusted producer claim) UNLESS
  the legacy blob already asserts a genuine contradiction (status=="ABSENT"
  with a non-empty per_overlap_witnesses array) -- that case is NOT
  silently resolved; normalize_w4_entry raises UnconvertibleLegacyEntry
  instead (normalizing must never invent data or paper over a schema
  violation that pre-dates this tool -- the normalizer must not be MORE
  permissive than the verifier it feeds).

runtime = python (stdlib only: copy, hashlib, json, sys).
"""
from __future__ import annotations
import copy
import hashlib
import json
import sys

LEGACY_ARRAY_KEY = "per_overlap_witnesses"
CANONICAL_ARRAY_KEY = "entries"
CANONICAL_STATUSES = ("ABSENT", "PRESENT")


def canonical_serialize(obj):
    """Project-wide canonical form: UTF-8, sorted keys, no whitespace --
    same convention as ninfty-verifier-b.py / ninfty-cert-validator.py."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


class UnconvertibleLegacyEntry(Exception):
    """Raised when a legacy W-4 entry (or certificate) cannot be safely
    normalized without inventing data (e.g. a genuine ABSENT/non-empty-
    array contradiction, or a shape with neither the legacy nor the
    canonical array key at all) -- never silently resolved, never
    swallowed by the CLI either (it propagates to a nonzero exit)."""


def is_canonical_w4_entry(entry):
    """True iff entry ALREADY satisfies 追補(n) v2's strict {status,
    entries} shape (status in {ABSENT, PRESENT}, entries a list, no
    inspection of the legacy key needed)."""
    return (
        isinstance(entry, dict)
        and entry.get("status") in CANONICAL_STATUSES
        and isinstance(entry.get("entries"), list)
    )


def _build_canonical(entry, raw_entries):
    """Builds the canonical {divisor_object?, status, entries, ...extra}
    dict from a legacy entry's other fields + the resolved entries array.
    status is ALWAYS re-derived from entries' own emptiness -- the legacy
    status value (if any) is discarded, never trusted (matches this
    codebase's long-standing "producer claim, never authoritative"
    discipline for this field)."""
    canonical_status = "ABSENT" if len(raw_entries) == 0 else "PRESENT"
    leftover = {k: v for k, v in entry.items() if k not in (LEGACY_ARRAY_KEY, "status", CANONICAL_ARRAY_KEY)}
    ordered = {}
    if "divisor_object" in leftover:
        ordered["divisor_object"] = leftover.pop("divisor_object")
    ordered["status"] = canonical_status
    ordered["entries"] = raw_entries
    ordered.update(leftover)  # any remaining extra keys (e.g. `reason`), in original order
    return ordered


def normalize_w4_entry(entry):
    """
    Converts ONE legacy-shape chart_overlap_witnesses entry (a dict) into
    the 追補(n) v2 canonical shape. Returns (canonical_entry, record) where
    record = {converted: bool, legacy_digest, canonical_digest, note}.
    Raises UnconvertibleLegacyEntry if the legacy data is genuinely
    self-contradictory, or carries neither a legacy nor a canonical array
    at all -- never silently resolved.
    """
    if not isinstance(entry, dict):
        raise UnconvertibleLegacyEntry(f"W-4 entry is not an object: {entry!r}")

    legacy_digest = sha256_of(entry)

    if is_canonical_w4_entry(entry):
        # Already canonical -- pass through unchanged (still a fresh dict,
        # never the same object reference, so callers can't accidentally
        # alias into caller-owned data), but still report identical
        # digests so callers have a uniform record shape regardless of
        # whether a conversion actually happened.
        return dict(entry), {
            "converted": False,
            "legacy_digest": legacy_digest,
            "canonical_digest": legacy_digest,
            "note": "already canonical (追補(n) v2 shape {status, entries}); no conversion performed",
        }

    has_legacy_array = isinstance(entry.get(LEGACY_ARRAY_KEY), list)
    has_entries_array = isinstance(entry.get(CANONICAL_ARRAY_KEY), list)
    legacy_status = entry.get("status")

    if not has_legacy_array and not has_entries_array:
        raise UnconvertibleLegacyEntry(
            f"W-4 entry has neither a well-typed legacy {LEGACY_ARRAY_KEY!r} array nor a "
            f"well-typed canonical {CANONICAL_ARRAY_KEY!r} array -- nothing to normalize: {entry!r}"
        )

    # Prefer the legacy array when BOTH are present (an unusual, presumably
    # hand-edited intermediate state) -- documented, not silently guessed.
    raw_entries = entry[LEGACY_ARRAY_KEY] if has_legacy_array else entry[CANONICAL_ARRAY_KEY]

    if legacy_status == "ABSENT" and len(raw_entries) != 0:
        # Genuine contradiction pre-dating this tool (matches
        # ninfty-verifier-b.py's own rule-3 fail-closed discipline: the
        # normalizer must not be MORE permissive than the verifier it
        # feeds) -- refuse to invent a resolution.
        raise UnconvertibleLegacyEntry(
            f"legacy W-4 entry declares status='ABSENT' but its witness array has "
            f"{len(raw_entries)} entries -- self-contradictory legacy data, refusing to "
            "silently resolve (never invent evidence, never discard the contradiction)"
        )

    canonical = _build_canonical(entry, raw_entries)
    canonical_digest = sha256_of(canonical)
    key_used = LEGACY_ARRAY_KEY if has_legacy_array else CANONICAL_ARRAY_KEY
    return canonical, {
        "converted": True,
        "legacy_digest": legacy_digest,
        "canonical_digest": canonical_digest,
        "note": (
            f"legacy shape ({key_used!r} key"
            + (f", status={legacy_status!r}" if legacy_status is not None else ", no status field")
            + ") converted to 追補(n) v2 canonical form {status, entries}; status "
              "RE-DERIVED from the witness array's own emptiness (the legacy status "
              "value, if any, was always documented as an untrusted producer claim, "
              "never authoritative, and is discarded here)"
        ),
    }


def normalize_chart_overlap_witnesses(field):
    """
    Normalizes an ENTIRE chart_overlap_witnesses array (list of
    divisor_object-tagged entries). Returns (canonical_field, records)
    where records is a list of per-entry conversion records (see
    normalize_w4_entry), in the same order as the input array. Raises
    UnconvertibleLegacyEntry (propagated, not swallowed) if ANY entry
    cannot be safely normalized -- fail-closed, no partial silent
    conversion of only some entries.
    """
    if not isinstance(field, list):
        raise UnconvertibleLegacyEntry(f"chart_overlap_witnesses is not an array: {field!r}")
    canonical_entries = []
    records = []
    for entry in field:
        canonical_entry, record = normalize_w4_entry(entry)
        canonical_entries.append(canonical_entry)
        records.append(record)
    return canonical_entries, records


def normalize_certificate_w4(certificate):
    """
    Top-level entry point (裁定152 item 2): given a FULL certificate dict,
    returns (new_certificate, conversion_report) where new_certificate is a
    DEEP COPY with ONLY chart_overlap_witnesses replaced by its canonical
    form (every other field passed through byte-identical) -- the ORIGINAL
    `certificate` argument object is never mutated. conversion_report
    records:
      - legacy_certificate_digest: sha256 of the certificate AS SUPPLIED
      - canonical_certificate_digest: sha256 of the certificate AFTER
        normalization
      - w4_entry_records: per-entry conversion records (see
        normalize_w4_entry)
      - any_conversion_performed: bool
    This function does NOT rewrite any file; the caller decides what (if
    anything) to persist, and where -- consistent with 裁定152 item 2's
    "凍結済み certificate 本体は書き換えない" (the frozen certificate body
    itself is never rewritten in place).
    """
    if not isinstance(certificate, dict):
        raise UnconvertibleLegacyEntry(f"certificate is not an object: {certificate!r}")

    legacy_certificate_digest = sha256_of(certificate)
    new_certificate = copy.deepcopy(certificate)

    w4_records = []
    any_conversion = False
    if "chart_overlap_witnesses" in new_certificate:
        canonical_field, records = normalize_chart_overlap_witnesses(new_certificate["chart_overlap_witnesses"])
        new_certificate["chart_overlap_witnesses"] = canonical_field
        w4_records = records
        any_conversion = any(r["converted"] for r in records)

    canonical_certificate_digest = sha256_of(new_certificate)

    return new_certificate, {
        "legacy_certificate_digest": legacy_certificate_digest,
        "canonical_certificate_digest": canonical_certificate_digest,
        "w4_entry_records": w4_records,
        "any_conversion_performed": any_conversion,
    }


def main(argv):
    """CLI: reads a payload JSON ({"certificate": {...}, ...} or a bare
    certificate) from a file path or stdin ('-'), normalizes
    chart_overlap_witnesses, and prints
    {..., "certificate": <normalized>, "_legacy_normalization": <report>}
    to stdout (canonical form, one line). Never writes any file in place --
    the caller redirects stdout if a new artifact should be persisted, kept
    deliberately separate from the frozen input file."""
    if len(argv) < 1:
        print("usage: ninfty-legacy-normalizer.py <payload.json|-->", file=sys.stderr)
        return 2
    src = argv[0]
    if src == "-":
        payload = json.load(sys.stdin)
    else:
        with open(src, "r", encoding="utf-8") as f:
            payload = json.load(f)

    if isinstance(payload, dict) and isinstance(payload.get("certificate"), dict):
        cert = payload["certificate"]
        wrapper = dict(payload)
    else:
        cert = payload
        wrapper = {"certificate": payload}

    new_cert, report = normalize_certificate_w4(cert)
    wrapper["certificate"] = new_cert
    wrapper["_legacy_normalization"] = report
    print(canonical_serialize(wrapper))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
