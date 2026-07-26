#############################################################################
# search/kummer-cov3-actual.g -- 第三 covariance(GAP 側・第一系統)v1
# 委嘱: 便 36(裁定 36_ben35)。Sol 便 35 F3(blocker 4)の指摘により、旧
# search/kummer-decide.g の KummerCovariance3Check(Gal(K/Q) の GaloisCyc
# 作用を検査していた・撤回済み)を、K3 fixture の**実値** rho_0・tau・j
# を使う較正へ作り直す。
#
# *** 射程の限定(重要・司令塔へ明記する UNKNOWN 事項) ***
# Sol の要求(sol_reply_35_freeze1r4.md F3)は「b_i と Kummer character
# exponent を同時に変換し (5') 相当の等式と formal a=1 の不変性を検査する」
# である。本スクリプトが実装できるのは以下のみ:
#   - rho_0(F0 の生成元) と tau(mu_M[e] の生成元) の実値(fixture の
#     tau_rho0_j_orientation ブロック)から j: mu_M[e] -> F0 を再構成し、
#     生成元の取り替え zeta_M[e] -> zeta_M[e]^{d'} (d' in (Z/e)^x) の下で
#     j の対応表が transformation law t' = d'^{-1} t (mod e) のとおりに
#     書き換わることを、置換の実値等式として検査する。
# 実装**できない**もの(UNKNOWN として申告・司令塔へ差し戻す):
#   - b_i(Rule 1 S7.1: 実際の局所モノドロミー生成元 ell_i と intertwiner
#     c_i から測る量)の独立測定値。K3 の tau は s^{1/M} -> zeta_M s^{1/M}
#     という局所 Kummer 規約から**直接定義**されており
#     (docs/week4-K3飽和_opus_v3.md S5.2.0)、この構成では b=1 は定義上の
#     ものであって、Rule 1 S7.4 が要求する「独立に計算して記録する」対象の
#     実測値ではない。intertwiner c_i の明示的な計算(FC-3)は本 campaign の
#     証明書に載っていない。
#   - formal a(= K5 の sq/ns 比較指数、Rule 1 (1.11))。K3 単体の dessin
#     には定義されない量なので、本追補では独立に再導出しない
#     (K5 側の a=1 は既に permanent invariant として別途固定済み)。
#
# 入力(すべて certificates/k5fixture/K3-regression.json
# tau_rho0_j_orientation ブロックからの転記・出所は docs/manifest_k5_appendixA_v1.md
# の表と一致):
#   rho_0(Phi_{0,0}) = id, rho_0(Phi_{0,1}) = k1, rho_0(Phi_{0,2}) = k2
#   tau_2 (= tau(zeta_6^2), mu_6[3] の一つの生成元) = k2 (fixture の cited 値)
#   e = 3 (F0 = mu_6[3] の位数), M = 6
#
# 実行: .\gap.ps1 search\kummer-cov3-actual.g
#############################################################################

Read("search/gaplib_common.g");

ToPerm := function(list0)
  return PermList(List(list0, x -> x + 1));
end;;

# ---- fixture data (出所: certificates/k5fixture/K3-regression.json
#      .tau_rho0_j_orientation.rho0_images_one_line_0indexed / .tau_generator_action)
rho0 := rec(
  k0 := ToPerm([0,1,2,3,4,5]),
  k1 := ToPerm([1,2,0,4,5,3]),
  k2 := ToPerm([2,0,1,5,3,4])
);;
tau2_fixture := ToPerm([2,0,1,5,3,4]);;   # cited: tau(zeta_6^2)
e := 3;;  M := 6;;

totalPass := 0;; totalFail := 0;;
Check := function(name, ok, extra)
  if ok then totalPass := totalPass + 1; else totalFail := totalFail + 1; fi;
  if ok then Print("[PASS] ", name, "  ", extra, "\n");
  else Print("[FAIL] ", name, "  ", extra, "\n"); fi;
end;;

# -- sanity: fixture's cited tau_2 literally equals rho0(k2) (this equality
# is itself the content of j(tt=1)=2 in the fixture's j_table -- re-verify
# rather than assume).
Check("SANITY tau_2 (fixture) = rho0(Phi_{0,2})", tau2_fixture = rho0.k2, "");

# -- reconstruct tau on the full order-3 subgroup {0,2,4} (exponents of
# zeta_6) using ONLY the homomorphism property tau_{a+b mod 6} = tau_a * tau_b
# (Rule 1 (1.3)/(1.4): tau_i is a homomorphism) plus the single cited value
# tau_2. This is not an invented fact -- it is the defining property of tau
# as a homomorphism, applied to derive tau_4 = tau_2^2 and tau_0 = id.
tau0 := ();;
tau2 := tau2_fixture;;
tau4 := tau2 * tau2;;   # tau_{2+2 mod 6} = tau_4, by the homomorphism property

Check("DERIVE tau_0 = id", tau0 = rho0.k0, "");
Check("DERIVE tau_4 = tau_2^2 = rho0(Phi_{0,1}) (matches fixture j_table tt2->k=1)",
      tau4 = rho0.k1, Concatenation("tau_4 = ", String(List([1..6], i -> i^tau4 - 1))));

# -- baseline table T: exponent (0,2,4 -- i.e. t=0,1,2 with exponent=2t) -> k
# such that rho0(Phi_{0,k}) = tau_{2t mod 6}. Reconstructed purely from raw
# permutation equality (not copied from the fixture's j_table -- this IS an
# independent recomputation of that table from rho0/tau raw data).
baseTauByT := [tau0, tau2, tau4];;   # index t=0,1,2 -> tau_{2t mod 6}
rho0ByK := [rho0.k0, rho0.k1, rho0.k2];;

FindK := function(target)
  local k;
  for k in [0..2] do
    if rho0ByK[k+1] = target then return k; fi;
  od;
  return fail;
end;;

baseJTable := List([0..2], t -> FindK(baseTauByT[t+1]));;
Print("baseJTable (t -> k, independently recomputed from rho0/tau raw data) = ", baseJTable, "\n");
Check("baseJTable matches fixture j_table (tt0:0, tt1:2, tt2:1)",
      baseJTable = [0,2,1], Concatenation("got ", String(baseJTable)));

# -- covariance test: for d' in (Z/e)^x = (Z/3)^x = {1,2}, replace the chosen
# generator zeta_6^2 of mu_6[3] by (zeta_6^2)^{d'} = zeta_6^{2 d' mod 6}, and
# rebuild the j-table INDEPENDENTLY from the new generator's powers (not by
# copying/relabelling the old table). Then check it against the
# transformation law t' = d'^{-1} t (mod e), evaluated on the OLD table.
unitsModE := Filtered([1..e-1], x -> Gcd(x, e) = 1);;
covarianceResults := [];;
for dprime in unitsModE do
  newGen := baseTauByT[(( (2*dprime) mod 6 ) / 2) + 1];   # tau_{2*dprime mod 6}; safe since 2*dprime mod 6 is even for dprime in {1,2}
  # independently rebuild table T'[t'] := k such that rho0(Phi_{0,k}) = (newGen)^{t'}
  newTauByT := List([0..2], tprime -> newGen^tprime);
  newJTable := List([0..2], tprime -> FindK(newTauByT[tprime+1]));
  dprimeInv := First([1..e], x -> (x*dprime) mod e = 1);
  # transformation law prediction, using the OLD (base) table:
  predictedFromOld := List([0..2], tprime -> baseJTable[ ((dprime*tprime) mod e) + 1 ]);
  matchOk := newJTable = predictedFromOld;
  Add(covarianceResults, rec(dprime := dprime, dprimeInv := dprimeInv,
        newJTable := newJTable, predictedFromOld := predictedFromOld, match := matchOk));
  Check(Concatenation("COV d'=", String(dprime), ": independently rebuilt j'-table = predicted-from-old via t'=d'^{-1}t(modE)... (transformation law t-index correspondence)"),
        matchOk, Concatenation("newJTable=", String(newJTable), " predictedFromOld=", String(predictedFromOld)));
od;;

allCovarianceMatch := ForAll(covarianceResults, r -> r.match);;
Print("\nallCovarianceMatch = ", allCovarianceMatch, "\n");

# -- b (formal, definitional -- NOT independently measured; see header UNKNOWN note)
bFormal := 1;;
bPrimeByDprime := List(unitsModE, dp -> rec(dprime := dp,
  bPrime := (First([1..e], x -> (x*dp) mod e = 1) * bFormal) mod e));;
Print("b (formal/definitional, per header note) = ", bFormal, "\n");
Print("b' = d'^{-1} * b (mod e) for each d': ", bPrimeByDprime, "\n");

Print("\n=== ", totalPass, "/", totalPass + totalFail, " PASS ===\n");

# ---------------------------------------------------------------- certificate
JCovRec := function(r)
  return Concatenation("{",
    JStr("dprime"), ":", String(r.dprime), ",",
    JStr("dprimeInv"), ":", String(r.dprimeInv), ",",
    JStr("newJTable"), ":", JArr(List(r.newJTable, String)), ",",
    JStr("predictedFromOld"), ":", JArr(List(r.predictedFromOld, String)), ",",
    JStr("match"), ":", JB(r.match),
  "}");
end;;

certJson := Concatenation(
  "{",
  "\"schema\":\"k5pipeline/kummer-cov3-actual-gap/v1\",",
  "\"retraction_note\":\"supersedes certificates/k5pipeline/retracted/K3-regression-kummer-cov3.v1.json (search/kummer-decide.g KummerCovariance3Check, retracted per Sol 便35 F3 -- that check applied GaloisCyc / Gal(K/Q) to a witness e in K, which is NOT the Kummer character kappa_w(gamma)=gamma(w^{1/M})/w^{1/M} for gamma in G_K, since e in K is fixed by G_K by definition.\",",
  "\"scope_limitation_UNKNOWN\":\"This certificate implements ONLY the rho_0/tau/j actual-value reparametrization covariance (independently rebuilt j-table under generator change, matching the transformation law t'=d'^{-1}t mod e). It does NOT implement an independently measured b_i (Rule 1 S7.1: requires actual local monodromy generator ell_i and intertwiner c_i, not present as certified data for K3 -- tau is defined directly via the local Kummer convention, so b=1 here is definitional, not measured) and does NOT re-derive formal a=1 (Rule 1 (1.11), a K5 sq/ns-specific quantity, N/A for a single K3 dessin). These two items are reported as UNKNOWN / out of current scope, per instruction not to weaken the predicate.\",",
  "\"e\":", String(e), ",",
  "\"M\":", String(M), ",",
  "\"rho0_k0\":", JArr(List([1..6], i -> String(i^rho0.k0 - 1))), ",",
  "\"rho0_k1\":", JArr(List([1..6], i -> String(i^rho0.k1 - 1))), ",",
  "\"rho0_k2\":", JArr(List([1..6], i -> String(i^rho0.k2 - 1))), ",",
  "\"tau2_fixture\":", JArr(List([1..6], i -> String(i^tau2_fixture - 1))), ",",
  "\"tau2_equals_rho0_k2\":", JB(tau2_fixture = rho0.k2), ",",
  "\"tau4_derived\":", JArr(List([1..6], i -> String(i^tau4 - 1))), ",",
  "\"tau4_equals_rho0_k1\":", JB(tau4 = rho0.k1), ",",
  "\"baseJTable\":", JArr(List(baseJTable, String)), ",",
  "\"baseJTable_matches_fixture\":", JB(baseJTable = [0,2,1]), ",",
  "\"units_mod_e\":", JArr(List(unitsModE, String)), ",",
  "\"covariance_results\":", JArr(List(covarianceResults, JCovRec)), ",",
  "\"all_covariance_match\":", JB(allCovarianceMatch), ",",
  "\"b_formal_definitional\":", String(bFormal), ",",
  "\"formal_a_note\":\"formal a (Rule 1 (1.11), K5 sq/ns-specific) is not applicable to a single K3 dessin; not re-derived here.\",",
  "\"pass\":", String(totalPass), ",",
  "\"fail\":", String(totalFail),
  "}"
);;

WriteFile("certificates/k5pipeline/K3-regression-kummer-cov3-actual.gap.json", certJson);;
Print("wrote certificates/k5pipeline/K3-regression-kummer-cov3-actual.gap.json\n");

if totalFail > 0 then
  Print("*** THERE ARE FAILURES ***\n");
fi;

QUIT;
