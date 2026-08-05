#!/usr/bin/env python3
"""
twin_witness_scope1_extract.py -- 双子 witness 走 scope 1 (登録集合の固定)

Reads search/certs/lins_twin_census_v1_20260806.json (INVENTORY ONLY twin
census cert, 裁定548 W-1) and machine-reproduces the prereg doc's (docs/notes/
twin_witness_prereg_iffirst_v1.md sec 1) layer counts and SETDIGESTs:

    L0 (all twin pairs)                174 unordered / 348 directed
    L1 (in_PB3 both members)            28 unordered /  56 directed
    L2 (L1 and c_in_N both members)     15 unordered /  30 directed  <- REGISTERED
    L3 (L1 and c_in_N false both)       13 unordered /  26 directed  <- NOT touched (T-1 hold)

UID scheme (reverse-engineered by brute-force format search against the
doc's published table values -- verified to match EXACTLY, all digits, for
every one of L0/L1/L2/L3's SETDIGEST and all 15 L2 pair UIDs / 30 member
UIDs before this script was trusted for anything downstream):

    member_uid(words) = sha256("|".join(words))[:12 hex chars]
    pair_uid(index, [m0,m1]) = sha256(f"{index}#{'#'.join(sorted([m0,m1]))}")[:12 hex chars]
    setdigest(layer_pair_uids) = sha256("|".join(sorted(layer_pair_uids))).hexdigest()  (full 64 hex)

This script performs NO group-theoretic computation and touches no window,
kernel, or mirror question -- pure data extraction from an already-generated
cert (regulation §規律申告 point 1 of the prereg doc).

Also emits search/twin_witness_l2_data_v1_generated.g: a GAP data file (list
literals only, no logic) holding the 15 L2 pairs' generator words + index +
pair UID, for the mirror-classification GAP script
(search/twin-witness-mirror-v1.g) to Read() -- avoids a second hand-
transcription channel and keeps GAP's job to computation, not JSON parsing.
"""
import json
import hashlib
import sys

CERT_PATH = "search/certs/lins_twin_census_v1_20260806.json"
EXPECTED_CERT_SHA256 = "8bfd762ef565f5ce72f9a4a25368783b96b02f4905274e858d460e30bb335610"

EXPECTED_SETDIGEST = {
    "L0": "babc71f11022694bafde5f4b73ab06c677fc25aee6cd3bff6651e2aaac47be87",
    "L1": "f94a8ae0384144189950d61ba727fc713a0eacb751a712784d5923a7a067daa3",
    "L2": "ec72ed77e1bb6040c5a4d29e43b51e45a63b5d2ffa6d50f8e8455aa16d7c9bba",
    "L3": "af88692a78341c82688169c4b3ade43b4d4c83ed0e7c54e160365249b0e18ebd",
}
EXPECTED_COUNTS = {"L0": 174, "L1": 28, "L2": 15, "L3": 13}


def member_uid(words):
    s = "|".join(words)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def pair_uid(index, muids):
    s = str(index) + "#" + "#".join(sorted(muids))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def setdigest(puids):
    return hashlib.sha256("|".join(sorted(puids)).encode("utf-8")).hexdigest()


def gap_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    with open(CERT_PATH, "rb") as f:
        raw = f.read()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != EXPECTED_CERT_SHA256:
        print(f"FATAL: cert sha256 mismatch: got {actual_sha}, expected {EXPECTED_CERT_SHA256}")
        sys.exit(1)

    d = json.loads(raw.decode("utf-8"))
    pairs_raw = d["twin_pairs"]

    L0, L1, L2, L3 = [], [], [], []
    mixed = 0
    for e in pairs_raw:
        idx = e["index"]
        ms = e["members"]
        assert len(ms) == 2, f"expected 2 members, got {len(ms)} at index {idx}"
        muids = [member_uid(m["canonical_id_words"]) for m in ms]
        puid = pair_uid(idx, muids)
        entry = {
            "index": idx,
            "pair_uid": puid,
            "member_uids": muids,
            "members": ms,
        }
        L0.append(entry)
        if all(m.get("in_PB3") for m in ms):
            L1.append(entry)
            c_vals = [m.get("c_in_N") for m in ms]
            if all(c_vals):
                L2.append(entry)
            elif not any(c_vals):
                L3.append(entry)
            else:
                mixed += 1

    layers = {"L0": L0, "L1": L1, "L2": L2, "L3": L3}
    ok = True
    for name, layer in layers.items():
        n = len(layer)
        sd = setdigest([e["pair_uid"] for e in layer])
        n_ok = (n == EXPECTED_COUNTS[name])
        sd_ok = (sd == EXPECTED_SETDIGEST[name])
        print(f"{name}: count={n} (expected {EXPECTED_COUNTS[name]}, {'OK' if n_ok else 'MISMATCH'})  "
              f"SETDIGEST={'OK' if sd_ok else 'MISMATCH: ' + sd}")
        ok = ok and n_ok and sd_ok

    print(f"mixed c_in_N pairs within L1 (expect 0): {mixed}")
    ok = ok and (mixed == 0)

    directed = {k: 2 * len(v) for k, v in layers.items()}
    print("directed counts:", directed)

    if not ok:
        print("FATAL: scope 1 machine reproduction did NOT match prereg doc sec 1. STOP.")
        sys.exit(1)

    print("\nscope 1 (registered-set fixation) machine-reproduced EXACTLY -- "
          "matches docs/notes/twin_witness_prereg_iffirst_v1.md sec 1 bit-for-bit "
          "(counts 174/28/15/13, directed 348/56/30/26, all 4 SETDIGESTs).")

    # ---- write GAP data file for the L2 registered set (mirror-classification input) ----
    L2_sorted = sorted(L2, key=lambda e: (e["index"], e["pair_uid"]))
    gap_lines = []
    gap_lines.append("#############################################################################")
    gap_lines.append("## twin_witness_l2_data_v1_generated.g -- GENERATED, do not hand-edit.")
    gap_lines.append("## Produced by search/twin_witness_scope1_extract.py from the sha256-verified")
    gap_lines.append(f"## census cert ({CERT_PATH}, sha256={EXPECTED_CERT_SHA256}).")
    gap_lines.append("## Data only (word lists + index + pair UID for the 15 registered L2 pairs).")
    gap_lines.append(f"## L2 SETDIGEST (recomputed, matches prereg doc sec 1.2): {setdigest([e['pair_uid'] for e in L2])}")
    gap_lines.append("#############################################################################")
    gap_lines.append("")
    gap_lines.append("L2Pairs := [")
    for e in L2_sorted:
        idx = e["index"]
        puid = e["pair_uid"]
        mA, mB = e["members"]
        muA, muB = e["member_uids"]
        wa = ", ".join(gap_str(w) for w in mA["canonical_id_words"])
        wb = ", ".join(gap_str(w) for w in mB["canonical_id_words"])
        gap_lines.append(f'  rec(index:={idx}, pair_uid:={gap_str(puid)},')
        gap_lines.append(f'      A_uid:={gap_str(muA)}, B_uid:={gap_str(muB)},')
        gap_lines.append(f'      A_idGroup:={gap_str(str(mA.get("id_group")))},')
        gap_lines.append(f'      A:=[{wa}],')
        gap_lines.append(f'      B:=[{wb}]),')
    gap_lines.append("];;")
    gap_lines.append("")

    out_path = "search/twin_witness_l2_data_v1_generated.g"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(gap_lines) + "\n")
    print(f"\nWrote {out_path} ({len(L2_sorted)} pairs)")

    # ---- also emit a JSON summary for provenance / the final twin_witness cert ----
    summary = {
        "cert_path": CERT_PATH,
        "cert_sha256": actual_sha,
        "counts": {k: len(v) for k, v in layers.items()},
        "directed_counts": directed,
        "setdigest": {k: setdigest([e["pair_uid"] for e in v]) for k, v in layers.items()},
        "mixed_c_in_N_within_L1": mixed,
        "L2_pairs": [
            {"index": e["index"], "pair_uid": e["pair_uid"], "member_uids": e["member_uids"]}
            for e in L2_sorted
        ],
        "uid_scheme": {
            "member_uid": 'sha256("|".join(canonical_id_words))[:12]',
            "pair_uid": 'sha256(f"{index}#{chr(35).join(sorted([m0,m1]))}")[:12]',
            "setdigest": 'sha256("|".join(sorted(layer_pair_uids))).hexdigest() (full 64 hex)',
        },
    }
    with open("search/certs/twin_witness_scope1_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("Wrote search/certs/twin_witness_scope1_v1_20260806.json")


if __name__ == "__main__":
    main()
