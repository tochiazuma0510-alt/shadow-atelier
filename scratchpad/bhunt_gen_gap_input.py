#!/usr/bin/env python3
"""Generate the GAP-readable input file (L, pent(m0), anchor c) from the J0
join output (scratchpad/bhunt_j0_output.json), for consumption by
scratchpad/bhunt_j1j2.g. Pure formatting -- no new computation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J0_PATH = ROOT / "scratchpad/bhunt_j0_output.json"
OUT_PATH = ROOT / "scratchpad/bhunt_j0_input.g"

M0 = 1        # generating layer: u0 = 2*1+1 = 3, a generator of (Z/7)^x
C_M = 6       # anchor c = Ih_N(iota) = [6,1] (docs/notes/bhunt_prereg_iffirst_v1.md Sec 2.2)
C_E = [0, 0, 0, 0, 0, 0]  # f_c = 1 (identity of P)


def gap_int_list(xs):
    return "[" + ",".join(str(x) for x in xs) + "]"


def gap_list_of_lists(xss):
    return "[\n  " + ",\n  ".join(gap_int_list(xs) for xs in xss) + "\n]"


def main():
    d = json.load(open(J0_PATH, encoding="utf-8"))
    if d["pent_per_layer_counts"]["0"] != 7:
        raise SystemExit(f"expected |L|=7, got {d['pent_per_layer_counts']['0']}")
    if d["pent_per_layer_counts"][str(M0)] != 7:
        raise SystemExit(f"expected |pent({M0})|=7, got {d['pent_per_layer_counts'][str(M0)]}")
    L_EVECS = d["L_m0"]
    PENT_M1_EVECS = d["pent_m1"]

    lines = []
    lines.append("## scratchpad/bhunt_j0_input.g -- GENERATED from scratchpad/bhunt_j0_output.json")
    lines.append("## by scratchpad/bhunt_gen_gap_input.py. Pure formatting of the J0 join result")
    lines.append("## (scratchpad/bhunt_j0_join.py, streamed from the existing S/V/P lane artifacts).")
    lines.append("## No new window computation happens in this file or its generator.")
    lines.append(f"L_EVECS := {gap_list_of_lists(L_EVECS)};;")
    lines.append(f"PENT_M1_EVECS := {gap_list_of_lists(PENT_M1_EVECS)};;")
    lines.append(f"M0 := {M0};;")
    lines.append(f"C_M := {C_M};;")
    lines.append(f"C_E := {gap_int_list(C_E)};;")
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
