#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scratchpad/build_v2_cert.py -- wraps the GAP-produced row/witness jsonl output
of scratchpad/koubou83_A2_48sweep_v2.g into the two final deliverable JSON certs:
  search/certs/koubou83_A2_48sweep_v2_20260822.json
  search/certs/koubou83_A2_48sweep_v2_witness_export_20260822.json
Pure provenance/formatting wrapper -- does NOT recompute or alter any GAP-produced
verdict, cond1/cond2/cond3 value, or witness content. All hashes are machine-computed
here (hashlib), never hand-copied.
"""
import json
import hashlib
import datetime

ROOT = r"C:\Users\81905\Desktop\shadow-atelier"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def read_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


rows_path = ROOT + r"\search\certs\koubou83_A2_48sweep_v2_20260822_rows.jsonl"
wit_path = ROOT + r"\search\certs\koubou83_A2_48sweep_v2_20260822_witness.jsonl"
script_v2_path = ROOT + r"\scratchpad\koubou83_A2_48sweep_v2.g"
script_v1_path = ROOT + r"\scratchpad\koubou83_A2_48sweep_v1.g"
run_log_path = ROOT + r"\scratchpad\koubou83_A2_48sweep_v2_run2.log"

rows = read_jsonl(rows_path)
wit_rows = read_jsonl(wit_path)

# ---- per-window, per-prime tallies ----
windows = sorted(set(tuple(r["window"]) for r in rows))
summary = {}
for w in windows:
    wkey = f"{w[0]}_{w[1]}"
    summary[wkey] = {}
    for p in (2, 3):
        sub = [r for r in rows if tuple(r["window"]) == w and r["p"] == p]
        n_survive = sum(1 for r in sub if r["survives_v2"] is True)
        n_changed = sum(1 for r in sub if r["changed_v1_to_v2"] is True)
        n_died_on_cond3_only = sum(
            1 for r in sub
            if r["cond1"] is True and r["cond2"] is True and r["legalOk"] is True
            and r["directOk"] is True and r["cond3"] is False
        )
        summary[wkey][f"p{p}"] = {
            "n_survive_v2": n_survive,
            "n_total": len(sub),
            "n_changed_from_v1": n_changed,
            "n_died_on_cond3_only_all_other_gates_passed": n_died_on_cond3_only,
            "v1_survive_count_for_reference": sum(1 for r in sub if r["survives_v1"] is True),
        }

# ---- diff manifest: only the rows whose verdict changed ----
diff_rows = [r for r in rows if r["changed_v1_to_v2"] is True]

# ---- cond3_method distribution (audit trail that no brute enumeration was used) ----
method_dist = {}
for p in (2, 3):
    d = {}
    for r in rows:
        if r["p"] != p:
            continue
        d[r["cond3_method"]] = d.get(r["cond3_method"], 0) + 1
    method_dist[f"p{p}"] = d

kerdims = {}
for p in (2, 3):
    vals = [r["kerDim"] for r in rows if r["p"] == p]
    kerdims[f"p{p}"] = {"min": min(vals), "max": max(vals)}

cert = {
    "cert_schema": "koubou83-A2-48sweep-v2/1",
    "generated": datetime.datetime.now().isoformat(),
    "purpose": (
        "Sol reply 154 (sol/sol_reply_154_daily.md sec.1 F1) fix re-run: charmOk in "
        "scratchpad/koubou83_A2_48sweep_v1.g checked only p|A, p|B for (A,B) in "
        "p*Lambda_N, omitting the third condition (A+B)==0 (mod 3p) required by the "
        "actual definition Lambda_N={(a,b):3|a+b}. This cert re-derives the FULL "
        "3-condition charming test for the full-48 sweep at p in {2,3}, both windows, "
        "using an exact (non-sampled) existence argument over the affine solution "
        "coset xiAug+Ker(augMat) rather than brute enumeration (kernel dimension "
        "measured at 10-23, far beyond p^dim brute force -- see script header comment "
        "in koubou83_A2_48sweep_v2.g for the full derivation)."
    ),
    "provenance": {
        "note_external_audit_gate": (
            "F1 was caught by EXTERNAL audit (Sol reply 154), not by this campaign's "
            "own internal verification net. Sol flagged p=3 only; this re-run applied "
            "the same general 3-condition formula to p=2 as well per commander "
            "instruction, since nothing in the mathematics privileges p=3."
        ),
        "script_v2_path": "scratchpad/koubou83_A2_48sweep_v2.g",
        "script_v2_sha256": sha256_of(script_v2_path),
        "script_v1_path": "scratchpad/koubou83_A2_48sweep_v1.g (UNCHANGED, kept for diff provenance)",
        "script_v1_sha256": sha256_of(script_v1_path),
        "rows_jsonl_path": "search/certs/koubou83_A2_48sweep_v2_20260822_rows.jsonl",
        "rows_jsonl_sha256": sha256_of(rows_path),
        "rows_jsonl_bytes": __import__("os").path.getsize(rows_path),
        "witness_jsonl_path": "search/certs/koubou83_A2_48sweep_v2_20260822_witness.jsonl",
        "witness_jsonl_sha256": sha256_of(wit_path),
        "run_log_path": "scratchpad/koubou83_A2_48sweep_v2_run2.log",
        "run_log_sha256": sha256_of(run_log_path),
        "v1_baseline_source": (
            "scratchpad/koubou83_A2_48sweep_v1.log (all 96 rows, both windows, both "
            "primes: survives=TRUE; this is the diff comparison target hardcoded into "
            "koubou83_A2_48sweep_v2.g as v1_p2/v1_p3)"
        ),
        "gap_invocation": ".\\gap.ps1 scratchpad\\koubou83_A2_48sweep_v2.g (via gap.ps1, -o 2g per project convention)",
        "elapsed_ms_this_run": 257773,
        "gap_version": "gap-4.16.0 (per gap.ps1 hardcoded runtime path; per project CLAUDE.md installed version)",
    },
    "universe": {
        "windows": [list(w) for w in windows],
        "primes_swept": [2, 3],
        "shadows_per_window": 48,
        "note_universe_scope": (
            "Same registered universe as v1: [1152,154161] and [1152,154163] windows, "
            "full 48-element GT(N) corr set per window, p in {2,3}. v1 also did NOT "
            "sweep p=5 (no mach5/Solve5 built in v1), so p=5 is NOT included here "
            "either -- this is a scope match to v1, not a silent narrowing."
        ),
    },
    "summary_by_window_and_prime": summary,
    "cond3_method_distribution": method_dist,
    "kernel_dimension_range_augMat": kerdims,
    "method_note": (
        "cond3_method values seen: 'invariant-gcd(p,3)=1-baseline-definitive' (p=2: "
        "proven mathematically that cond3's truth value is IDENTICAL for every point "
        "of the affine solution coset, regardless of kernel dimension -- derivation in "
        "script header; the v1 baseline witness's cond3 value is therefore the exact, "
        "exhaustive answer, not a partial search), 'baseline-sufficient' (p=3: the v1 "
        "baseline witness already satisfies cond3, so no coset search was needed), "
        "'kernel-shift-constructed-cN' (p=3 only, not encountered in this run: an "
        "explicit alternate witness in the coset was constructed and re-verified), "
        "'EXHAUSTED-orthogonal-to-entire-kernel-PROVEN-DEATH' (p=3 only, not "
        "encountered in this run: proven, via kernel-orthogonality of the v-vector, "
        "that NO point of the coset can satisfy cond3 -- a genuine structural death, "
        "not an unsearched gap). No row in this run required the "
        "'kernel-shift-attempted-no-c-worked-INVESTIGATE' escape hatch or the "
        "'ASSUMPTION-VIOLATED' escape hatch (both zero occurrences -- see "
        "cond3_method_distribution and the assumption_violated field, all False)."
    ),
    "diff_vs_v1": {
        "n_rows_changed": len(diff_rows),
        "changed_rows": diff_rows,
    },
    "row_manifest": rows,
}

out_path = ROOT + r"\search\certs\koubou83_A2_48sweep_v2_20260822.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cert, f, indent=2, ensure_ascii=False)
    f.write("\n")

# ---- witness export (separate file, per task instruction 5) ----
wit_cert = {
    "cert_schema": "koubou83-A2-48sweep-v2-witness-export/1",
    "generated": datetime.datetime.now().isoformat(),
    "purpose": (
        "Object-identity-only witness export for independent cross-checker extension "
        "(judgment-logic-free: raw sigma-word witnesses only, no verdicts)."
    ),
    "provenance": {
        "witness_jsonl_source": "search/certs/koubou83_A2_48sweep_v2_20260822_witness.jsonl",
        "witness_jsonl_sha256": sha256_of(wit_path),
    },
    "witnesses": wit_rows,
}
wit_out_path = ROOT + r"\search\certs\koubou83_A2_48sweep_v2_witness_export_20260822.json"
with open(wit_out_path, "w", encoding="utf-8") as f:
    json.dump(wit_cert, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("WROTE", out_path)
print("WROTE", wit_out_path)
print("cert sha256:", sha256_of(out_path))
print("cert bytes:", __import__("os").path.getsize(out_path))
print("witness export sha256:", sha256_of(wit_out_path))
print("witness export bytes:", __import__("os").path.getsize(wit_out_path))
print(json.dumps(summary, indent=2))
