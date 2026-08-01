#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_w6key.py

Suite for the pointwise W-6 branch-key DRAFT (Sol 便97 §3):
  schema      docs/mb_ninfty_w6_branch_key_v1.md
  receiver R1' search/ninfty-w6-key-gate-r1p.py   (discriminant / perfect square)
  receiver R2' search/ninfty-w6-key-gate-r2p.py   (Sturm / rational root theorem)

The seven mandatory fixture families of P97-3.3 are sections 2..8. Section 9
fixes, mechanically, that NONE of this closes W-6: Sol P97-3.4 authorised the
draft and explicitly refused "token agreement counts as closure".

The two routes are exercised SEPARATELY on every fixture. A check that ran
only one of them would silently permit the shared implementation P97-3.2
item 6 forbids.

Run: python search/test_ninfty_w6key.py     (exit 0 iff all checks PASS)
"""
from __future__ import annotations

import copy
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCHEMA_DOC = os.path.join(REPO, "docs", "mb_ninfty_w6_branch_key_v1.md")

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if not ok else ""))


def _load(alias, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(alias, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R1P = _load("w6_key_gate_r1p", "ninfty-w6-key-gate-r1p.py")
R2P = _load("w6_key_gate_r2p", "ninfty-w6-key-gate-r2p.py")
ROUTES = (("R1'", R1P), ("R2'", R2P))

with open(SCHEMA_DOC, encoding="utf-8") as f:
    SCHEMA_TEXT = f.read()
with open(os.path.join(HERE, "ninfty-w6-key-gate-r1p.py"), encoding="utf-8") as f:
    R1P_SRC = f.read()
with open(os.path.join(HERE, "ninfty-w6-key-gate-r2p.py"), encoding="utf-8") as f:
    R2P_SRC = f.read()

DIGEST = R1P._definition_digest()
FRAME = {"branch_key_schema_id": R1P.BRANCH_KEY_SCHEMA_ID,
         "target_coordinate_id": R1P.TARGET_COORDINATE_ID,
         "branch_key_definition_digest": DIGEST}

W = R1P.IMAGE_WITNESS_SCHEMA_ID


def witness(datum):
    return {"schema_id": W, "datum": datum}


# ============================================================================
# §1 frame, schema binding, and the standing refusal to claim closure
# ============================================================================

check("§1 both routes recompute the schema-definition digest from their OWN copy and agree",
      DIGEST is not None and DIGEST == R2P._definition_digest() and len(DIGEST) == 64,
      (DIGEST, R2P._definition_digest()))
check("§1 neither route claims W-6 closure (W6_CLOSED is False in both -- P97-3.4 refused "
      "'token agreement = closure')",
      R1P.W6_CLOSED is False and R2P.W6_CLOSED is False)
check("§1 both routes pin the same versioned schema ids (the schema is the ONLY thing they may share)",
      R1P.BRANCH_KEY_SCHEMA_ID == R2P.BRANCH_KEY_SCHEMA_ID == "mb/ninfty-w6-branch-key/v1"
      and R1P.POINT_MAP_SCHEMA_ID == R2P.POINT_MAP_SCHEMA_ID == "mb/ninfty-w6-point-map/v1")
check("§1 the schema document registers the universe as Q / fixed target P^1_mu (pre-registration)",
      "係数体 $\\mathbf Q$、固定標的 $\\mathbf P^1_\\mu$" in SCHEMA_TEXT
      or "固定標的" in SCHEMA_TEXT)

# ============================================================================
# §2 fixture family 1 -- the genuine four points, both lanes, both routes
#
# The expected tokens are NOT typed into this suite: they are READ from the
# schema document's normative example block, so the suite calibrates against
# the fixture, never against a hand-written answer.
# ============================================================================

_EXAMPLES = dict(re.findall(r"^(\S+)\s+->\s+(aqp1\|\S+)$", SCHEMA_TEXT, re.M))
check("§2 the schema document supplies all four normative example tokens",
      sorted(_EXAMPLES) == sorted(["infinity", "0", "-16*sqrt(5)*i/125", "+16*sqrt(5)*i/125"]),
      sorted(_EXAMPLES))

# lane A prototype: derives the image from its own locus data -- rational and
# quadratic data in lowest terms.
LANE_A_DATA = {
    "infinity": {"kind": "infinity"},
    "0": {"kind": "rational", "value": "0"},
    "-16*sqrt(5)*i/125": {"kind": "quadratic_imaginary", "real_part": "0",
                          "imag_sq": "256/3125", "sign": -1},
    "+16*sqrt(5)*i/125": {"kind": "quadratic_imaginary", "real_part": "0",
                          "imag_sq": "256/3125", "sign": 1},
}
# lane B prototype: the SAME four points, reached from its own exact
# algebraic-number representation, which naturally produces the unreduced
# square (16^2*5)/125^2 and a "0/1" style rational. No canonicaliser is
# shared -- the agreement below is the schema doing the work.
LANE_B_DATA = {
    "infinity": {"kind": "infinity"},
    "0": {"kind": "rational", "value": "0/1"},
    "-16*sqrt(5)*i/125": {"kind": "quadratic_imaginary", "real_part": "0/1",
                          "imag_sq": "1280/15625", "sign": -1},
    "+16*sqrt(5)*i/125": {"kind": "quadratic_imaginary", "real_part": "0/1",
                          "imag_sq": "1280/15625", "sign": 1},
}

for _label, _expected in sorted(_EXAMPLES.items()):
    _tokens = {}
    for _rname, _route in ROUTES:
        for _lane, _data in (("A", LANE_A_DATA), ("B", LANE_B_DATA)):
            _st, _tok, _d = _route.token_from_image_witness(_data[_label])
            _tokens[(_rname, _lane)] = (_st, _tok)
    check(f"§2 point {_label}: both lanes, on both receiver routes, produce the schema's normative "
          f"token {_expected} (fixture family 1)",
          all(v == ("PASS", _expected) for v in _tokens.values()), _tokens)

check("§2 the conjugate pair is SEPARATED by the key: same minimal polynomial, different rank",
      _EXAMPLES["-16*sqrt(5)*i/125"] != _EXAMPLES["+16*sqrt(5)*i/125"]
      and _EXAMPLES["-16*sqrt(5)*i/125"].rsplit("|", 1)[0]
      == _EXAMPLES["+16*sqrt(5)*i/125"].rsplit("|", 1)[0],
      (_EXAMPLES["-16*sqrt(5)*i/125"], _EXAMPLES["+16*sqrt(5)*i/125"]))
check("§2 the orbit-level NF component does NOT separate them (the reason a weak/orbit W-6 was "
      "refused -- F97-3.1 NG-2): dropping the rank collapses the two tokens to one",
      len({t.rsplit("|", 1)[0] for t in (_EXAMPLES["-16*sqrt(5)*i/125"],
                                         _EXAMPLES["+16*sqrt(5)*i/125"])}) == 1)

# ============================================================================
# §3 fixture family 2 -- scalar multiples and denominator representations
#    normalise to the SAME token (positive control for K-2)
# ============================================================================

_variants = [
    {"kind": "quadratic_imaginary", "real_part": "0", "imag_sq": "256/3125", "sign": 1},
    {"kind": "quadratic_imaginary", "real_part": "0/1", "imag_sq": "1280/15625", "sign": 1},
    {"kind": "quadratic_imaginary", "real_part": "0", "imag_sq": "2560/31250", "sign": 1},
]
for _rname, _route in ROUTES:
    _out = {_i: _route.token_from_image_witness(v) for _i, v in enumerate(_variants)}
    check(f"§3 [{_rname}] three different rational representations of the same point normalise to one "
          "token (fixture family 2)",
          len({v[1] for v in _out.values()}) == 1 and all(v[0] == "PASS" for v in _out.values()),
          _out)
    _non_primitive = "aqp1|mu|F|512,0,6250|1"
    _st, _d = _route.validate_token(_non_primitive)
    check(f"§3 [{_rname}] a NON-primitive token is MALFORMED, not silently normalised -- the producer "
          "must emit the canonical form (K-2)",
          _st == "MALFORMED" and "primitiv" in (_d.get("reason") or "").lower()
          or _st == "MALFORMED" and "content" in (_d.get("reason") or "").lower(),
          (_st, _d.get("reason")))

# ============================================================================
# §4 fixture family 3 -- the conjugate incidence swap:
#    NF (orbit-level) agrees, pointwise W-6 FAILS
# ============================================================================

B_MINUS = _EXAMPLES["-16*sqrt(5)*i/125"]
B_PLUS = _EXAMPLES["+16*sqrt(5)*i/125"]


def _record(point_id, token, multiplicity, datum):
    return {"ramification_point_id": point_id, "branch_value": token,
            "multiplicity": multiplicity,
            "source_locus_ref": {"artifact_id": "prototype-locus", "json_pointer": "/loci/" + point_id,
                                 "digest": "0" * 64},
            "exact_image_witness": witness(datum)}


_D_MINUS = LANE_A_DATA["-16*sqrt(5)*i/125"]
_D_PLUS = LANE_A_DATA["+16*sqrt(5)*i/125"]
GOOD_MAP = [_record("r1", B_MINUS, 1, _D_MINUS), _record("r2", B_PLUS, 2, _D_PLUS)]
SWAPPED_MAP = [_record("r1", B_PLUS, 1, _D_PLUS), _record("r2", B_MINUS, 2, _D_MINUS)]
SUPPORT = ["r1", "r2"]
LANE_B_DIVISOR = {B_MINUS: 1, B_PLUS: 2}


def _orbit_forgetful(records):
    """What the NF sees: the rank is dropped, so a conjugate swap is invisible."""
    out = {}
    for rec in records:
        key = rec["branch_value"].rsplit("|", 1)[0]
        out[key] = out.get(key, 0) + rec["multiplicity"]
    return out


check("§4 the orbit-level (NF) image of the good and swapped incidences is IDENTICAL -- so no "
      "orbit-level predicate can separate them (F97-3.1 NG-2 / W96-2.3)",
      _orbit_forgetful(GOOD_MAP) == _orbit_forgetful(SWAPPED_MAP),
      (_orbit_forgetful(GOOD_MAP), _orbit_forgetful(SWAPPED_MAP)))

for _rname, _route in ROUTES:
    _st, _d = _route.aggregate_gate(GOOD_MAP, LANE_B_DIVISOR)
    check(f"§4 [{_rname}] the correct incidence AGGREGATES to lane B's independent branch divisor",
          _st == "PASS", _d)
    _st, _d = _route.aggregate_gate(SWAPPED_MAP, LANE_B_DIVISOR)
    check(f"§4 [{_rname}] the conjugate swap with multiplicities 1,2 is a pointwise W-6 FAIL -- "
          "exactly the separation the orbit key could not make (fixture family 3)",
          _st == "FAIL", _d)

# Sol's caveat (P97-3.3, verbatim): W-6 equates the pushforward divisor, not
# a labelled incidence graph. A swap between two points of EQUAL multiplicity
# leaves the divisor unchanged, and NOT separating it is CORRECT.
_EQ_GOOD = [_record("r1", B_MINUS, 2, _D_MINUS), _record("r2", B_PLUS, 2, _D_PLUS)]
_EQ_SWAP = [_record("r1", B_PLUS, 2, _D_PLUS), _record("r2", B_MINUS, 2, _D_MINUS)]
for _rname, _route in ROUTES:
    _eq_divisor = {B_MINUS: 2, B_PLUS: 2}
    check(f"§4 [{_rname}] non-firing edge: swapping two points of EQUAL multiplicity leaves the "
          "pushforward divisor unchanged, and W-6 correctly does NOT flag it (P97-3.3 caveat)",
          _route.aggregate_gate(_EQ_GOOD, _eq_divisor)[0] == "PASS"
          and _route.aggregate_gate(_EQ_SWAP, _eq_divisor)[0] == "PASS")

# ============================================================================
# §5 fixture family 4 -- one-sided rank swap, token tampering, wrong
#    coordinate-definition digest
# ============================================================================

for _rname, _route in ROUTES:
    _rank_swapped = [_record("r1", B_PLUS, 1, _D_MINUS), _record("r2", B_PLUS, 2, _D_PLUS)]
    _st, _d = _route.image_gate(_rank_swapped)
    check(f"§5 [{_rname}] a ONE-SIDED rank swap (token says rank 1, the point's own exact image datum "
          "says rank 0) is caught by IMAGE-KEY -- the token is recomputed, never trusted (W97-3.1)",
          _d["records"]["r1"]["IMAGE-KEY"] == "FAIL", _d["records"]["r1"])

    _tampered = [_record("r1", "aqp1|mu|F|256,0,3126|0", 1, _D_MINUS)]
    _st, _d = _route.image_gate(_tampered)
    check(f"§5 [{_rname}] a tampered coefficient is caught by IMAGE-KEY recomputation",
          _d["records"]["r1"]["IMAGE-KEY"] == "FAIL", _d["records"]["r1"])

    _bad_frame = dict(FRAME, branch_key_definition_digest="f" * 64)
    _st, _d = _route.key_gate(GOOD_MAP, _bad_frame)
    check(f"§5 [{_rname}] a WRONG coordinate/schema definition digest is MALFORMED -- the receiver "
          "recomputes it from its own copy (G-3)",
          _st == "MALFORMED" and _d["frame_ok"] is False, _d.get("errors"))

    _wrong_coord = dict(FRAME, target_coordinate_id="other")
    check(f"§5 [{_rname}] a frame whose target_coordinate_id disagrees with the token prefix is "
          "MALFORMED (G-4)",
          _route.key_gate(GOOD_MAP, _wrong_coord)[0] == "MALFORMED")

    _foreign_prefix = [_record("r1", "zzz|mu|F|256,0,3125|0", 1, _D_MINUS)]
    check(f"§5 [{_rname}] a token with a foreign coordinate prefix is MALFORMED",
          _route.validate_token(_foreign_prefix[0]["branch_value"])[0] == "MALFORMED")

# ============================================================================
# §6 fixture family 5 -- duplicated / omitted ramification points
# ============================================================================

for _rname, _route in ROUTES:
    _dup = GOOD_MAP + [_record("r1", B_MINUS, 1, _D_MINUS)]
    _st, _d = _route.coverage_gate(_dup, SUPPORT)
    check(f"§6 [{_rname}] a DUPLICATED ramification point is MALFORMED (covered twice, not 'covered')",
          _st == "MALFORMED" and _d["duplicated"] == ["r1"], _d)
    _st, _d = _route.coverage_gate(GOOD_MAP, SUPPORT + ["r3"])
    check(f"§6 [{_rname}] an OMITTED ramification point is MALFORMED -- an unlisted point is never "
          "'no ramification there' (fail-closed)",
          _st == "MALFORMED" and _d["missing"] == ["r3"], _d)
    _st, _d = _route.coverage_gate(GOOD_MAP, ["r1"])
    check(f"§6 [{_rname}] a point OUTSIDE the declared support is MALFORMED (the universe is "
          "pre-registered and may not be widened silently)",
          _st == "MALFORMED" and _d["not_in_declared_support"] == ["r2"], _d)
    check(f"§6 [{_rname}] positive control: the exact declared support, covered once each, is PASS",
          _route.coverage_gate(GOOD_MAP, SUPPORT)[0] == "PASS")

# ============================================================================
# §7 fixture family 6 -- float-only data, reducible polynomials, out-of-range
#    ranks, and undecidable degrees: all fail closed, never PASS
# ============================================================================

for _rname, _route in ROUTES:
    _st, _tok, _d = _route.token_from_image_witness({"kind": "float", "value": 0.256})
    check(f"§7 [{_rname}] a FLOAT-only image datum is MALFORMED -- there is no float form in v1 and no "
          "fallback to one (O-3)",
          _st == "MALFORMED" and _tok is None, (_st, _d))
    _st, _tok, _d = _route.token_from_image_witness(
        {"kind": "quadratic_imaginary", "real_part": "0", "imag_sq": "0.256", "sign": 1})
    check(f"§7 [{_rname}] a decimal string is not an exact rational and is MALFORMED",
          _st == "MALFORMED", (_st, _d))

    check(f"§7 [{_rname}] a REDUCIBLE quadratic (T^2-1) is MALFORMED -- K-2 requires irreducibility",
          _route.validate_token("aqp1|mu|F|-1,0,1|0")[0] == "MALFORMED")
    check(f"§7 [{_rname}] a quadratic with a repeated root (T^2) is MALFORMED",
          _route.validate_token("aqp1|mu|F|0,0,1|0")[0] == "MALFORMED")
    check(f"§7 [{_rname}] an OUT-OF-RANGE rank (k = d) is MALFORMED (G-2: 0 <= k < d)",
          _route.validate_token("aqp1|mu|F|256,0,3125|2")[0] == "MALFORMED")
    check(f"§7 [{_rname}] a degree-3 token is UNKNOWN, never PASS -- this route does not decide exact "
          "complex ordering there, and an undecided rank is not a satisfied one",
          _route.validate_token("aqp1|mu|F|1,1,0,1|0")[0] == "UNKNOWN",
          _route.validate_token("aqp1|mu|F|1,1,0,1|0"))
    for _bad in ("aqp1|mu|F|+256,0,3125|0", "aqp1|mu|F|256, 0,3125|0", "aqp1|mu|F|0256,0,3125|0",
                 "aqp1|mu|F|-0,1|0", "aqp1|mu|F|0,1|-0", "aqp1|mu|I|extra", "aqp1|mu|X|0,1|0"):
        check(f"§7 [{_rname}] grammar violation {_bad!r} is MALFORMED (G-1/G-2)",
              _route.validate_token(_bad)[0] == "MALFORMED", _route.validate_token(_bad))
    check(f"§7 [{_rname}] the infinity token is accepted exactly as written",
          _route.validate_token("aqp1|mu|I")[0] == "PASS")
    check(f"§7 [{_rname}] an ABSENT lane-B divisor is ABSENT, never agreement",
          _route.aggregate_gate(GOOD_MAP, {})[0] == "ABSENT")

# ============================================================================
# §8 fixture family 7 -- H-4 negatives, and the structural independence of
#    the two receiver routes
# ============================================================================

for _rname, _route in ROUTES:
    _st, _d = _route.independence_gate({"lane_a": "import ninfty-nf-laneb tokens", "lane_b": ""})
    check(f"§8 [{_rname}] H-4 negative: lane A reading lane B's output is a FAIL (H-3)",
          _st == "FAIL" and _d["findings"], _d)
    _st, _d = _route.independence_gate({"receiver_r1p": "from ninfty-w6-key-gate-r2p import *"})
    check(f"§8 [{_rname}] H-4 negative: one receiver route importing the other is a FAIL "
          "(P97-3.2 item 6)",
          _st == "FAIL", _d)
    _st, _d = _route.independence_gate({"lane_a": "srepr of the branch value"})
    check(f"§8 [{_rname}] H-4 negative: lane A mimicking sympy srepr is a FAIL (H-1)",
          _st == "FAIL", _d)
    check(f"§8 [{_rname}] positive control: clean sources are PASS",
          _route.independence_gate({"lane_a": "own ideal elimination", "lane_b": "own algebraic number",
                                    "receiver_r1p": "", "receiver_r2p": ""})[0] == "PASS")

def _load_sites(src, other_module_stem):
    """Lines that would actually PULL the other route in: an import, a
    dynamic load, or an open(). Naming the other route in a comment or in a
    forbidden-token table is not a dependency, so the check is about load
    sites, not about mentions."""
    out = []
    for line in src.splitlines():
        if other_module_stem not in line:
            continue
        if any(tok in line for tok in ("import", "spec_from_file_location", "open(", "exec(")):
            out.append(line.strip())
    return out


check("§8 structural: neither receiver route has a LOAD SITE for the other (import / dynamic load / "
      "open) -- they can name each other in a forbidden-token table, but never pull each other in",
      not _load_sites(R1P_SRC, "ninfty-w6-key-gate-r2p")
      and not _load_sites(R2P_SRC, "ninfty-w6-key-gate-r1p"),
      (_load_sites(R1P_SRC, "ninfty-w6-key-gate-r2p"), _load_sites(R2P_SRC, "ninfty-w6-key-gate-r1p")))
check("§8 structural: the two routes share no project helper module -- every import in both files is "
      "stdlib",
      sorted({ln.split()[1].split(".")[0] for ln in (R1P_SRC + "\n" + R2P_SRC).splitlines()
              if ln.startswith("import ") or (ln.startswith("from ") and " import " in ln)})
      == ["__future__", "fractions", "hashlib", "math", "os", "re"],
      sorted({ln for ln in (R1P_SRC + "\n" + R2P_SRC).splitlines()
              if ln.startswith(("import ", "from "))}))
check("§8 structural: neither route loads a module dynamically at all (no shared canonicaliser can be "
      "smuggled in at run time)",
      "importlib" not in R1P_SRC and "importlib" not in R2P_SRC and "__import__" not in R1P_SRC
      and "__import__" not in R2P_SRC)
_r1_code = "\n".join(ln for ln in R1P_SRC.splitlines() if not ln.strip().startswith("#"))
_r2_code = "\n".join(ln for ln in R2P_SRC.splitlines() if not ln.strip().startswith("#"))
check("§8 structural: the two routes decide rank and irreducibility by DIFFERENT algorithms -- R1' has "
      "no Sturm chain, R2' has no discriminant/perfect-square test (P97-3.2 item 6 is about the "
      "implementation, not about a declaration)",
      "_sturm_chain" not in _r1_code and "_perfect_square" not in _r2_code
      and "_sturm_chain" in _r2_code and "_perfect_square" in _r1_code)

# ============================================================================
# §9 W-6 REMAINS OPEN -- asserted, not merely stated
# ============================================================================

SOURCES = {"lane_a": "own ideal elimination", "lane_b": "own exact algebraic number",
           "receiver_r1p": "", "receiver_r2p": ""}
for _rname, _route in ROUTES:
    _report = _route.run_receiver_route(GOOD_MAP, FRAME, SUPPORT, LANE_B_DIVISOR, SOURCES)
    check(f"§9 [{_rname}] on a fully well-formed, correctly aggregating point map, KEY / COVERAGE / "
          "AGGREGATE / INDEPENDENCE all PASS",
          all(_report["gates"][g] == "PASS" for g in ("KEY", "COVERAGE", "AGGREGATE", "INDEPENDENCE")),
          _report["gates"])
    check(f"§9 [{_rname}] and yet the route's overall verdict is UNKNOWN, because IMAGE-MU "
          "(mu(r) = b recomputed exactly from the curve model) is not implemented in v1 -- an "
          "unimplemented gate reports UNKNOWN, it does not abstain",
          _report["overall"] == "UNKNOWN" and _report["gates"]["IMAGE"] == "UNKNOWN"
          and all(rec["IMAGE-MU"] == "UNKNOWN" for rec in _report["details"]["IMAGE"]["records"].values()),
          _report["gates"])
    check(f"§9 [{_rname}] therefore the frozen R1/R2 dictionary equality is NOT reached as the final "
          "W-6 comparison (P97-3.2 item 6 orders it after every gate PASSes)",
          _report["final_comparison_reached"] is False and _report["w6_closed"] is False)

check("§9 the schema document itself records W-6 as OPEN and the draft as unauthorised for closure",
      "W-6 は OPEN" in SCHEMA_TEXT and "認可されていない" in SCHEMA_TEXT)
check("§9 neither route can mint, publish or freeze: no write-mode file access, no registry module, no "
      "subprocess -- these are diagnostic gates, and a diagnostic construction may not become a "
      "published artifact by accident (便95 F95-2.3 terminology separation)",
      all(tok not in src for src in (R1P_SRC, R2P_SRC)
          for tok in ('"w"', "'w'", "commit_generation", "subprocess", "ninfty-native-registry")),
      "grep over both route sources")

# ============================================================================
# §10 THE REAL LANE-A PER-POINT PRODUCER  (Sol 便98 P98-6.1, 認可 GO)
#
# Sections 2..9 exercise the receiver routes against hand-built prototype
# records. This section runs the ACTUAL producer,
# search/ninfty-w6-pointmap-lanea.mjs, on the genuine fixtures and pushes its
# real output through both receiver routes.
#
# What P98-6.1 authorises, and what it does NOT: the producer change is
# authorised; W-6 closure, EP activation and the positive-control run are not
# (P98-6.2 / F98-6.3). So the checks below fix, mechanically, that the overall
# verdict is still UNKNOWN.
#
# CALIBRATION DISCIPLINE: the expected aggregate is NOT typed in here. It is
# derived from lane A's own INDEPENDENTLY computed normal form (the orbit-level
# object that both lanes already agree on): for each NF branch component,
# coefficient * degree must equal the sum of the point map's multiplicities
# over that orbit. That is a refinement check -- the pointwise map must forget
# down to the NF -- and it is NOT W-6 closure (W6-C2: the NF has no incidence).
# ============================================================================

import json
import subprocess
from fractions import Fraction

PRODUCER = os.path.join(HERE, "ninfty-w6-pointmap-lanea.mjs")
FIXTURES = os.path.join(REPO, "search", "fixtures", "ninfty")
with open(PRODUCER, encoding="utf-8") as f:
    PRODUCER_SRC = f.read()

_NODE_HELPER = r"""
import { readFileSync } from 'node:fs';
import { buildW6PointMapLaneA } from './ninfty-w6-pointmap-lanea.mjs';
import { computeNormalFormLaneA } from './ninfty-searcher-v2.mjs';
const c = JSON.parse(readFileSync(process.argv[2], 'utf8'));
process.stdout.write(JSON.stringify({
  point_map: buildW6PointMapLaneA(c),
  nf: computeNormalFormLaneA(c),
}));
"""
_HELPER_PATH = os.path.join(HERE, "_w6_pointmap_probe.tmp.mjs")


def _run_producer(fixture_stem):
    with open(_HELPER_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(_NODE_HELPER)
    try:
        out = subprocess.run(["node", _HELPER_PATH, os.path.join(FIXTURES, fixture_stem + ".json")],
                             cwd=HERE, capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
    finally:
        try:
            os.remove(_HELPER_PATH)
        except OSError:
            pass
    if out.returncode != 0:
        return None, out.stderr[-400:]
    return json.loads(out.stdout), ""


_GENUINE = ("checker_pos_01", "checker_pos_02", "checker_pos_03")

check("§10 the lane-A per-point producer exists as a separate module and never claims closure "
      "(W6_CLOSED = false, artifact_class = diagnostic_construction)",
      "export const W6_CLOSED = false;" in PRODUCER_SRC
      and "diagnostic_construction" in PRODUCER_SRC)
check("§10 H-1/H-3 structural: the producer has no load site for the other lane's producer, its "
      "normal form, its symbolic string encoding, or either receiver route",
      not _load_sites(PRODUCER_SRC, "ninfty-nf-laneb")
      and not _load_sites(PRODUCER_SRC, "ninfty-checker")
      and not _load_sites(PRODUCER_SRC, "ninfty-w6-key-gate")
      and "srepr" not in PRODUCER_SRC,
      _load_sites(PRODUCER_SRC, "ninfty-nf-laneb") + _load_sites(PRODUCER_SRC, "ninfty-w6-key-gate"))
check("§10 W6-C4: the producer ships NO self-declared aggregate/divisor field -- the receiver must "
      "re-sum the per-point multiplicities itself",
      "producer_self_aggregate" not in PRODUCER_SRC and "branch_divisor" not in PRODUCER_SRC)

for _stem in _GENUINE:
    _payload, _err = _run_producer(_stem)
    check(f"§10 [{_stem}] the producer runs and returns a point map", _payload is not None, _err)
    if _payload is None:
        continue
    _pm, _nf = _payload["point_map"], _payload["nf"]
    _recs = _pm["records"]

    check(f"§10 [{_stem}] status PRESENT with the ramification degree fully accounted for "
          "(sum of multiplicities = deg R_mu = 2g-2+2deg(mu) = 12, asserted by the producer)",
          _pm["status"] == "PRESENT" and _pm["ramification_degree_check"]["ok"] is True
          and _pm["ramification_degree_check"]["total_multiplicity"] == 12,
          (_pm["status"], _pm.get("ramification_degree_check"), _pm.get("reason")))

    _finite = [r for r in _recs if r["ramification_point_id"].startswith("aff|")]
    _infin = [r for r in _recs if not r["ramification_point_id"].startswith("aff|")]
    check(f"§10 [{_stem}] P98-6.1: the FINITE ramification points are separated one by one -- 4 "
          "records (2 x-values x 2 y-root ranks), each of multiplicity 1",
          len(_finite) == 4 and all(r["multiplicity"] == 1 for r in _finite),
          [(r["ramification_point_id"], r["multiplicity"]) for r in _finite])
    check(f"§10 [{_stem}] P98-6.1: the two ramification points at infinity and their images/"
          "coefficients REMAIN in the same point map (the 4 finite points alone may not be declared "
          "to be the whole COVERAGE)",
          len(_infin) == 2 and all(r["multiplicity"] == 4 for r in _infin)
          and {r["ramification_point_id"] for r in _infin} == {"inf_plus", "inf_minus"},
          [(r["ramification_point_id"], r["multiplicity"], r["branch_value"]) for r in _infin])

    check(f"§10 [{_stem}] P98-6.1 verbatim: `ramification_point_id` carries BOTH the value of x and "
          "the y-root rank, and is never the branch token in disguise",
          all(re.match(r"^aff\|x=-?\d+(/\d+)?\|yrank=[01]$", r["ramification_point_id"])
              for r in _finite)
          and not any(r["ramification_point_id"] == r["branch_value"] for r in _recs),
          [r["ramification_point_id"] for r in _finite])
    _by_x = {}
    for _r in _finite:
        _by_x.setdefault(_r["ramification_point_id"].split("|yrank=")[0], []).append(_r["branch_value"])
    check(f"§10 [{_stem}] over each x the two y-root ranks get DIFFERENT tokens with the SAME minimal "
          "polynomial -- the conjugate pair is separated pointwise, which the orbit key could not do",
          all(len(set(v)) == 2 and len({t.rsplit("|", 1)[0] for t in v}) == 1 for v in _by_x.values()),
          _by_x)
    check(f"§10 [{_stem}] the exact_image_witness carries the exact reduction chain P98-6.1 requires "
          "(fibre relation in y, the evaluation mu = a(x0)+p(x0)y, and the image minimal polynomial) "
          "-- no float form appears anywhere in the map",
          all(set(("fibre_relation", "map_evaluation", "image_relation", "square_relation"))
              <= set(r["exact_image_witness"]["exact_reduction"]) for r in _finite)
          and not re.search(r"\d+\.\d+", json.dumps(_pm)),
          [r["exact_image_witness"]["exact_reduction"] for r in _finite[:1]])
    check(f"§10 [{_stem}] the map is a DIAGNOSTIC CONSTRUCTION, not a published artifact, and its "
          "inline-only locus refs are marked LEGACY_UNVERIFIED_REF (W6-C5)",
          _pm["artifact_class"] == "diagnostic_construction" and _pm["registry_pinned"] is False
          and all(r["source_locus_ref"]["ref_status"] == "LEGACY_UNVERIFIED_REF" for r in _recs))
    check(f"§10 [{_stem}] P98-6.2 item 2: the point map is NOT dressed up as a v18 native payload -- "
          "it carries the point-map schema id and no frozen-era native/predicate schema id",
          _pm["point_map_schema_id"] == R1P.POINT_MAP_SCHEMA_ID
          and "native_schema_id" not in json.dumps(_pm) and "/v18" not in json.dumps(_pm))

    # --- both receiver routes, separately, on the REAL producer output ------
    for _rname, _route in ROUTES:
        _rep = _route.run_receiver_route(_recs, _pm["frame"], _pm["declared_support"], {},
                                         {"lane_a": PRODUCER_SRC, "lane_b": "",
                                          "receiver_r1p": "", "receiver_r2p": ""})
        check(f"§10 [{_stem}][{_rname}] KEY passes on the real producer's frame and tokens (the "
              "receiver recomputes the schema digest, primitivity, irreducibility and rank itself)",
              _rep["gates"]["KEY"] == "PASS", _rep["details"]["KEY"].get("errors"))
        check(f"§10 [{_stem}][{_rname}] COVERAGE passes: every declared ramification point covered "
              "exactly once, infinities included",
              _rep["gates"]["COVERAGE"] == "PASS", _rep["details"]["COVERAGE"])
        check(f"§10 [{_stem}][{_rname}] IMAGE-KEY passes on every record -- each token is recomputed "
              "from that point's own exact image datum and agrees",
              all(e["IMAGE-KEY"] == "PASS" for e in _rep["details"]["IMAGE"]["records"].values()),
              {k: v.get("IMAGE-KEY") for k, v in _rep["details"]["IMAGE"]["records"].items()})
        check(f"§10 [{_stem}][{_rname}] INDEPENDENCE passes on the shipped producer source",
              _rep["gates"]["INDEPENDENCE"] == "PASS", _rep["details"]["INDEPENDENCE"])
        check(f"§10 [{_stem}][{_rname}] AGGREGATE is ABSENT, not PASS: no lane-B per-point producer "
              "is authorised yet (P98-6.1 authorised the LANE A producer only), and absence of an "
              "independent divisor is never agreement",
              _rep["gates"]["AGGREGATE"] == "ABSENT", _rep["details"]["AGGREGATE"])
        check(f"§10 [{_stem}][{_rname}] and therefore the overall verdict on the real fixture is "
              "ABSENT (no independent lane-B divisor) over a still-UNKNOWN IMAGE gate -- never PASS. "
              "W-6 stays OPEN: a green producer is not closure (P98-6.2/F98-6.3)",
              _rep["overall"] == "ABSENT" and _rep["overall"] != "PASS"
              and _rep["gates"]["IMAGE"] == "UNKNOWN"
              and _rep["w6_closed"] is False and _rep["final_comparison_reached"] is False,
              _rep["gates"])

        # receiver-side re-aggregation, calibrated against lane A's own NF
        _agg = _route.aggregate_pushforward(_recs)
        _orbit = {}
        for _tok, _m in _agg.items():
            _orbit[_tok.rsplit("|", 1)[0] if _tok != "aqp1|mu|I" else _tok] = \
                _orbit.get(_tok.rsplit("|", 1)[0] if _tok != "aqp1|mu|I" else _tok, 0) + _m
        _nf_expect = {}
        for _c in _nf["nf"]["branch"]["components"]:
            if _c.get("at_infinity"):
                _nf_expect["aqp1|mu|I"] = _c["coefficient"]
            else:
                _deg = len(_c["ideal_generator"]) - 1
                _key = "aqp1|mu|F|" + ",".join(
                    str(x) for x in R1P._primitive_integer_form(
                        [Fraction(g) for g in _c["ideal_generator"]]))
                _nf_expect[_key] = _c["coefficient"] * _deg
        check(f"§10 [{_stem}][{_rname}] the receiver's own re-aggregation of the per-point map "
              "FORGETS DOWN to lane A's independently computed normal form (coefficient x degree per "
              "branch component) -- the pointwise map refines the NF rather than contradicting it. "
              "This is a refinement check, NOT W-6 closure (W6-C2: the NF has no incidence)",
              _orbit == _nf_expect, (_orbit, _nf_expect))

        # firing edge of the pointwise predicate on REAL data: tamper one rank.
        _tampered = copy.deepcopy(_recs)
        for _r in _tampered:
            if _r["ramification_point_id"].endswith("yrank=0") and _r["branch_value"].endswith("|0"):
                _r["branch_value"] = _r["branch_value"][:-1] + "1"
                break
        check(f"§10 [{_stem}][{_rname}] firing edge on REAL data: flipping one point's declared root "
              "rank while leaving its exact image datum alone is caught by IMAGE-KEY",
              any(e["IMAGE-KEY"] == "FAIL"
                  for e in _route.image_gate(_tampered)[1]["records"].values()),
              _route.image_gate(_tampered)[1]["records"])
        check(f"§10 [{_stem}][{_rname}] non-firing edge on REAL data: the untampered map has no "
              "IMAGE-KEY FAIL anywhere (the detector is not firing on everything)",
              not any(e["IMAGE-KEY"] == "FAIL"
                      for e in _route.image_gate(_recs)[1]["records"].values()))

# fail-closed edges of the producer itself
for _stem, _expected in (("checker_neg_01", "ABSENT"), ("neg_divisor_orientation_27", "INTEGRITY_STOP")):
    _payload, _err = _run_producer(_stem)
    check(f"§10 producer fail-closed edge [{_stem}]: status {_expected} and NOT ONE ramification "
          "point is named -- a rejected / internally inconsistent candidate has no divisor to map",
          _payload is not None and _payload["point_map"]["status"] == _expected
          and _payload["point_map"]["records"] == []
          and _payload["point_map"]["declared_support"] == [],
          (_payload and _payload["point_map"]["status"], _err))

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS)} checks, {n_fail} FAIL")
raise SystemExit(1 if n_fail else 0)
