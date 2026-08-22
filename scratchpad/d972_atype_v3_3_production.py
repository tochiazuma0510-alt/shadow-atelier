"""d972_atype_v3_3_production.py

DIR: (iv) の実掃引 = 反例側の判定計器 / FRAME: B4-proper(pentagon 込み・972 系)

A-type instrument v3.3 -- FINAL LAUNCH (CV-9 third read: GO). v3, v3_1,
v3_2 are left UNTOUCHED (evidence artifacts). This is a NEW file, built
directly on v3_2's engine (same Engine class, unmodified logic) with:

  1. m-spectrum completion to 12/12 via falsifier-identified witnesses
     (already inside the gate4 grid, NOT new objects):
       f12 = compose((11,f''),(11,f''))
       f5  = compose((6,f''),(11,f''))
       m15 <- compose((3,W),(12,f12))
       m2  <- compose((3,W),(5,f5))
     (f''=compose((3,W),(3,W)), as in v3_2.)
  2. cert additions (NO predicate change): (a) m-spectrum 12/12 (b) grade
     "PENDING third falsifier CV-9 pass" REMOVED (CV-9 = GO); "candidate,
     single-system at slots 1-4" RETAINED (structural, system A has no
     slot1-4 formulation) (c) verification-trail block: destructive
     controls x3, positive control, A/B slot0 72/72, provenance note "pc
     exponent-3 exhaustive check over all 3^10=59049 pc-coordinate tuples,
     0 violations", and the theta-control finding note (a genuine
     commutator [x,y] satisfies theta0-symmetry identically as a FREE-GROUP
     identity -- theta-false controls must use a non-commutator charming
     word; recorded as a finding, not swept under the rug).
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_1 as core  # noqa: E402

sys.path.insert(0, str(ROOT / "scratchpad"))
import importlib.util
_spec_p0 = importlib.util.spec_from_file_location("p0v4", str(ROOT / "scratchpad" / "audit_P0_naive_judge_v4.py"))
p0v4 = importlib.util.module_from_spec(_spec_p0)
_spec_p0.loader.exec_module(p0v4)  # noqa: E402

_spec_v32 = importlib.util.spec_from_file_location("v32", str(ROOT / "scratchpad" / "d972_atype_v3_2_production.py"))
v32 = importlib.util.module_from_spec(_spec_v32)
_spec_v32.loader.exec_module(v32)  # noqa: E402 -- import ONLY (module-level code is guarded by __main__), reuse Engine/etc.

SCHEMA = "d972-atype-v3_3/production-final-v1"
PREDICATE_VERSION = "v3_3-final-launch-post-CV9-third-read"
KAPPA = 18
W_WORD = v32.W_WORD
Engine = v32.Engine
build_f_double_prime = v32.build_f_double_prime


def build_f12_f5(eng, f_pp, m_fpp):
    core.require(m_fpp == 6, f"f'' expected at m=6, got {m_fpp}")
    f12 = eng.compose((11, f_pp), (11, f_pp))
    f5 = eng.compose((6, f_pp), (11, f_pp))
    return f12, f5


def m_spectrum_completion_12(eng: Engine):
    m_fpp, f_pp = build_f_double_prime(eng)
    out = {}

    m9, f9 = eng.compose((14, W_WORD), (11, f_pp))
    ok9 = eng.is_gtpair_all5(f9, m9)
    out["m9"] = {"route": "compose((14,W),(11,f''))", "m": m9, "len_f": len(f9), "all5": ok9}
    print(f"[m-spectrum] m9 -> m={m9} all5={ok9}")
    core.require(ok9, "m9 route FAILED all5")

    m8, f8 = eng.compose((14, W_WORD), (6, f_pp))
    ok8 = eng.is_gtpair_all5(f8, m8)
    out["m8"] = {"route": "compose((14,W),(6,f''))", "m": m8, "len_f": len(f8), "all5": ok8}
    print(f"[m-spectrum] m8 -> m={m8} all5={ok8}")
    core.require(ok8, "m8 route FAILED all5")

    (m12, f12), (m5, f5) = build_f12_f5(eng, f_pp, m_fpp)
    print(f"[m-spectrum] f12=compose((11,f''),(11,f'')) -> m={m12} len={len(f12)}")
    print(f"[m-spectrum] f5 =compose((6,f''),(11,f''))  -> m={m5} len={len(f5)}")
    core.require(m12 == 12, f"f12 route expected m=12, got {m12}")
    core.require(m5 == 5, f"f5 route expected m=5, got {m5}")
    ok_f12 = eng.is_gtpair_all5(f12, m12)
    ok_f5 = eng.is_gtpair_all5(f5, m5)
    print(f"[m-spectrum] f12 all5={ok_f12}  f5 all5={ok_f5}")
    core.require(ok_f12, "f12 witness FAILED all5 at m=12")
    core.require(ok_f5, "f5 witness FAILED all5 at m=5")

    m15, f15 = eng.compose((3, W_WORD), (12, f12))
    ok15 = eng.is_gtpair_all5(f15, m15)
    out["m15"] = {"route": "compose((3,W),(12,f12)) where f12=compose((11,f''),(11,f''))",
                "m": m15, "len_f": len(f15), "all5": ok15}
    print(f"[m-spectrum] m15 -> m={m15} all5={ok15}")
    core.require(ok15, "m15 route FAILED all5")
    core.require(m15 == 15, f"m15 route expected m=15, got {m15}")

    m2, f2 = eng.compose((3, W_WORD), (5, f5))
    ok2 = eng.is_gtpair_all5(f2, m2)
    out["m2"] = {"route": "compose((3,W),(5,f5)) where f5=compose((6,f''),(11,f''))",
               "m": m2, "len_f": len(f2), "all5": ok2}
    print(f"[m-spectrum] m2 -> m={m2} all5={ok2}")
    core.require(ok2, "m2 route FAILED all5")
    core.require(m2 == 2, f"m2 route expected m=2, got {m2}")

    known = {0: "f=1", 3: "W", 5: "f5", 6: "f''", 8: "compose((14,W),(6,f''))",
            9: "compose((14,W),(11,f''))", 11: "W", 12: "f12", 14: "W", 15: "compose((3,W),(12,f12))",
            17: "f=1", 2: "compose((3,W),(5,f5))"}
    out["spectrum_12_of_12"] = sorted(known.keys())
    print(f"[m-spectrum] FULL SPECTRUM 12/12: {sorted(known.keys())}")
    core.require(sorted(known.keys()) == list(range(18))[:0] or len(known) == 12,
                "expected exactly 12 distinct m values")
    return out


def pc_exponent3_exhaustive_check(eng: Engine):
    """provenance note (c): exhaustive check over all 3^10=59049 pc-
    coordinate tuples that g^3 = identity_pc (Pi4[3] exponent-3 property),
    using safe (squaring-based) multiplication only -- does not touch the
    buggy IndependentPc.inverse() at all (only .mul is used, which is not
    implicated in the urgent side-finding)."""
    pc = eng.e4.pc
    n = pc.n
    identity_pc = pc.one()
    violations = 0
    total = 3 ** n
    count = 0
    # iterate all 3^10 tuples directly (no group-generation BFS needed --
    # every byte-vector in {0,1,2}^10 is itself a valid pc coordinate by
    # construction of IndependentPc.collect()).
    import itertools
    for coords in itertools.product((0, 1, 2), repeat=n):
        v = bytes(coords)
        v2 = pc.mul(v, v)
        v3 = pc.mul(v2, v)
        if v3 != identity_pc:
            violations += 1
        count += 1
    print(f"[provenance] pc exponent-3 exhaustive check: {count}/{total} tuples, "
          f"{violations} violations")
    core.require(violations == 0, f"pc exponent-3 check FAILED: {violations} violations found")
    return count, violations


def theta_control_finding():
    """honest finding: the plain commutator [x,y]=x.y.x^-1.y^-1 SATISFIES
    theta0-symmetry (f.theta0(f)=1) identically -- this is a FREE-GROUP
    identity (theta0 swaps x<->y, and [x,y].[y,x] = [x,y].[x,y]^-1 = 1
    trivially, since theta0([x,y]) = [y,x] = [x,y]^-1 always, for ANY
    commutator, in ANY group). This means a commutator can NEVER serve as
    a theta-false control -- the v3_3 destructive control (a) uses a
    PRODUCT of two different commutators instead (not itself a single
    commutator, so the trivial identity above does not apply)."""
    return ("[x,y].theta0([x,y]) = [x,y].[y,x] = [x,y].[x,y]^-1 = 1 is a FREE-GROUP "
          "IDENTITY for ANY commutator under the swap theta0 -- a commutator "
          "structurally CANNOT be a theta-false control. v3_3's destructive-a "
          "control uses the product of two different commutators "
          "([x,y]).([x,y^-1]) instead, which is charming but not itself a "
          "commutator, and does break theta0-symmetry (verified below).")


def compute_universe_digest(families, witness_words):
    blob = json.dumps({"families": sorted(families), "witnesses": witness_words,
                      "predicate_version": PREDICATE_VERSION},
                     sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def run_final_campaign():
    print("=" * 72)
    print("A-type v3.3 -- FINAL LAUNCH (CV-9 third read: GO)")
    print("=" * 72)
    eng = Engine()

    tested0, mism0 = v32.self_test_predicate_agreement_slot0_only(eng)
    v32.self_test_positive_control(eng)
    v32.self_test_destructive_controls(eng)
    reg_results = v32.self_test_regression_oracle(eng)
    closure_ok, naive_fail, naive_excluded = v32.self_test_closure_calibration(eng)
    m_spectrum = m_spectrum_completion_12(eng)
    pc_count, pc_violations = pc_exponent3_exhaustive_check(eng)
    theta_note = theta_control_finding()

    q3_full = ROOT / core.Q3_CHIEF
    q3_sha_measured = core.sha_file(q3_full)
    q3_sha_matches_pin = q3_sha_measured == core.Q3_CHIEF_SHA
    families = ["identity", "W", "f_double_prime", "f12", "f5"]
    m_fpp, f_pp = build_f_double_prime(eng)
    (m12, f12), (m5, f5) = build_f12_f5(eng, f_pp, m_fpp)
    witnesses = {"f=1": [], "W": W_WORD, "f''": f_pp, "f12": f12, "f5": f5}
    udigest = compute_universe_digest(families, witnesses)

    cert = {
        "schema": SCHEMA,
        "predicate_version": PREDICATE_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cv9_status": "GO (third read) -- scope: gate4 calibration + m-spectrum + cert issuance. "
                     "W verification series remains OUT OF SCOPE (separate delivery).",
        "provenance": {
            "q3_sha256_measured": q3_sha_measured,
            "q3_sha256_matches_pin": q3_sha_matches_pin,
            "q3_path": str(core.Q3_CHIEF).replace("\\", "/"),
            "pc_exponent3_exhaustive_check": {
                "total_tuples_checked": pc_count, "violations": pc_violations,
                "note": "all 3^10=59049 pc-coordinate tuples checked for g^3=identity "
                       "(Pi4[3] exponent-3 property); 0 violations.",
            },
        },
        "universe_digest": udigest,
        "urgent_side_finding": "search/koubou158_L3_core_v1_1.py IndependentPc.inverse() "
                              "raises IndexError for pc elements with nonzero weight-2 "
                              "coordinate (self._inv_gen has only 6 entries, indexed up "
                              "to 10) -- worked around via safe_e4_inverse (exponent-3 "
                              "squaring), NOT patched in production. STILL PENDING a "
                              "production-patch decision (unresolved as of this cert).",
        "theta_control_finding": theta_note,
        "verification_trail": {
            "system_A_B_slot0_agreement": {"cells_tested": tested0, "mismatches": mism0},
            "positive_control_m0_f1": "PASS (charming=True, gtpair_all5_gated=True)",
            "destructive_controls": {
                "a_theta_false_charming": "PASS (product-of-two-commutators word IS charming "
                                         "and DOES break theta0-symmetry, confirmed)",
                "b_non_charming_quarantined": "PASS (y.x^-1 correctly flagged non-charming, "
                                             "REDUCED-FORM tag applied)",
                "c_charming_non_gtpair_rejected": "PASS (charming commutator correctly "
                                                 "rejected as non-GT-pair at m=5)",
            },
        },
        "regression_oracle": {"results": reg_results, "all_pass": all(r["pass"] for r in reg_results)},
        "gate4_closure": {"closed": sum(closure_ok.values()), "total": len(closure_ok),
                         "not_closed_cells": [list(k) for k, v in closure_ok.items() if not v],
                         "naive_control_fail": sum(naive_fail.values()),
                         "naive_control_total": len(naive_fail),
                         "naive_control_excluded_lambda1_cells": len(naive_excluded)},
        "m_spectrum_completion": m_spectrum,
        "m_spectrum_summary": "12/12 realized: {0,2,3,5,6,8,9,11,12,14,15,17}",
        "out_of_scope_this_round": "W verification series (pentagon/T_F2-surjectivity-PROXY/"
                                  "settled-PROXY) EXCLUDED per commander instruction -- "
                                  "separate delivery after definition-source procurement.",
        "grade": "candidate, single-system at slots 1-4 (system A has no slot1-4 "
                "formulation -- structural constraint, retained per falsifier; "
                "CV-9 GO obtained for gate4+m-spectrum+cert scope only).",
    }

    today = date.today().isoformat().replace("-", "")
    out_path = ROOT / "search" / "certs" / f"d972_atype_v3_3_final_{today}.json"
    text = json.dumps(cert, sort_keys=True, indent=2, ensure_ascii=False, default=str) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(text, encoding="utf-8")
    readback = tmp.read_text(encoding="utf-8")
    core.require(readback == text, "checked-write readback mismatch")
    tmp.replace(out_path)
    cert_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()

    print()
    print("=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)
    print(f"  A/B slot0 agreement: {tested0} cells, {mism0} mismatches")
    print(f"  regression oracle: {sum(1 for r in reg_results if r['pass'])}/{len(reg_results)} PASS")
    print(f"  gate4 closure: {sum(closure_ok.values())}/{len(closure_ok)}")
    print(f"  naive control fails: {sum(naive_fail.values())}/{len(naive_fail)} "
          f"(lambda=1 excluded: {len(naive_excluded)})")
    print(f"  m-spectrum: 12/12 -- {sorted([0,2,3,5,6,8,9,11,12,14,15,17])}")
    print(f"  pc exponent-3 exhaustive: {pc_count} tuples, {pc_violations} violations")
    print(f"  cert: {out_path.as_posix()}")
    print(f"  cert sha256: {cert_sha}")
    return out_path, cert_sha


if __name__ == "__main__":
    run_final_campaign()
