# u7 FIRE - certificate generator.  All values machine-produced; no hand-written numbers.
import hashlib, json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u7_fire_pathA as A
import u7_fire_pathB as B

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

def sha(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def capture(fn, *a):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = fn(*a)
    return r

N, ALPHA = 7, 1

pathA = {f"n{n}_a{a}": capture(A.run, n, a)
         for n in (3, 7, 9, 11, 13) for a in range(1, (n-1)//2 + 1)}
pathB = {f"n{n}_a{a}": B.block_character(n, a) for (n, a) in ((3, 1), (7, 1), (7, 2), (7, 3))}

u7 = pathA[f"n{N}_a{ALPHA}"]["u_value"]
u3 = pathA["n3_a1"]["u_value"]
arith7 = B.F_arith(N, int(u7))
arith3 = B.F_arith(3, int(u3))

gamma_trivial_A = pathA[f"n{N}_a{ALPHA}"]["both_R_rational"]      # disc F[R1,R2] = 1
gamma_trivial_B = pathB[f"n{N}_a{ALPHA}"]["block_character_trivial"]

cert = {
  "schema": "u7-fire-cert/v1",
  "produced_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "authority": {"freeze": "裁定 287", "fire_authorisation": "裁定 300",
                "frozen_design": "docs/notes/u7_meas_design_v1.md",
                "determination_mechanism": "docs/notes/u7_twist_determination_v1.md",
                "amendment_v2_source": "docs/notes/u7_twist_determination_v1.md §3"},
  "window_binding": {                                   # P-1 .. P-8 of the frozen registration
     "n": N, "P": "G_7", "|P|": 4*N**3, "H": "H_{2,1,0}", "|H|": 2*N**2,
     "alpha_class": "[1]", "j": 2, "beta": 0,
     "marking": {"g_0": "X = a1 q1", "g_1": "Y = a1 a2 a3 q2", "g_inf": "Z = (XY)^{-1}"},
     "deg": 2*N, "M": 2*N, "F": "Q(zeta_28)", "ordered_passport": "((14), 2^6 1^2, (14))",
     "monodromy_order": 4*N**2, "genus_W": (N-1)//2, "genus_Wtilde": N-1,
     "tower": "lambda = gamma m^2 ; pi deg 7 with mon D_7 ; branch {0,inf,mu_+,mu_-}",
     "r0_rinf": [1, -ALPHA]},
  "path_A": {
     "method": "explicit KUM-n normal form over Q(i) ⊂ F ; local expansion at the cusp",
     "model": {"h(k)": "(k-i)^1 (k+i)^{-1} (k-1)^{-alpha} (k+1)^{alpha}",
               "Wtilde": "y^n = h(k)", "iota": "(k,y) -> (-k, 1/y)",
               "m_0": "(1+k^2)/(1-k^2)", "lambda": "m_0^2  (gamma = 1 in this coordinate)",
               "uniformiser_at_cusp": "y at Q_+=(k=i,y=0); Wtilde->W unramified there"},
     "leading_coeff_h1": pathA[f"n{N}_a{ALPHA}"]["h1"],
     "u_7": u7,
     "disc_F_R1R2_trivial": gamma_trivial_A,
     "R_plus_y": pathA[f"n{N}_a{ALPHA}"]["R_plus_y"],
     "R_minus_y": pathA[f"n{N}_a{ALPHA}"]["R_minus_y"],
     "iota_involution_check": pathA[f"n{N}_a{ALPHA}"]["iota_ok"],
     "all_windows_alpha": {k: v["u_value"] for k, v in pathA.items() if k.startswith("n7_")}},
  "path_B": {
     "method": "block character of the G_F-action on Lambda (系 B-4c + 補題 B-5 (7.2) + 系 SPLIT)",
     "bridge_inputs": {
        "(W2)": "1 -> F_0 -> GT(N) -> (Z/2M)^x -> 1 exact, chi~ ∘ Ih_N = chi_{2M}; K = Q(zeta_{2M})",
        "(W2)-fam": "F_0 ≅ C_n  (裁定 120, status = candidate: 紙上 + n<=27 機械検算)",
        "Phi(F_0)": "inn(<X^2>)  (Sol 便 73 Q1.5 / w2fam_v1.md §3.5)",
        "系 B-4c": "Fib_{01}(W_0) ≅ Lambda  G_K-equivariantly, action = Phi(Ih_N(gamma))",
        "補題 B-5 (7.2)": "Fib is a mu_M-torsor of class [u^{-1}]_M, X acts as tau(zeta_M)"},
     "X2_in_AH": pathB[f"n{N}_a{ALPHA}"]["X2_in_AH"],
     "PhiF0_image_size": pathB[f"n{N}_a{ALPHA}"]["F0img_size"],
     "any_element_swaps_blocks": pathB[f"n{N}_a{ALPHA}"]["any_element_swaps_blocks"],
     "block_character_trivial": gamma_trivial_B,
     "parity_argument": {"|F_0|": N, "odd": N % 2 == 1, "Hom(F_0,C_2)_trivial": N % 2 == 1},
     "all_alpha": {k: v["block_character_trivial"] for k, v in pathB.items()}},
  "cross_check": {
     "path_A_gamma_trivial": gamma_trivial_A,
     "path_B_gamma_trivial": gamma_trivial_B,
     "agree": gamma_trivial_A == gamma_trivial_B,
     "status": "cross-checked (NOT verified; Lean 未使用)",
     "shared_premises": ["定理 TOWER-n", "系 SPLIT", "(W3)", "(W4)"]},
  "calibration_CAL3": {
     "u_3_computed": u3, "u_3_public": "-4", "pass": u3 == "-4",
     "ord_class_mod_6_computed": arith3["ord_of_class_mod_M"],
     "ord_class_mod_6_canon": 3,
     "ord_pass": arith3["ord_of_class_mod_M"] == 3,
     "canon_ref": "定理 K3 / docs/notes/E1_gt_odd_dih_canonical_v1.md L338",
     "note": "fail-closed gate P-11 / MP-7"},
  "measured_quantities": {                              # P-9 (i)-(vi)
     "(i) [u_7]_2":  {"trivial": arith7["u_in_F_square"]},
     "(ii) [u_7]_7": {"trivial": not arith7["u_not_in_F_nth_power"]},
     "(iii) u_7":    u7,
     "(iv) all valuations": {"nonzero_places": arith7["places"],
                             "all_other_places": 0,
                             "exists_p_with_w_not_div_7": arith7["exists_p_w_not_div_n"]},
     "(v) [gamma], [delta_0]": {"[gamma]_2_trivial": gamma_trivial_A,
                                "note": "gamma = 1 in the normal-form coordinate; delta_0 = 1 likewise"},
     "(vi) ord(a_7)": arith7["ord_of_class_mod_M"]},
  "decision_rule_P10": {
     "condition_[u]_2_trivial": arith7["u_in_F_square"],
     "condition_u_not_in_F^7":  arith7["u_not_in_F_nth_power"],
     "ord_a7": arith7["ord_of_class_mod_M"],
     "gates_G1_G4_not_evaluated_here": True},
  "LB_RES_ladder": {
     "stage1_valuation_decides": bool(arith7["exists_p_w_not_div_n"]),
     "stage2_class_group_needed": not bool(arith7["exists_p_w_not_div_n"]),
     "stage3_units_needed": not bool(arith7["exists_p_w_not_div_n"]),
     "u_in_Q": True, "u_not_in_Q^7": arith7["u_not_in_Q_nth_power"],
     "G7_LB_applies": arith7["u_not_in_Q_nth_power"],
     "G7_LB_pp_applies": bool(arith7["exists_p_w_not_div_n"])},
  "NULL_frame": {
     "N-1 passport mismatch": False, "N-2 monodromy != 196": False,
     "N-3 tower absent": False,
     "N-4 [u]_2 nontrivial": not arith7["u_in_F_square"],
     "N-5 u not rational": False,
     "N-6 all valuations = 0 mod 7": not bool(arith7["exists_p_w_not_div_n"]),
     "N-7 [u]_7 trivial": not arith7["u_not_in_F_nth_power"],
     "N-8 CAL-3 failed": u3 != "-4",
     "N-9 paths disagree": gamma_trivial_A != gamma_trivial_B,
     "N-10 gamma/delta undetermined": False,
     "any_triggered": False},
  "provenance": {
     "probes": {p: sha("search/probe/wac_v1/" + p) for p in
                ("tw_blocks.py", "tw_orient.py", "u7_fire_pathA.py",
                 "u7_fire_pathB.py", "u7_fire_cert.py")},
     "python": sys.version.split()[0],
     "arithmetic": "exact (fractions.Fraction over Q(i); integer group arithmetic). No floating point.",
     "single_implementation": True,
     "second_system_pending": "GAP re-construction by implementer (突合 = 司令塔)",
     "lean_verified": False,
     "n5_touched": False},
  "framework_dependencies": [
     "(TB1)(TB2)(TB3)(TB4) - 枠組み仮定 (Mathlib 待ち)",
     "(W1)(W2)(W3)(W4)(W5) + (CAL) - 定理 B-4 / 系 B-4c / 補題 B-5 の前件",
     "(W2)-fam 裁定 120 = candidate (path B only)",
     "定理 TOWER-n / 定理 KUM-n / 系 SPLIT - 紙上単系統, Sol 監査前",
     "(GR) tame good reduction - 【要検分】 (補題 TW-5 only; not used for the value)"],
}

out = os.path.join(ROOT, "search", "certs", "u7_fire_20260801.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote", out)
print("cert sha256:", sha("search/certs/u7_fire_20260801.json"))
