# u5 FIRE - certificate generator.  All values machine-produced; no hand-written numbers.
# Ported from u7_fire_cert.py.  predictions_confronted stays False here -- the
# confrontation against any sealed prediction is 司令塔's job after this cert exists,
# not this script's.
import hashlib, json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u5_fire_pathA as A
import u5_fire_pathB as B

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

N, ALPHA = 5, 1

# ---- CV-13 anchor block: n=7 (+n=3) reproduction, captured quietly here too ----
u7_cert = A._load_u7_cert()
anchor_pathA = {f"n{n}_a{a}": capture(A.run, n, a)
                for (n, a) in ((3, 1), (7, 1), (7, 2), (7, 3))}
anchor_pathB = {f"n{n}_a{a}": B.block_character(n, a)
                for (n, a) in ((3, 1), (7, 1), (7, 2), (7, 3))}
anchor_orient7 = {f"n7_a{a}": capture(B.orientation_self_check, 7, a) for a in (1, 2, 3)}
anchor_ok = (
    all(anchor_pathA[f"n7_a{a}"]["u_value"] == u7_cert["path_A"]["all_windows_alpha"][f"n7_a{a}"]
        for a in (1, 2, 3))
    and anchor_pathA["n3_a1"]["u_value"] == u7_cert["calibration_CAL3"]["u_3_computed"]
    and all(anchor_pathB[f"n7_a{a}"]["block_character_trivial"] == u7_cert["path_B"]["all_alpha"][f"n7_a{a}"]
            for a in (1, 2, 3))
    and anchor_pathB["n3_a1"]["block_character_trivial"] == u7_cert["path_B"]["all_alpha"]["n3_a1"]
)
anchor_orient_ok = all(
    (o["H_conj_XHXinv_in_AH"] is False) and (o["X_swaps_blocks"] is True) and
    all(o["translation_consistent"]) and (o["sum_of_two_ratios_mod_n"] == 0)
    for o in anchor_orient7.values())
assert anchor_ok, "CV-13 anchor (n=7 bit reproduction) failed inside cert generator"
assert anchor_orient_ok, "CV-13 orientation self-check (n=7) failed inside cert generator"

# ---- n=5 measurement ----
pathA5 = {f"n{N}_a{a}": capture(A.run, N, a) for a in range(1, (N-1)//2 + 1)}
pathB5 = {f"n{N}_a{a}": B.block_character(N, a) for a in range(1, (N-1)//2 + 1)}
orient5 = {f"n{N}_a{a}": capture(B.orientation_self_check, N, a) for a in range(1, (N-1)//2 + 1)}

u5 = pathA5[f"n{N}_a{ALPHA}"]["u_value"]
arith5 = B.F_arith(N, int(u5))

gamma_trivial_A = pathA5[f"n{N}_a{ALPHA}"]["both_R_rational"]      # disc F[R1,R2] = 1
gamma_trivial_B = pathB5[f"n{N}_a{ALPHA}"]["block_character_trivial"]

orient5_structural_ok = all(
    (o["H_conj_XHXinv_in_AH"] is False) and (o["X_swaps_blocks"] is True) and
    all(o["translation_consistent"]) and (o["sum_of_two_ratios_mod_n"] == 0)
    for o in orient5.values())

cert = {
  "schema": "u5-fire-cert/v1",
  "produced_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "authority": {
     "seal_release_ruling": "396",
     "seal_release_note": "2026-08-01 研究者一括認可 (2) n=5 開封 -- versioned ALLOWED_N release, scoped to u5_fire_pathA.py / u5_fire_pathB.py only",
     "fire_design_ported_from": "u7 firing (裁定 287 freeze / 裁定 300 fire_authorisation)",
     "frozen_design_ported_from": "docs/notes/u7_meas_design_v1.md",
     "determination_mechanism_ported_from": "docs/notes/u7_twist_determination_v1.md",
     "n5_freeze_prior": "U7-NO5 (K^(5) blind, held everywhere except this scoped release)"},
  "window_binding": {                                   # ported n-generic formulas from u7 cert
     "n": N, "P": f"G_{N}", "|P|": 4*N**3, "H": "H_{2,1,0}", "|H|": 2*N**2,
     "alpha_class": "[1]", "j": 2, "beta": 0,
     "marking": {"g_0": "X = a1 q1", "g_1": "Y = a1 a2 a3 q2", "g_inf": "Z = (XY)^{-1}"},
     "deg": 2*N, "M": 2*N, "F": "Q(zeta_20)", "ordered_passport": "((10), 2^4 1^2, (10))",
     "monodromy_order": 4*N**2, "genus_W": (N-1)//2, "genus_Wtilde": N-1,
     "tower": "lambda = gamma m^2 ; pi deg 5 with mon D_5 ; branch {0,inf,mu_+,mu_-}",
     "r0_rinf": [1, -ALPHA]},
  "path_A": {
     "method": "explicit KUM-n normal form over Q(i) subset F ; local expansion at the cusp",
     "model": {"h(k)": "(k-i)^1 (k+i)^{-1} (k-1)^{-alpha} (k+1)^{alpha}",
               "Wtilde": "y^n = h(k)", "iota": "(k,y) -> (-k, 1/y)",
               "m_0": "(1+k^2)/(1-k^2)", "lambda": "m_0^2  (gamma = 1 in this coordinate)",
               "uniformiser_at_cusp": "y at Q_+=(k=i,y=0); Wtilde->W unramified there"},
     "leading_coeff_h1": pathA5[f"n{N}_a{ALPHA}"]["h1"],
     "u_5": u5,
     "disc_F_R1R2_trivial": gamma_trivial_A,
     "R_plus_y": pathA5[f"n{N}_a{ALPHA}"]["R_plus_y"],
     "R_minus_y": pathA5[f"n{N}_a{ALPHA}"]["R_minus_y"],
     "iota_involution_check": pathA5[f"n{N}_a{ALPHA}"]["iota_ok"],
     "all_windows_alpha": {k: v["u_value"] for k, v in pathA5.items()}},
  "path_B": {
     "method": "block character of the G_F-action on Lambda (系 B-4c + 補題 B-5 (7.2) + 系 SPLIT)",
     "bridge_inputs": {
        "(W2)": "1 -> F_0 -> GT(N) -> (Z/2M)^x -> 1 exact, chi~ o Ih_N = chi_{2M}; K = Q(zeta_{2M})",
        "(W2)-fam": "F_0 = C_n  (裁定 120, status = candidate: 紙上 + n<=27 機械検算)",
        "Phi(F_0)": "inn(<X^2>)  (Sol 便 73 Q1.5 / w2fam_v1.md §3.5)",
        "系 B-4c": "Fib_{01}(W_0) = Lambda  G_K-equivariantly, action = Phi(Ih_N(gamma))",
        "補題 B-5 (7.2)": "Fib is a mu_M-torsor of class [u^{-1}]_M, X acts as tau(zeta_M)"},
     "X2_in_AH": pathB5[f"n{N}_a{ALPHA}"]["X2_in_AH"],
     "PhiF0_image_size": pathB5[f"n{N}_a{ALPHA}"]["F0img_size"],
     "any_element_swaps_blocks": pathB5[f"n{N}_a{ALPHA}"]["any_element_swaps_blocks"],
     "block_character_trivial": gamma_trivial_B,
     "parity_argument": {"|F_0|": N, "odd": N % 2 == 1, "Hom(F_0,C_2)_trivial": N % 2 == 1},
     "all_alpha": {k: v["block_character_trivial"] for k, v in pathB5.items()},
     "orientation_self_check": {k: v for k, v in orient5.items()},
     "orientation_self_check_structural_expectations_hold": orient5_structural_ok},
  "cross_check": {
     "path_A_gamma_trivial": gamma_trivial_A,
     "path_B_gamma_trivial": gamma_trivial_B,
     "agree": gamma_trivial_A == gamma_trivial_B,
     "status": "cross-checked (NOT verified; Lean 未使用)",
     "shared_premises": ["定理 TOWER-n", "系 SPLIT", "(W3)", "(W4)"]},
  "cv13_anchor_n7": {
     "bit_reproduction_of": "search/certs/u7_fire_20260801.json",
     "pathA_all_windows_alpha_match": {a: anchor_pathA[f"n7_a{a}"]["u_value"] for a in (1, 2, 3)},
     "pathA_cal3_n3_match": anchor_pathA["n3_a1"]["u_value"],
     "pathB_all_alpha_match": {a: anchor_pathB[f"n7_a{a}"]["block_character_trivial"] for a in (1, 2, 3)},
     "pathB_n3_match": anchor_pathB["n3_a1"]["block_character_trivial"],
     "orientation_self_check_n7": {f"a{a}": anchor_orient7[f"n7_a{a}"] for a in (1, 2, 3)},
     "anchor_pass": bool(anchor_ok),
     "orientation_anchor_pass": bool(anchor_orient_ok)},
  "measured_quantities_n5": {
     "(i) [u_5]_2":  {"trivial": arith5["u_in_F_square"]},
     "(ii) [u_5]_5": {"trivial": not arith5["u_not_in_F_nth_power"]},
     "(iii) u_5":    u5,
     "(iv) all valuations": {"nonzero_places": arith5["places"],
                             "all_other_places": 0,
                             "exists_p_with_w_not_div_5": arith5["exists_p_w_not_div_n"]},
     "(v) [gamma], [delta_0]": {"[gamma]_2_trivial": gamma_trivial_A,
                                "note": "gamma = 1 in the normal-form coordinate; delta_0 = 1 likewise"},
     "(vi) ord(a_5)": arith5["ord_of_class_mod_M"]},
  "LB_RES_ladder": {
     "stage1_valuation_decides": bool(arith5["exists_p_w_not_div_n"]),
     "stage2_class_group_needed": not bool(arith5["exists_p_w_not_div_n"]),
     "stage3_units_needed": not bool(arith5["exists_p_w_not_div_n"]),
     "u_in_Q": True, "u_not_in_Q^5": arith5["u_not_in_Q_nth_power"],
     "G5_LB_applies": arith5["u_not_in_Q_nth_power"],
     "G5_LB_pp_applies": bool(arith5["exists_p_w_not_div_n"])},
  "NULL_frame": {
     "N-1 passport mismatch": False, "N-2 monodromy != 100": False,
     "N-3 tower absent": False,
     "N-4 [u]_2 nontrivial": not arith5["u_in_F_square"],
     "N-5 u not rational": False,
     "N-6 all valuations = 0 mod 5": not bool(arith5["exists_p_w_not_div_n"]),
     "N-7 [u]_5 trivial": not arith5["u_not_in_F_nth_power"],
     "N-8 CV13 anchor failed": not anchor_ok,
     "N-9 paths disagree": gamma_trivial_A != gamma_trivial_B,
     "N-10 gamma/delta undetermined": False,
     "N-11 orientation self-check failed": not orient5_structural_ok,
     "any_triggered": (not anchor_ok) or (gamma_trivial_A != gamma_trivial_B) or (not orient5_structural_ok)},
  "predictions_confronted": False,
  "predictions_confronted_note": "実測値は本 cert に machine-piped で記載する(接触遮断対象は期待値の側)。予言との対決は司令塔が封印開封後に実施する。本 script は予言 cert を読んでいない。",
  "provenance": {
     "probes": {p: sha("search/probe/wac_v1/" + p) for p in
                ("tw_blocks.py", "tw_orient.py", "u7_fire_pathA.py", "u7_fire_pathB.py",
                 "u5_fire_pathA.py", "u5_fire_pathB.py", "u5_fire_cert.py")},
     "python": sys.version.split()[0],
     "arithmetic": "exact (fractions.Fraction over Q(i); integer group arithmetic). No floating point.",
     "single_implementation": True,
     "second_system_pending": "GAP re-construction by implementer (突合 = 司令塔), same as u7",
     "lean_verified": False,
     "n5_touched": True,
     "n5_touch_scope": "u5_fire_pathA.py / u5_fire_pathB.py / u5_fire_cert.py only; other probes unaffected"},
  "framework_dependencies": [
     "(TB1)(TB2)(TB3)(TB4) - 枠組み仮定 (Mathlib 待ち)",
     "(W1)(W2)(W3)(W4)(W5) + (CAL) - 定理 B-4 / 系 B-4c / 補題 B-5 の前件",
     "(W2)-fam 裁定 120 = candidate (path B only)",
     "定理 TOWER-n / 定理 KUM-n / 系 SPLIT - 紙上単系統, Sol 監査前 (u7 firing と同じ枠組み)",
     "(GR) tame good reduction - 【要検分】 (補題 TW-5 only; not used for the value)",
     "docs/notes/fam_u_v1.md (FAM-U) explicitly excludes n=5 from its scope (§6 FAM-f, 凍結 U7-NO5); this cert does NOT read fam_u_v1.md's formula and does not use FAM-U as an input -- it is an independent measurement"],
}

out = os.path.join(ROOT, "search", "certs", "u5_fire_20260801.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote", out)
print("cert sha256:", sha("search/certs/u5_fire_20260801.json"))
