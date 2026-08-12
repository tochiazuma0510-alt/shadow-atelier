"""[I-SET-4 / 検算B'] cert iset4_remeasure_v1_20260813 からの導出量(裁定1103: 数値は機械生成)."""
import json, io
d = json.load(io.open('search/certs/iset4_remeasure_v1_20260813.json', encoding='utf-8'))
b0 = d['b_prime_0_base_quantities']; sc = d['b_prime_1_2_scan']; w = d['window']
h = sc['pattern_histogram_csh_bitindex_1to8']          # index = C*4+S*2+H+1
n = w['shadow_total']
lab = {i: ('C' if (i-1)>>2 & 1 else 'c') + ('S' if (i-1)>>1 & 1 else 's') + ('H' if (i-1) & 1 else 'h')
       for i in range(1, 9)}
print(f"window {w['id']} slot{w['slot']}  shadows={n}  |Q|={b0['q_size']}  |PN|={b0['pn_full_size']}")
print(f"  z = ord(c-bar) = {w['z_order_of_c']}   z0 = [PN:Q] = {b0['z0_index_pnfull_over_q']}"
      f"   -> z0 | z, z0 != z : {b0['z0_index_pnfull_over_q'] != w['z_order_of_c']}")
print(f"  |[Q,Q]| = {b0['dcomm_size']}  |D1 = C_Q(s1)| = {b0['d1_size']}  |D0 = D1 cap [Q,Q]| = {b0['d0_size']}")
print(f"  total trials = {sc['total_trials']} = {n} x {b0['q_size']} : {sc['total_trials'] == n*b0['q_size']}")
print("\n  (C,S,H) pattern            count   per-shadow")
for i in range(1, 9):
    print(f"    {lab[i]:5s} idx{i}            {h[i-1]:6d}   {h[i-1]/n:8.3f}")
surv = h[7]; hexonly = h[6]; Ctrue = sum(h[4:8]); CS = h[6] + h[7]
print(f"\n  survivors (C,S,H)=TTT        = {surv}  = {surv//n}/shadow   (= N_m, SURV-EXACT)")
print(f"  charming-true total          = {Ctrue} = {Ctrue//n}/shadow  (= |[Q,Q]| = {b0['dcomm_size']} : {Ctrue//n == b0['dcomm_size']})")
print(f"  hexagon-ONLY cut (C,S,~H)    = {hexonly} = {hexonly//n}/shadow")
print(f"  C&S true                     = {CS} = {CS//n}/shadow  -> hexagon cuts {hexonly}/{CS} = {hexonly/CS:.1%}")
print(f"  surjectivity-cut (C,~S,*)    = {h[4]+h[5]} = {(h[4]+h[5])//n}/shadow")
print(f"\n  W1 SURV-EXACT all_uniform    = {d['w1_surv_exact']['all_uniform']}")
print(f"  W2 identity survives         = {d['w2_identity_survives']['all_pass']}")
print(f"  W3 charming regression       = {d['w3_charming_regression']['all_pass']}  violations={d['w3_charming_regression']['violation_count']}")
ds = d['d_separation_indicator']
print(f"\n  D0\{{1}} size = {ds['d0_minus_1_size']} ; hexagon-cut hits = {ds['hit_count']}"
      f" / {ds['d0_minus_1_size']*n} possible -> {ds['hit_count']/(ds['d0_minus_1_size']*n):.0%}")
print(f"  => Surv(t) cap D1 = {{1}} for all t : {ds['hit_count'] == ds['d0_minus_1_size']*n}")
print(f"\n  K9 positive control : {d['k9_positive_control']['status']}")
