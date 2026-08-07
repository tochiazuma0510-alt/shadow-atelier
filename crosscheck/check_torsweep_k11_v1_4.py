#!/usr/bin/env python3
"""
Independent checker for the TOR-SWEEP k=11 v1.4 closure cert (裁定737(3) /
裁定739 full-column adaptive-pivot Howell elimination modulo M). Reads ONLY
the cert JSON file -- does NOT import search/torsweep_k11_close_v1_4.py or
edim_semidirect_v1.py (search/crosscheck separation).

Disclosed limitation (honest, not silently skipped): the FULL exact N_11
matrix (H_rank x up to ~179,195 word-ambient columns, big-integer entries)
is NOT embedded in the v1.4 cert -- it would be far too large for a JSON
cert (tens to hundreds of MB of big integers). Consequently this checker
CANNOT independently redo the core exact reconstruction (stage FULL1), the
reconstruction canary (stage FULL2b), or the Howell elimination arithmetic
itself (stage FULL3) from the cert alone. What IS independently checked
from the cert's own recorded fields:
  - schema / supersedes bookkeeping
  - internal consistency of the FULL2 ground-truth cross-check claim
    (mismatches==0 iff ground_truth_match)
  - the bound argument's own arithmetic (measured_max_abs_entry vs the two
    recorded moduli, i.e. that the cert's own numbers support its claimed
    "modulus >> 2*max|entry|" argument)
  - the FULL2b canary's own internal consistency (裁定742/743: rank mod
    each canary prime must equal r_prime_target; input provenance note
    must be present, since this exact canary produced a false-positive
    "reconstruction bug" report earlier in this cert's development when
    accidentally fed mod-M-reduced data instead of the true exact rows --
    see 裁定743 lesson recorded in the cert itself)
  - the closures list's internal arithmetic: for every "split" that appears
    implicitly in the recursive structure, the product of all reported
    piece moduli (by status) reconstitutes target_M; every status is one of
    the legal 裁定741-corrected outcomes; "success" pieces' pivot_count
    equals r_prime_target (NOT H_rank -- 裁定741's bugfix is exactly that
    H_rank is the wrong target)
  - the two_system_crosscheck section's own arithmetic (target-modulus
    divisibility relationship, outcome agreement flags), if present
  - S-TOR-4 judgement-word scan
This is a cross-check of bookkeeping/arithmetic self-consistency, NOT a
recomputation of the underlying algebra -- exactly the same category of
disclosed limitation as crosscheck/check_torsweep_k11_t4t5.py's "escalated
tier" note.

Usage: python crosscheck/check_torsweep_k11_v1_4.py <cert_path>
"""
import json
import sys
from functools import reduce
from math import gcd


def fail(msg, failures):
    failures.append(msg)
    print(f"FAIL: {msg}")


def check(cert_path):
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)
    failures = []
    warnings = []

    if cert.get("schema") != "tor_sweep_k11_v1.4":
        fail(f"unexpected schema {cert.get('schema')!r}", failures)
    if cert.get("k") != 11:
        fail(f"unexpected k {cert.get('k')!r}", failures)
    if not cert.get("supersedes"):
        fail("v1.4 cert missing 'supersedes' reference to v1.3", failures)

    try:
        target_M = int(cert["target_M"])
    except (KeyError, ValueError):
        fail("missing/unparseable target_M", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0
    if len(str(target_M)) != cert.get("target_M_digits"):
        fail(f"target_M_digits={cert.get('target_M_digits')} != "
             f"len(str(target_M))={len(str(target_M))}", failures)

    # ---------------- FULL1: exact reconstruction ----------------
    f1 = cert.get("stages", {}).get("FULL1_exact_reconstruction")
    if f1 is None:
        fail("missing stages.FULL1_exact_reconstruction", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    warnings.append("FULL1's exact full-column N_11 reconstruction (two "
                     "huge-modulus centre-lift passes over ~186 Lyndon "
                     "basis trees) is NOT independently recomputable from "
                     "the cert alone -- the resulting matrix (H_rank x up "
                     "to ~179,195 big-integer columns) is not embedded "
                     "(would be far too large for a JSON cert). This "
                     "checker only verifies the cert's own internal "
                     "arithmetic/bookkeeping around FULL1, not the "
                     "algebra itself.")

    try:
        mod_a = int(f1["modulus_A"])
        mod_b = int(f1["modulus_B"])
        max_abs = int(f1["measured_max_abs_entry"])
    except (KeyError, ValueError):
        fail("FULL1 missing/unparseable modulus_A/modulus_B/measured_max_abs_entry", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    if not (mod_a > 2 * max_abs and mod_b > 2 * max_abs):
        fail(f"FULL1 bound argument does NOT hold on the cert's own numbers: "
             f"need modulus_A,modulus_B > 2*measured_max_abs_entry "
             f"({2*max_abs}), got modulus_A={mod_a}, modulus_B={mod_b} "
             f"-- the centre-lift exactness argument is NOT supported by "
             f"these recorded values", failures)

    if len(str(max_abs)) != f1.get("measured_max_abs_entry_digits"):
        fail("measured_max_abs_entry_digits inconsistent with measured_max_abs_entry", failures)

    if f1.get("full_word_ambient_dim") != f1.get("n_ambient_dim", 0) + f1.get("h_ambient_dim", 0):
        fail("full_word_ambient_dim != n_ambient_dim + h_ambient_dim", failures)
    if f1.get("n_ambient_dim") != 3 ** 11:
        fail(f"n_ambient_dim={f1.get('n_ambient_dim')} != 3**11={3**11}", failures)
    if f1.get("h_ambient_dim") != 2 ** 11:
        fail(f"h_ambient_dim={f1.get('h_ambient_dim')} != 2**11={2**11}", failures)

    exact_moduli_agree = f1.get("exact_moduli_agree")
    if exact_moduli_agree is not True:
        sr = cert.get("stop_rules", {}).get("S-TOR-1")
        if not sr or not sr.get("triggered"):
            fail("FULL1 exact_moduli_agree is not True but stop_rules.S-TOR-1 "
                 "not recorded as triggered", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    # ---------------- FULL2: ground-truth cross-check ----------------
    f2 = cert.get("stages", {}).get("FULL2_ground_truth_crosscheck")
    if f2 is None:
        fail("missing stages.FULL2_ground_truth_crosscheck", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0
    mism = f2.get("mismatches")
    expected_match = (mism == 0)
    if f2.get("ground_truth_match") != expected_match:
        fail(f"FULL2 ground_truth_match={f2.get('ground_truth_match')} "
             f"inconsistent with mismatches={mism}", failures)
    if f2.get("pivot_columns_checked", 0) < 3:
        fail(f"FULL2 pivot_columns_checked={f2.get('pivot_columns_checked')} "
             f"is suspiciously small (v1.2 recorded 60 pivot columns)", failures)

    if not expected_match:
        sr = cert.get("stop_rules", {}).get("S-TOR-1")
        if not sr or not sr.get("triggered"):
            fail("FULL2 ground-truth mismatch but stop_rules.S-TOR-1 not "
                 "recorded as triggered", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    # ---------------- FULL2b: mandatory reconstruction canary (裁定742/743) ----
    f2b = cert.get("stages", {}).get("FULL2b_reconstruction_canary")
    if f2b is None:
        fail("missing stages.FULL2b_reconstruction_canary (裁定742's "
             "mandatory gate -- a cert without this stage either predates "
             "the fix or skipped the gate)", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    r_prime_target = f2b.get("r_prime_target")
    results_by_prime = f2b.get("results_by_prime", {})
    canary_all_pass_computed = bool(results_by_prime) and all(
        v.get("pass") == (v.get("rank") == r_prime_target)
        for v in results_by_prime.values()
    )
    if f2b.get("all_pass") != canary_all_pass_computed:
        fail(f"FULL2b all_pass={f2b.get('all_pass')} inconsistent with "
             f"recomputed {canary_all_pass_computed} from results_by_prime", failures)
    for p, v in results_by_prime.items():
        if v.get("pass") is not True:
            fail(f"FULL2b canary FAILED at prime {p}: rank={v.get('rank')} "
                 f"!= r_prime_target={r_prime_target} -- per 裁定742 this "
                 f"should have stopped the run before any Howell elimination "
                 f"was attempted", failures)
    input_note = f2b.get("input", "")
    if "pre-mod-M" not in input_note and "true exact" not in input_note.lower():
        fail("FULL2b canary's 'input' provenance field does not document "
             "that TRUE EXACT (pre-mod-M) rows were used -- 裁定743's "
             "central lesson (a canary fed mod-M-reduced/derived data can "
             "see a phantom, since odd-M reduction flips parity) is "
             "unrecorded for this run", failures)

    if not f2b.get("all_pass"):
        sr = cert.get("stop_rules", {}).get("S-TOR-1")
        if not sr or not sr.get("triggered"):
            fail("FULL2b canary failed but stop_rules.S-TOR-1 not recorded "
                 "as triggered", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    # ---------------- FULL3: Howell elimination over full columns ----------------
    f3 = cert.get("stages", {}).get("FULL3_howell_full_columns")
    if f3 is None:
        fail("missing stages.FULL3_howell_full_columns", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    r_prime = f3.get("r_prime_target")
    if r_prime != r_prime_target:
        fail(f"FULL3 r_prime_target={r_prime} != FULL2b r_prime_target="
             f"{r_prime_target} -- inconsistent target between the canary "
             f"and the Howell elimination", failures)
    if r_prime == f3.get("H_rank"):
        warnings.append("r_prime_target equals H_rank in this cert -- if "
                         "that is a coincidence of the specific k/data this "
                         "is fine, but it was ALSO the exact symptom of "
                         "裁定741's bug (H_rank used instead of the true "
                         "Q-rank); double check this wasn't silently "
                         "reintroduced.")

    closures = f3.get("closures", [])
    if not closures:
        fail("FULL3 closures list is empty", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    VALID_STATUSES = {"trivial", "success", "insufficient_FULL_COLUMNS",
                       "anomaly_unit_witness_beyond_rank"}
    STOP_STATUSES = {"insufficient_FULL_COLUMNS", "anomaly_unit_witness_beyond_rank"}
    product_check = 1
    any_stop_computed = False
    for piece in closures:
        status = piece.get("status")
        if status not in VALID_STATUSES:
            fail(f"closures piece has unrecognized status {status!r} -- not "
                 f"one of the legal 裁定741-corrected outcomes", failures)
            continue
        try:
            m = int(piece["modulus"])
        except (KeyError, ValueError):
            fail(f"closures piece missing/unparseable modulus: {piece}", failures)
            continue
        product_check *= m
        if status == "success":
            pc = piece.get("pivot_count")
            if pc != r_prime:
                fail(f"closures 'success' piece has pivot_count={pc} != "
                     f"r_prime_target={r_prime} (裁定741: the target must "
                     f"be the Q-rank, not H_rank)", failures)
            zc = piece.get("zero_check_columns")
            if not isinstance(zc, int) or zc <= 0:
                fail(f"closures 'success' piece has invalid "
                     f"zero_check_columns={zc} -- this field records how "
                     f"many columns were checked for the dependent-row "
                     f"zero criterion (裁定741's positive success test)", failures)
        if status in STOP_STATUSES:
            any_stop_computed = True

    if product_check != target_M:
        fail(f"product of all closures piece moduli = {product_check} != "
             f"target_M = {target_M} -- the recursive split/close "
             f"bookkeeping does not reconstitute the original modulus", failures)

    all_success_expected = all(p.get("status") == "success" for p in closures)
    if f3.get("all_pieces_resolved_success") != all_success_expected:
        fail(f"all_pieces_resolved_success={f3.get('all_pieces_resolved_success')} "
             f"inconsistent with recomputed {all_success_expected} from closures", failures)
    if f3.get("any_stop_evidence") != any_stop_computed:
        fail(f"any_stop_evidence={f3.get('any_stop_evidence')} inconsistent "
             f"with recomputed {any_stop_computed} from closures", failures)

    if any_stop_computed:
        sr = cert.get("stop_rules", {}).get("QUAR-TOR")
        if not sr or not sr.get("triggered"):
            fail("FULL3 has stop-evidence but stop_rules.QUAR-TOR not "
                 "recorded as triggered", failures)

    # ---------------- two_system_crosscheck (if present) ----------------
    tsc = cert.get("two_system_crosscheck")
    if tsc is not None:
        tmc = tsc.get("target_modulus_comparison", {})
        try:
            this_M = int(tmc["this_M"])
            other_M = int(tmc["other_M"])
        except (KeyError, ValueError):
            fail("two_system_crosscheck.target_modulus_comparison has "
                 "missing/unparseable this_M/other_M", failures)
        else:
            if this_M != target_M:
                fail(f"two_system_crosscheck this_M={this_M} != this cert's "
                     f"own target_M={target_M}", failures)
            divides_recomputed = (other_M % this_M == 0)
            if tmc.get("other_M_divisible_by_this_M") != divides_recomputed:
                fail(f"two_system_crosscheck other_M_divisible_by_this_M="
                     f"{tmc.get('other_M_divisible_by_this_M')} != "
                     f"recomputed {divides_recomputed}", failures)
            if divides_recomputed:
                q_recomputed = str(other_M // this_M)
                if tmc.get("other_M_over_this_M") != q_recomputed:
                    fail(f"two_system_crosscheck other_M_over_this_M="
                         f"{tmc.get('other_M_over_this_M')} != recomputed "
                         f"{q_recomputed}", failures)
        oc = tsc.get("outcome_comparison", {})
        status_agrees_recomputed = (oc.get("this_status") == oc.get("other_status") == "success")
        if oc.get("status_agrees") != status_agrees_recomputed:
            fail(f"two_system_crosscheck status_agrees={oc.get('status_agrees')} "
                 f"!= recomputed {status_agrees_recomputed}", failures)
        pivot_agrees_recomputed = (oc.get("this_pivot_count") == oc.get("other_pivot_count") == 60)
        if oc.get("pivot_count_agrees") != pivot_agrees_recomputed:
            fail(f"two_system_crosscheck pivot_count_agrees="
                 f"{oc.get('pivot_count_agrees')} != recomputed "
                 f"{pivot_agrees_recomputed}", failures)
    else:
        warnings.append("no two_system_crosscheck section present in this "
                         "cert -- the independent-second-system comparison "
                         "(裁定740/743) has not been recorded here")

    # ---------------- judgement-word scan (S-TOR-4) ----------------
    banned_words = ["無条件", "捩れなし", "格上げ", "証明終わり", "verified",
                     "捩れ支持=∅", "確定"]
    cert_text = json.dumps(cert, ensure_ascii=False)
    for w in banned_words:
        if w in cert_text:
            fail(f"S-TOR-4 violation: banned judgement word {w!r} found in cert", failures)

    # ---------------- mojibake regression check (裁定739 requirement) --------
    if "�" in cert_text:
        fail("cert contains U+FFFD replacement characters -- the same "
             "encoding data-loss bug found in v1.3's critical_limitation_found "
             "field (裁定739 required this be fixed in v1.4)", failures)

    report(cert_path, failures, warnings)
    return len(failures) == 0


def report(cert_path, failures, warnings):
    print(f"\n=== check_torsweep_k11_v1_4.py report for {cert_path} ===")
    if warnings:
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  WARN: {w}")
    if failures:
        print(f"{len(failures)} FAILURE(S):")
        for f in failures:
            print(f"  FAIL: {f}")
        print("RESULT: cross-check FAILED")
    else:
        print("RESULT: cross-check PASSED (subject to the disclosed FULL1/"
              "FULL3 recomputation limitation above; this is a cross-check "
              "of cert-internal bookkeeping, not a Lean-level verification)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check_torsweep_k11_v1_4.py <cert_path>", file=sys.stderr)
        sys.exit(2)
    ok = check(sys.argv[1])
    sys.exit(0 if ok else 1)
