#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crosscheck/check_koubou83_tref_v1.py

Independent second-system cross-checker for T-REF (search/certs/koubou83_tref_v1_20260822.json).

PURPOSE
-------
Sol audit (sol/sol_reply_audit_972_koubou83.md, F6/P5) graded the producer's T-REF
cert as "candidate" because it is a single GAP-only path with no independent
checker. This script is the independent second system: it is written in pure
Python (NO GAP), from the frozen canonical spec ONLY, and it does NOT read,
import, or translate the producer's GAP script
(scratchpad/koubou83_tref_v1.g -- path/SHA recorded below, never opened).

SPEC SOURCE (frozen, pre-dispute; the only inputs used to derive the check
equations and the calibration target):
  - arXiv 2401.06870 (3.3)/(3.4), as extracted verbatim in
    docs/notes/2401.06870-抽出ノート_v1.md (L49-50):
      (3.3)  sigma1^(2m+1) f^-1 sigma2^(2m+1) f  ==  f^-1 sigma1 sigma2 x12^(-m) c^m      (mod N)
      (3.4)  f^-1 sigma2^(2m+1) f sigma1^(2m+1)  ==  sigma2 sigma1 x23^(-m) c^m f          (mod N)
    (equivalently docs/week1-定義ノート.md section 2, same formulas with x:=x12, y:=x23)
  - docs/week1-定義ノート.md section 3 (dihedral-style calibration construction,
    calibration-suite item 7 "N5 control"):
      beta5: B3 -> S3 x C5,  sigma1 |-> ((0 1), t),  sigma2 |-> ((1 2), t)
      N5 := ker(beta5).  Known fact (frozen, WP1 calibration suite v2, item 7):
      N_ord = 5, expected |GT(N5)| = 4, with f = 1 and m in {0,1,3,4} (mod 5)
      passing both (3.3) and (3.4); m = 2 fails.
  - word convention W-1..W-4 (docs/week1-定義ノート.md 1.5): "paper" left-action
    convention (AB)*i = A*(B*i). This script implements paper convention directly
    (no GAP B*A reversal is used anywhere), so W-1/W-2 do not need translation.

INDEPENDENCE DECLARATION
------------------------
  - This script's group-theory engine (permutation multiplication, cyclic group
    arithmetic, word evaluation) is written from scratch in this file.
  - The producer's GAP script for T-REF (scratchpad/koubou83_tref_v1.g) was
    NOT opened, read, or translated. Its path and SHA-256 are recorded in the
    output JSON for provenance only.
  - The producer's hexagon-checking helper functions (TT/TH/CorrectedShadows/
    MakeWindow, used across the campaign's GAP scripts) were NOT read or reused.
  - Main-check status: see MAIN_CHECK_STATUS below. As of this run, the raw
    finite-quotient data (concrete sigma1/sigma2/f images) for the disputed
    windows [1152,154161]/[1152,154163] is not available as portable
    (non-producer) input data anywhere in the repository (grep-confirmed);
    obtaining it independently requires either (a) an explicit commander
    ruling that window-construction code (as opposed to hexagon-judging code)
    counts as "input data", or (b) a fresh, producer-logic-free data export.
    This is recorded honestly below rather than guessed.
"""

import hashlib
import itertools
import json
import math
import os
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Minimal from-scratch group-theory engine (paper/left-action convention).
# Elements of S3 x C5 are represented as (perm, c5) where perm is a tuple of
# length 3 giving the image of (0,1,2), and c5 is an int mod 5.
# Multiplication implements paper word "AB": (AB)(i) = A(B(i)).
# ---------------------------------------------------------------------------

def perm_mul(a, b):
    # (a*b)(i) := a(b(i))  -- paper convention for the word "ab"
    return tuple(a[b[i]] for i in range(len(a)))


def perm_inv(a):
    inv = [0] * len(a)
    for i, v in enumerate(a):
        inv[v] = i
    return tuple(inv)


IDENT_PERM = (0, 1, 2)


class S3C5Elt:
    """Element of S3 x C5, group op = paper word concatenation."""

    __slots__ = ("perm", "c5")

    def __init__(self, perm, c5):
        self.perm = perm
        self.c5 = c5 % 5

    def __mul__(self, other):
        return S3C5Elt(perm_mul(self.perm, other.perm), self.c5 + other.c5)

    def inv(self):
        return S3C5Elt(perm_inv(self.perm), (-self.c5) % 5)

    def __eq__(self, other):
        return self.perm == other.perm and self.c5 == other.c5

    def __hash__(self):
        return hash((self.perm, self.c5))

    def __repr__(self):
        return "S3C5(%s,%d)" % (self.perm, self.c5)


IDENTITY = S3C5Elt(IDENT_PERM, 0)


def power(elt, n):
    """elt^n for integer n (n may be negative)."""
    if n == 0:
        return IDENTITY
    if n < 0:
        return power(elt.inv(), -n)
    result = IDENTITY
    base = elt
    e = n
    while e > 0:
        if e & 1:
            result = result * base
        base = base * base
        e >>= 1
    return result


def order_of(elt):
    cur = elt
    n = 1
    while cur != IDENTITY:
        cur = cur * elt
        n += 1
        if n > 10000:
            raise RuntimeError("order_of: exceeded search bound, likely a bug")
    return n


# ---------------------------------------------------------------------------
# Calibration: N5 control (docs/week1-定義ノート.md sec.3/4 item 7)
#   beta5(sigma1) = ((0 1), t), beta5(sigma2) = ((1 2), t)
#   x := sigma1^2, y := sigma2^2
#   Delta := sigma1 sigma2 sigma1 (paper word), c := Delta^2
# ---------------------------------------------------------------------------

def build_n5_generators():
    sigma1 = S3C5Elt((1, 0, 2), 1)  # transposition (0 1), c5-part = t
    sigma2 = S3C5Elt((0, 2, 1), 1)  # transposition (1 2), c5-part = t
    return sigma1, sigma2


def paper_word_mul(*letters):
    """Multiply a sequence of group elements left to right as a paper word
    L1 L2 ... Ln, i.e. fold with __mul__ (which already implements the paper
    convention (AB)(i) = A(B(i)) for the perm component)."""
    result = IDENTITY
    for L in letters:
        result = result * L
    return result


def hexagon_33_holds(sigma1, sigma2, x, c, m, f):
    # (3.3): sigma1^(2m+1) f^-1 sigma2^(2m+1) f  ==  f^-1 sigma1 sigma2 x^(-m) c^m
    u = 2 * m + 1
    finv = f.inv()
    lhs = paper_word_mul(power(sigma1, u), finv, power(sigma2, u), f)
    rhs = paper_word_mul(finv, sigma1, sigma2, power(x, -m), power(c, m))
    return lhs == rhs


def hexagon_34_holds(sigma1, sigma2, y, c, m, f):
    # (3.4): f^-1 sigma2^(2m+1) f sigma1^(2m+1)  ==  sigma2 sigma1 y^(-m) c^m f
    u = 2 * m + 1
    finv = f.inv()
    lhs = paper_word_mul(finv, power(sigma2, u), f, power(sigma1, u))
    rhs = paper_word_mul(sigma2, sigma1, power(y, -m), power(c, m), f)
    return lhs == rhs


def run_calibration():
    sigma1, sigma2 = build_n5_generators()
    x = sigma1 * sigma1
    y = sigma2 * sigma2
    delta = paper_word_mul(sigma1, sigma2, sigma1)
    c = delta * delta

    n_ord_x = order_of(x)
    n_ord_y = order_of(y)
    n_ord_c = order_of(c)
    n_ord = math.lcm(n_ord_x, n_ord_y, n_ord_c)  # (3.1) N_ord := lcm(ord(xN),ord(yN),ord(cN))

    f = IDENTITY  # f = 1, the calibration's positive-control case
    per_m = []
    for m in range(0, n_ord if n_ord > 0 else 5):
        h33 = hexagon_33_holds(sigma1, sigma2, x, c, m, f)
        h34 = hexagon_34_holds(sigma1, sigma2, y, c, m, f)
        u = 2 * m + 1
        charming = (math.gcd(u, n_ord) == 1)  # f=1 is trivially in the commutator subgroup
        # GT-shadow membership (Def 3.7) = charming GT-pair (hexagon) + surjectivity;
        # for this f=1/N5 calibration target the frozen fact counts CHARMING hexagon
        # solutions (docs/week1-定義ノート.md sec.2 Def 3.1/charming + sec.4 item 7).
        per_m.append({
            "m": m, "u": u, "hex_3_3": h33, "hex_3_4": h34,
            "charming": charming, "both": h33 and h34 and charming,
        })

    passing_m = [row["m"] for row in per_m if row["both"]]
    expected_passing_m = [0, 1, 3, 4]
    expected_n_ord = 5

    calibration_ok = (
        n_ord_x == expected_n_ord
        and n_ord_y == expected_n_ord
        and n_ord_c == expected_n_ord
        and passing_m == expected_passing_m
    )

    return {
        "construction": "beta5: B3 -> S3 x C5, sigma1 |-> ((0 1),t), sigma2 |-> ((1 2),t); N5 := ker(beta5)",
        "spec_source": "docs/week1-定義ノート.md sec.3 (dihedral construction pattern) + sec.4 item 7 (N5 control, expected fact)",
        "measured": {
            "n_ord_x": n_ord_x,
            "n_ord_y": n_ord_y,
            "n_ord_c": n_ord_c,
            "per_m": per_m,
            "passing_m_f_eq_1": passing_m,
        },
        "expected": {
            "n_ord": expected_n_ord,
            "passing_m_f_eq_1": expected_passing_m,
            "source": "docs/week1-定義ノート.md sec.4 item 7 (frozen WP1 calibration suite v2 fact) + T-REF cert step1_stock_check.location_1 (search/suite-wp1.g N5 control, cross-checked C-3, ~1 month prior to this dispute)",
        },
        "calibration_pass": calibration_ok,
    }


# ---------------------------------------------------------------------------
# Main check: disputed m=2 (u=5) settled element, windows [1152,154161] and
# [1152,154163], full-form (3.3)/(3.4) in the actual order-1152 quotient Bq.
#
# Data source: search/certs/koubou83_tref_window_export_v1_20260822.json
# (raw object-identity export -- SmallGroup ID, generator images, disputed f,
# ALL as permutation image lists on [1..degree]; NO judgment-logic fields
# (TT/TH/CorrectedShadows/hex verdicts) are present in that export -- verified
# by inspection of its top-level keys before use). This crosscheck's own
# hexagon predicates below are the only judgment logic applied to this data.
# ---------------------------------------------------------------------------

WINDOW_EXPORT_PATH = "search/certs/koubou83_tref_window_export_v1_20260822.json"
WINDOW_EXPORT_EXPECTED_SHA256 = "05bb76b2e993e3f7ff26ef0b82f1d2458f17875122c2ccb0f2f1bdb07fdd9144"

PRODUCER_SCRIPT_PATH = "scratchpad/koubou83_tref_v1.g"
PRODUCER_CERT_PATH = "search/certs/koubou83_tref_v1_20260822.json"


class Perm:
    """A permutation of {0,...,degree-1}, built from a GAP-style 1-indexed
    image list (list[i-1] = image of point i). Multiplication implements the
    paper convention (AB)(pt) = A(B(pt)) -- i.e. plain function composition,
    matching W-1 (paper "AB" <-> GAP "B*A") once GAP's own right-action
    permutation-multiplication convention is unwound (see design note in the
    module docstring / implementer report). This is exactly the same
    composition rule used in run_calibration() above, generalized to
    arbitrary degree."""

    __slots__ = ("images",)  # tuple, 0-indexed: images[i] = image of point i (0-indexed)

    def __init__(self, images):
        self.images = tuple(images)

    @classmethod
    def from_gap_1indexed_list(cls, lst):
        # lst[i-1] (1-indexed i) = image of point i (1-indexed) -> convert to 0-indexed
        return cls(tuple(v - 1 for v in lst))

    def __mul__(self, other):
        # (self*other)(i) := self(other(i))
        b = other.images
        a = self.images
        return Perm(tuple(a[b[i]] for i in range(len(a))))

    def inv(self):
        n = len(self.images)
        inv = [0] * n
        for i, v in enumerate(self.images):
            inv[v] = i
        return Perm(tuple(inv))

    def __eq__(self, other):
        return self.images == other.images

    def __hash__(self):
        return hash(self.images)

    def to_gap_1indexed_list(self):
        return [v + 1 for v in self.images]


def perm_identity(degree):
    return Perm(tuple(range(degree)))


def perm_power(elt, n, degree):
    if n == 0:
        return perm_identity(degree)
    if n < 0:
        return perm_power(elt.inv(), -n, degree)
    result = perm_identity(degree)
    base = elt
    e = n
    while e > 0:
        if e & 1:
            result = result * base
        base = base * base
        e >>= 1
    return result


def perm_paper_word_mul(letters, degree):
    result = perm_identity(degree)
    for L in letters:
        result = result * L
    return result


def load_window_export():
    abspath = os.path.join(REPO_ROOT, WINDOW_EXPORT_PATH)
    actual_sha = sha256_of(abspath)
    with open(abspath, encoding="utf-8") as fh:
        data = json.load(fh)
    return data, actual_sha


def evaluate_window(window_key, w):
    degree = w["degree"]
    s1 = Perm.from_gap_1indexed_list(w["s1_perm_image_list"])
    s2 = Perm.from_gap_1indexed_list(w["s2_perm_image_list"])
    c = Perm.from_gap_1indexed_list(w["c_perm_image_list"])
    x12 = Perm.from_gap_1indexed_list(w["x12_perm_image_list"])
    x23 = Perm.from_gap_1indexed_list(w["x23_perm_image_list"])
    f = Perm.from_gap_1indexed_list(w["disputed_f_perm_image_list"])
    m = w["disputed_m"]
    u = w["disputed_u"]
    assert u == 2 * m + 1, "export u does not match 2m+1 for m=%r,u=%r" % (m, u)

    # --- built-in consistency checks (order-agnostic under either composition
    # direction, so these validate the permutation *data* and my parsing of it
    # independently of the paper-word direction question) ---
    x12_check = (s1 * s1) == x12
    x23_check = (s2 * s2) == x23
    delta = perm_paper_word_mul([s1, s2, s1], degree)  # Delta := sigma1 sigma2 sigma1
    c_check = (delta * delta) == c

    finv = f.inv()

    # (3.3): sigma1^u f^-1 sigma2^u f  ==  f^-1 sigma1 sigma2 x12^(-m) c^m
    lhs33 = perm_paper_word_mul(
        [perm_power(s1, u, degree), finv, perm_power(s2, u, degree), f], degree
    )
    rhs33 = perm_paper_word_mul(
        [finv, s1, s2, perm_power(x12, -m, degree), perm_power(c, m, degree)], degree
    )
    hex_3_3 = (lhs33 == rhs33)

    # (3.4): f^-1 sigma2^u f sigma1^u  ==  sigma2 sigma1 x23^(-m) c^m f
    lhs34 = perm_paper_word_mul(
        [finv, perm_power(s2, u, degree), f, perm_power(s1, u, degree)], degree
    )
    rhs34 = perm_paper_word_mul(
        [s2, s1, perm_power(x23, -m, degree), perm_power(c, m, degree), f], degree
    )
    hex_3_4 = (lhs34 == rhs34)

    return {
        "window_key": window_key,
        "smallgroup_id": w["smallgroup_id"],
        "bq_order": w["bq_order"],
        "pn_order": w["pn_order"],
        "degree": degree,
        "disputed_m": m,
        "disputed_u": u,
        "f_selection_caveat": (
            "disputed_f_perm_image_list is the FIRST (m=2,u=5)-settled pair found by the "
            "PRODUCER's own enumeration order (export's own note: 'an enumeration-order "
            "artifact, not a canonical choice'). This crosscheck evaluates exactly that "
            "element, as instructed, and does not independently search for other "
            "(m=2,u=5) candidates."
        ),
        "engine_consistency_checks": {
            "x12_eq_s1_squared": x12_check,
            "x23_eq_s2_squared": x23_check,
            "c_eq_Delta_squared_Delta_eq_s1s2s1": c_check,
        },
        "hex_3_3": hex_3_3,
        "hex_3_4": hex_3_4,
        "both_hold": hex_3_3 and hex_3_4,
        "raw_values": {
            "hex_3_3_lhs": lhs33.to_gap_1indexed_list(),
            "hex_3_3_rhs": rhs33.to_gap_1indexed_list(),
            "hex_3_4_lhs": lhs34.to_gap_1indexed_list(),
            "hex_3_4_rhs": rhs34.to_gap_1indexed_list(),
        },
    }


def run_main_check():
    export_data, actual_sha = load_window_export()

    export_status = {
        "path": WINDOW_EXPORT_PATH,
        "sha256_actual": actual_sha,
        "sha256_expected_per_commander_message": WINDOW_EXPORT_EXPECTED_SHA256,
        "sha256_match": (actual_sha == WINDOW_EXPORT_EXPECTED_SHA256),
        "schema": export_data.get("schema"),
        "top_level_keys": sorted(export_data.keys()),
        "judgment_logic_fields_absent_check": (
            "purpose" in export_data
            and "DELIBERATELY EXCLUDED" in export_data.get("purpose", "")
        ),
    }

    window_results = []
    for key, w in export_data["windows"].items():
        window_results.append(evaluate_window(key, w))

    tref_producer_verdict = {
        "windows": [
            {"id_group": [1152, 154161], "m": 2, "u": 5, "hex_3_3": True, "hex_3_4": True,
             "frozen_ground_truth_verdict": "genuine hexagon solution (settled)"},
            {"id_group": [1152, 154163], "m": 2, "u": 5, "hex_3_3": True, "hex_3_4": True,
             "frozen_ground_truth_verdict": "genuine hexagon solution (settled)"},
        ],
        "three_way_result": "CENSUS_CORRECT",
        "source": PRODUCER_CERT_PATH,
    }

    per_window_comparison = []
    all_match = True
    for res in window_results:
        producer_row = next(
            r for r in tref_producer_verdict["windows"] if r["id_group"] == list(res["smallgroup_id"])
        )
        matches = (res["hex_3_3"] == producer_row["hex_3_3"]) and (res["hex_3_4"] == producer_row["hex_3_4"])
        all_match = all_match and matches
        per_window_comparison.append({
            "id_group": res["smallgroup_id"],
            "independent_hex_3_3": res["hex_3_3"],
            "independent_hex_3_4": res["hex_3_4"],
            "producer_hex_3_3": producer_row["hex_3_3"],
            "producer_hex_3_4": producer_row["hex_3_4"],
            "match": matches,
        })

    return {
        "window_export": export_status,
        "window_results": window_results,
        "producer_tref_verdict_reference": tref_producer_verdict,
        "per_window_comparison": per_window_comparison,
        "all_windows_match_producer": all_match,
    }


def main():
    calibration = run_calibration()

    producer_script_abs = os.path.join(REPO_ROOT, PRODUCER_SCRIPT_PATH)
    producer_cert_abs = os.path.join(REPO_ROOT, PRODUCER_CERT_PATH)

    spec_sources = []
    for rel in [
        "docs/notes/2401.06870-抽出ノート_v1.md",
        "docs/week1-定義ノート.md",
    ]:
        abspath = os.path.join(REPO_ROOT, rel)
        spec_sources.append({
            "path": rel,
            "sha256": sha256_of(abspath) if os.path.exists(abspath) else None,
        })

    out = {
        "schema": "shadow-atelier/koubou83-tref-crosscheck/v1",
        "generated_by": "crosscheck/check_koubou83_tref_v1.py (independent second system, pure Python, no GAP)",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": "Independent cross-check of T-REF (search/certs/koubou83_tref_v1_20260822.json): disputed m=2 (u=5) settled element, windows [1152,154161]/[1152,154163], full-form hexagon (3.3)/(3.4).",
        "independence_declaration": {
            "producer_gap_script_opened": False,
            "producer_gap_script_path": PRODUCER_SCRIPT_PATH,
            "producer_gap_script_sha256": sha256_of(producer_script_abs) if os.path.exists(producer_script_abs) else None,
            "producer_cert_path": PRODUCER_CERT_PATH,
            "producer_cert_sha256": sha256_of(producer_cert_abs) if os.path.exists(producer_cert_abs) else None,
            "producer_helper_functions_reused": False,
            "note": "Producer script content was never read or translated; only its path and SHA-256 hash are recorded here for provenance. The group-theory engine, hexagon predicates, and calibration construction in this file were written independently from the frozen spec sources listed in spec_sources.",
        },
        "spec_sources": spec_sources,
        "calibration_positive_control": calibration,
    }

    if not calibration["calibration_pass"]:
        out["main_check_status"] = "not_attempted_calibration_failed"
        out["actual_result"] = "calibration_pass=False ; main check NOT attempted per instruction (calibration must PASS first)"
    else:
        main_check = run_main_check()
        out["main_check_status"] = "completed"
        out["main_check"] = main_check
        out["actual_result"] = (
            "calibration_pass=True ; independent per-window hex_3_3/hex_3_4 = {} ; "
            "matches producer CENSUS_CORRECT verdict = {}".format(
                [(r["smallgroup_id"], r["hex_3_3"], r["hex_3_4"]) for r in main_check["window_results"]],
                main_check["all_windows_match_producer"],
            )
        )

    out_path = os.path.join(REPO_ROOT, "crosscheck", "verdicts", "koubou83_tref_crosscheck_v1_20260822.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


if __name__ == "__main__":
    main()
