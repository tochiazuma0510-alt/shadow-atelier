#!/usr/bin/env python3
"""search/norm-embedding-seal-build.py

Builds search/certs/norm_embedding_manifest_20260731.json (P87-3,
sol_reply_87_math14.md F87-2.2). The committed norm_embedding.g had an
extra `fi` that closed the innermost loop's enclosing if-block early,
silently halving the (m,f)-scan for every window with N_ord != {1} where
the "else" branch (odd-coset case) was reachable -- this showed up as
shadow_total/ker_size exactly half the true GTSh order/kernel order for
several windows (A11/A12/A13, I10, D family). The one-line fix (dropping
the stray `fi`) is already applied in the working tree; this script binds
the fixed script and its regenerated certificate to a manifest so the fix
cannot silently drift again, and independently cross-checks the 9
regenerated (shadow_total, ker_size) pairs against GTSh order/kernel-order
values already recorded in OTHER, unrelated certs (a13_ladder_* for the
E-family ladder windows, i10_1_xi_recheck for the two I10-1 windows,
w62_splitting for the D-family windows) -- none of which import
norm_embedding.g or share its code path.

Reads only already-written files. Does not import norm_embedding.g logic.
"""
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTS = os.path.join(ROOT, "search", "certs")
SCRIPT_PATH = os.path.join(ROOT, "search", "probe", "wac_v1", "norm_embedding.g")
CERT_PATH = os.path.join(CERTS, "norm_embedding_20260731.json")

GAP_VERSION = "4.16.0"  # C:\Program Files\GAP-4.16.0, per gap.ps1 / CLAUDE.md


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_str(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


# --- 1. parse DoWindow(...) calls out of the script source to build a
#        canonical id per window, directly from what the script itself
#        currently contains (tamper-evident: any edit to n/a1/b1/wid
#        changes this hash). ---
def parse_dowindow_calls(src):
    # DoWindow(nn, a1, b1, "wid");  -- a1/b1 are GAP permutation literals
    # possibly spanning "(...)(...)..." with no internal top-level commas,
    # so we split on the comma that precedes the final quoted wid arg and
    # the comma right after the leading integer.
    calls = []
    for m in re.finditer(r'DoWindow\(\s*(\d+)\s*,\s*(.*?)\s*,\s*(.*?)\s*,\s*"([^"]+)"\s*\)\s*;',
                          src, flags=re.S):
        nn, a1, b1, wid = m.groups()
        a1 = re.sub(r'\s+', ' ', a1.strip())
        b1 = re.sub(r'\s+', ' ', b1.strip())
        calls.append({"wid": wid, "n": int(nn), "a1": a1, "b1": b1})
    return calls


# --- 2. independent (already-committed, unrelated-codepath) GTSh
#        order / kernel-order references per window. ---
def load_reference(wid):
    e_family_files = {
        "W-E-A10-9t1": "a13_ladder_W_E_A10_9t1_20260730.json",
        "W-E-A11-9t2": "a13_ladder_W_E_A11_9t2_20260730.json",
        "W-E-A12-9t3": "a13_ladder_W_E_A12_9t3_20260730.json",
        "W-E-A13-9t4": "a13_ladder_W_E_A13_9t4_20260730.json",
    }
    if wid in e_family_files:
        with open(os.path.join(CERTS, e_family_files[wid]), encoding="utf-8") as f:
            d = json.load(f)
        return {
            "source": rel(os.path.join(CERTS, e_family_files[wid])),
            "group_order": d["1_group_order"],
            "ker_size": d["2_ker_size"],
        }
    if wid in ("W-E-A10-5x2t0", "W-E-A15-5x3t0"):
        path = os.path.join(CERTS, "i10_1_xi_recheck_20260730.json")
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        for w in d["windows"]:
            if w["wid"] == wid:
                return {
                    "source": rel(path) + f" (window {wid})",
                    "group_order": w["accepted_count"],
                    "ker_size": w["m0_layer_count"],
                }
        raise KeyError(wid)
    if wid in ("W-D-A16-11a", "W-D-A18-13a", "W-D-A20-15a"):
        path = os.path.join(CERTS, "w62_splitting_20260729.json")
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        for r in d["results"]:
            if r["window_id"] == wid:
                return {
                    "source": rel(path) + f" (results[wid={wid}])",
                    "group_order": r["G_order"],
                    "ker_size": r["K_order"],
                }
        raise KeyError(wid)
    raise KeyError(wid)


def main():
    with open(SCRIPT_PATH, encoding="utf-8") as f:
        src = f.read()
    calls = parse_dowindow_calls(src)

    with open(CERT_PATH, encoding="utf-8") as f:
        cert = json.load(f)
    cert_by_wid = {w["window_id"]: w for w in cert["windows"]}

    script_sha256 = sha256_file(SCRIPT_PATH)
    cert_sha256 = sha256_file(CERT_PATH)

    windows_out = []
    all_match = True
    for c in calls:
        wid = c["wid"]
        canonical_id = f"{wid}|n={c['n']}|a1={c['a1']}|b1={c['b1']}"
        canonical_id_sha256 = sha256_str(canonical_id)

        w = cert_by_wid[wid]
        ref = load_reference(wid)
        nine_over_nine_ok = (
            w["kernel_trivial"] is True
            and w["hom_right"] is True
            and w["hom_left"] is False
            and w["image_order_eq_gtsh"] is True
            and w["image_is_subgroup_of_normalizer"] is True
            and w["alpha_well_defined"] is True
        )
        ref_match = (w["shadow_total"] == ref["group_order"]) and (w["ker_size"] == ref["ker_size"])
        all_match = all_match and nine_over_nine_ok and ref_match

        windows_out.append({
            "window_id": wid,
            "n": c["n"],
            "canonical_id_sha256": canonical_id_sha256,
            "shadow_total": w["shadow_total"],
            "ker_size": w["ker_size"],
            "distinct_alphas": w["distinct_alphas"],
            "kernel_trivial": w["kernel_trivial"],
            "hom_left": w["hom_left"],
            "hom_right": w["hom_right"],
            "image_order_eq_gtsh": w["image_order_eq_gtsh"],
            "image_is_subgroup_of_normalizer": w["image_is_subgroup_of_normalizer"],
            "nine_property_checks_pass": nine_over_nine_ok,
            "independent_reference": {
                "source": ref["source"],
                "group_order": ref["group_order"],
                "ker_size": ref["ker_size"],
            },
            "reference_matches_norm_embedding": ref_match,
        })

    manifest = {
        "schema": "norm-embedding-manifest/v1",
        "generated_by": {
            "tool": "python3",
            "script": "search/norm-embedding-seal-build.py",
        },
        "note": (
            "P87-3 seal (sol_reply_87_math14.md F87-2.2 / P87-3): binds the "
            "fixed search/probe/wac_v1/norm_embedding.g (extra `fi` removed "
            "-- see script diff) and its regenerated certificate "
            "search/certs/norm_embedding_20260731.json into one manifest, "
            "with per-window canonical-id hashes parsed directly from the "
            "script's own DoWindow(...) call arguments, and a cross-check "
            "against GTSh order / kernel order values already recorded in "
            "OTHER certs that do not import this script (a13_ladder_* for "
            "the E-family ladder windows, i10_1_xi_recheck for the two "
            "I10-1 windows, w62_splitting for the D-family windows). "
            "'measured PASS' (F87-2.1, 9/9) becomes 'artifact confirmed' "
            "only once this manifest and the underlying script/cert are "
            "committed together."
        ),
        "gap_version": GAP_VERSION,
        "script": {
            "path": rel(SCRIPT_PATH),
            "sha256": script_sha256,
        },
        "certificate": {
            "path": rel(CERT_PATH),
            "sha256": cert_sha256,
        },
        "windows_processed": len(windows_out),
        "windows": windows_out,
        "all_nine_windows_pass_and_match_independent_reference": all_match,
    }

    out_path = os.path.join(CERTS, "norm_embedding_manifest_20260731.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", rel(out_path))
    print("windows_processed =", len(windows_out))
    print("all_nine_windows_pass_and_match_independent_reference =", all_match)
    for w in windows_out:
        print(" ", w["window_id"], "shadow_total=", w["shadow_total"], "ker_size=", w["ker_size"],
              "ref_match=", w["reference_matches_norm_embedding"],
              "9props=", w["nine_property_checks_pass"])


if __name__ == "__main__":
    main()
