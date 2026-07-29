#!/usr/bin/env python3
"""
search/strike-witness-recheck-a20.py -- independent python-only (sympy)
recheck of the W-D-A20-15a witness (search/certs/strike_a20_full_20260729.json:
m1=0, f1=(11,14)(18,19); m2=0, f2=(2,11)(6,14)(16,19)(17,18)), against the B3
window generators machine-transcribed in search/strike-a20.g (JUDGE_S1_IMG_SLATE
/ JUDGE_S2_IMG_SLATE, 23 points, A20 factor on points 1..20).

Uses search/strike_witness_common.py (the generalized A16 engine). No GAP
import. No commit. No interpretation beyond what's printed / written.
"""
from strike_witness_common import run_window

s1_cycles = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],[16,17],[18,19],[21,22]]
s2_cycles = [[1,9,8,15,19,13,12,18,10,7,16,5,20,3,17],[2,6],[11,14],[22,23]]

f1_cycles = [[11,14],[18,19]]
f2_cycles = [[2,11],[6,14],[16,19],[17,18]]

run_window(
    window_label="W-D-A20-15a",
    s1_cycles=s1_cycles,
    s2_cycles=s2_cycles,
    degree=23,
    f1_cycles=f1_cycles,
    f2_cycles=f2_cycles,
    n_alt=20,
    alt_order=1216451004088320000,  # |A20| = 20!/2
    outpath="search/certs/strike_a20_witness_recheck_20260729.json",
    source_certificate="search/certs/strike_a20_full_20260729.json",
    source_generators="search/strike-a20.g JUDGE_S1_IMG_SLATE/JUDGE_S2_IMG_SLATE (23 points)",
)
