#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-verifier-w6-r2.py

Sol 便86 P86-2 item 2 (sol/sol_reply_86_math13.md F86-1.4 B86-o2): a
SECOND, INDEPENDENTLY-WRITTEN implementation of the W-6
pushforward-compatibility predicate (裁定139 item 2's contract: does the
searcher lane's native_a and the checker lane's native_b attest the SAME
{branch_value: multiplicity} pushforward map?).

This module deliberately shares NO helper functions, NO constants, and NO
code with search/ninfty-verifier-b.py's verify_W6_single -- it re-derives
the same mathematical predicate from scratch, in a different coding style
(single flat function, no shared _read_container/_split_by_divisor_object/
_parse_ref_triple/_check_ref_inline_consistency/_extract_w6_map plumbing),
so that search/ninfty-evidence-union.py's R2 route is built from a
genuinely SEPARATE implementation instead of a second call into R1's own
code -- closing B86-o2 ("R1 と R2 は同一 verifier の二重実行").

This module does NOT import ninfty-verifier-b.py and never should --
doing so would immediately collapse R1/R2 back onto the same code, which
is exactly the defect this file exists to fix.

Same public (status, detail) contract as ninfty-verifier-b.verify_W6_single
(status in {"ABSENT","MALFORMED","PASS","FAIL"}), so
search/ninfty-evidence-union.py can adapt either verifier's output into a
RouteResult via the same shared plumbing (that shared plumbing is about
RouteResult *shape*, not about the W-6 predicate itself -- see
_route_from_verifier_result's docstring there).

json_pointer resolution follows the SAME RFC 6901 convention already
established by ninfty-verifier-a.mjs's resolveJsonPointer and
ninfty-verifier-b.py's _resolve_json_pointer (裁定150 item 1: a
json_pointer resolves WITHIN the artifact named by the ref's own
artifact_id, i.e. within the caller-supplied native artifact -- never
within the certificate itself) -- ported independently here, not
imported from either.

runtime = python (stdlib only: hashlib, json, re).
"""
from __future__ import annotations
import hashlib
import json
import re

_HEX64_RE = re.compile(r"\A[0-9a-f]{64}\Z", re.IGNORECASE)

W6_FIELD = "pushforward_compatibility_witness"
W6_SIDES = ("searcher", "checker")

IMPLEMENTATION_ID = "ninfty-verifier-w6-r2.py::verify_W6_single_r2"


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(obj):
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


def _is_64hex(x):
    return isinstance(x, str) and bool(_HEX64_RE.match(x))


class W6R2Error(Exception):
    """Internal parse/shape failure for this independent implementation --
    always caught by verify_W6_single_r2, never escapes to the caller."""


def _pointer_lookup(doc, pointer):
    """RFC 6901 walk, written independently of ninfty-verifier-b.py's own
    _resolve_json_pointer (and of ninfty-verifier-a.mjs's
    resolveJsonPointer) -- same algorithm, separately-typed code. Returns
    (found: bool, value)."""
    if pointer == "":
        return True, doc
    if not isinstance(pointer, str) or pointer[:1] != "/":
        return False, None
    node = doc
    for step in pointer.split("/")[1:]:
        step = step.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or step not in node:
            return False, None
        node = node[step]
    return True, node


def _side_entries(raw_list, side):
    return [e for e in raw_list if isinstance(e, dict) and e.get("native_side") == side]


def _load_ref_value(ref, native_doc, what):
    """
    Independent ref-triple reader: {artifact_id, digest, json_pointer |
    object_id [, inline]}. Native artifact (`native_doc`) is authoritative
    when its json_pointer resolves -- `inline` is only a fallback CACHE,
    consulted ONLY when `json_pointer` was never supplied at all (mirrors
    ninfty-verifier-b.py's _dereference_native_ref priority, independently
    coded here). Returns (value, ok, why_not_ok_or_None). Raises
    W6R2Error on an actual digest disagreement OR an unresolved
    json_pointer (never a silent PASS).

    Sol 便87 P87-1 item 1 (F87-1.2): the prior version fell back to
    `inline` whenever `json_pointer` was present but did not resolve --
    an attacker-forged, self-digest-consistent inline map with NO
    counterpart in `native_doc` at all would be accepted as if it were
    the receiver-held native content (UNRESOLVED_POINTER_INLINE_ATTACK,
    sol/sol_reply_87_math14.md F87-1.2: R1, R2, and overall all reached
    PASS on Sol's `json_pointer="/definitely_missing"` probe). FIX: a
    json_pointer that is present but unresolvable is now UNCONDITIONALLY
    a MALFORMED-raising error here (via W6R2Error) -- inline is never
    consulted in that case, regardless of whether it is itself digest-
    consistent. inline fallback survives ONLY for the case where
    `json_pointer` was never supplied in the first place (裁定150 items
    2/3's legacy/offline semantics, unaffected).
    """
    if not isinstance(ref, dict):
        raise W6R2Error(f"{what}: ref is not an object, got {type(ref).__name__}")
    for k in ("artifact_id", "digest"):
        if k not in ref:
            raise W6R2Error(f"{what}: ref missing required key {k!r}")
    if "json_pointer" not in ref and "object_id" not in ref:
        raise W6R2Error(f"{what}: ref missing json_pointer/object_id")

    pointer = ref.get("json_pointer")
    if isinstance(pointer, str):
        found, val = _pointer_lookup(native_doc, pointer)
        if not found:
            raise W6R2Error(
                f"{what}: json_pointer {pointer!r} did not resolve within the pinned native artifact "
                f"(artifact_id={ref.get('artifact_id')!r}); inline is never consulted as a fallback "
                "authority for an unresolved pointer (Sol 便87 P87-1 item 1 fix, closing "
                "UNRESOLVED_POINTER_INLINE_ATTACK)"
            )
        got = _digest(val)
        declared = ref.get("digest")
        if got != declared:
            raise W6R2Error(
                f"{what}: native artifact dereference at json_pointer={pointer!r} digest "
                f"{got} != declared digest {declared!r} (independent R2 native-binding check)"
            )
        return val, True, None

    # json_pointer absent entirely -- legacy/offline inline-only path.
    if "inline" in ref:
        got = _digest(ref["inline"])
        declared = ref.get("digest")
        if got != declared:
            raise W6R2Error(f"{what}: inline digest {got} != declared digest {declared!r}")
        return ref["inline"], True, None

    reason = (f"{what}: no json_pointer and no inline content -- object_id-only external artifact stores "
              "are out of scope for this independent verifier (UNKNOWN, not a silent PASS)")
    return None, False, reason


def _map_from_entries(entries, what):
    """entries = list of {branch_value, multiplicity} -> total
    {branch_value: summed_multiplicity} map."""
    if not isinstance(entries, list):
        raise W6R2Error(f"{what}: map container is not a list, got {type(entries).__name__}")
    total = {}
    for i, item in enumerate(entries):
        if not isinstance(item, dict) or "branch_value" not in item or "multiplicity" not in item:
            raise W6R2Error(f"{what}[{i}]: entry missing branch_value/multiplicity")
        mult = item["multiplicity"]
        if isinstance(mult, bool) or not isinstance(mult, int):
            raise W6R2Error(f"{what}[{i}]: multiplicity is not an int, got {mult!r}")
        bv = item["branch_value"]
        total[bv] = total.get(bv, 0) + mult
    return total


def verify_W6_single_r2(cert, native_a, native_b):
    """
    Independent second implementation of the W-6 pushforward-compatibility
    predicate. Returns (status, detail), status in
    {"ABSENT","MALFORMED","PASS","FAIL"} -- same contract as
    ninfty-verifier-b.verify_W6_single, computed by DIFFERENT code that
    imports nothing from that module.
    """
    if not isinstance(cert, dict):
        return "MALFORMED", {"reason": f"certificate is not an object: {type(cert).__name__}"}
    if W6_FIELD not in cert:
        return "ABSENT", {"reason": f"{W6_FIELD} not supplied"}
    raw_list = cert[W6_FIELD]
    if raw_list is None:
        return "MALFORMED", {"reason": f"{W6_FIELD} is explicit null"}
    if not isinstance(raw_list, list):
        return "MALFORMED", {"reason": f"{W6_FIELD} must be an array, got {type(raw_list).__name__}"}
    if len(raw_list) == 0:
        return "ABSENT", {"reason": f"{W6_FIELD} is an empty array"}

    for e in raw_list:
        if not isinstance(e, dict) or e.get("native_side") not in W6_SIDES:
            return "MALFORMED", {"reason": "entry missing/unrecognized native_side tag "
                                            f"(expected one of {W6_SIDES})"}

    native_by_side = {"searcher": native_a, "checker": native_b}
    side_maps = {}
    side_unknown = {}
    for side in W6_SIDES:
        entries = _side_entries(raw_list, side)
        if len(entries) == 0:
            return "ABSENT", {"reason": f"no entry for native_side={side!r}"}
        if len(entries) > 1:
            return "MALFORMED", {"reason": f"{len(entries)} entries for native_side={side!r}, expected exactly 1"}
        entry = entries[0]
        if "map_ref" not in entry:
            return "MALFORMED", {"reason": f"{side}.map_ref missing"}
        try:
            val, ok, why = _load_ref_value(entry["map_ref"], native_by_side[side], f"{side}.map_ref")
        except W6R2Error as ex:
            return "MALFORMED", {"reason": str(ex)}
        if not ok:
            side_unknown[side] = why
            continue
        try:
            side_maps[side] = _map_from_entries(val, f"{side}.map_ref")
        except W6R2Error as ex:
            return "MALFORMED", {"reason": str(ex)}

    if side_unknown:
        return "ABSENT", {"reason": "one or both lanes have no dereferenceable map content",
                          "unresolved": side_unknown}

    ok = side_maps["searcher"] == side_maps["checker"]
    return ("PASS" if ok else "FAIL"), {"searcher_map": side_maps["searcher"], "checker_map": side_maps["checker"]}


def main(argv):
    """Standalone CLI smoke entry (not the trust boundary -- that is
    search/ninfty-evidence-union.py's evidence_union_from_raw_w6). Reads a
    JSON object {certificate, native_a, native_b} from a file or stdin,
    prints the (status, detail) pair, exits 0 iff status == PASS."""
    import sys
    if len(argv) != 1:
        print("usage: ninfty-verifier-w6-r2.py <path-to-{certificate,native_a,native_b}.json | ->", file=sys.stderr)
        return 2
    if argv[0] == "-":
        payload = json.load(sys.stdin)
    else:
        with open(argv[0], "r", encoding="utf-8") as f:
            payload = json.load(f)
    status, detail = verify_W6_single_r2(payload.get("certificate"), payload.get("native_a"), payload.get("native_b"))
    print(_canon({"status": status, "detail": detail}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
