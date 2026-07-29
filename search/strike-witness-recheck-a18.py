#!/usr/bin/env python3
"""
search/strike-witness-recheck-a18.py -- independent python-only (sympy)
recheck of the W-D-A18-13a witness (search/certs/strike_a18_full_20260729.json:
m1=0, f1=(3,5)(14,15); m2=0, f2=(2,6,18,9,11)(3,7,16,14,15,10,13,4,8,12,5)),
against the B3 window generators machine-transcribed in search/strike-a18.g
(JUDGE_S1_IMG_SLATE / JUDGE_S2_IMG_SLATE, 21 points, A18 factor on points
1..18).

Uses search/strike_witness_common.py (the generalized A16 engine). No GAP
import. No commit. No interpretation beyond what's printed / written.
"""
from strike_witness_common import run_window

s1_cycles = [[1,2,3,4,5,6,7,8,9,10,11,12,13],[14,15],[16,17],[19,20]]
s2_cycles = [[1,7],[2,16,13,9,12,18,10,8,17,6,14,4,15],[3,5],[20,21]]

f1_cycles = [[3,5],[14,15]]
f2_cycles = [[2,6,18,9,11],[3,7,16,14,15,10,13,4,8,12,5]]

run_window(
    window_label="W-D-A18-13a",
    s1_cycles=s1_cycles,
    s2_cycles=s2_cycles,
    degree=21,
    f1_cycles=f1_cycles,
    f2_cycles=f2_cycles,
    n_alt=18,
    alt_order=3201186852864000,  # |A18| = 18!/2
    outpath="search/certs/strike_a18_witness_recheck_20260729.json",
    source_certificate="search/certs/strike_a18_full_20260729.json",
    source_generators="search/strike-a18.g JUDGE_S1_IMG_SLATE/JUDGE_S2_IMG_SLATE (21 points)",
)
