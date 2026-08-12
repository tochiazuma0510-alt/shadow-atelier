# search/q3_m1_v1.g -- [Q3-M1] 候補宇宙のu制限の判定(裁定1064)
#
# 正本: docs/notes/q3_decision_design_v1.md §4。
# 判定: sigma_1^u(u notin {+-1})が「(位数3元)^-1・(位数2元)」の積の形で書けるか。
#   1個でもYES ⟹ 非isolated確定。全NO(サンプル内) ⟹ (M2)へ(未証明のまま)。
#
# 実装方針(exact witness search, s2_3_pre_gen23_v1.gと同型の設計): 位数3の共役類は
#   det=1・trace=-1(1+omega+omega^2=0)で単一(3|690より split)。位数3の代表元
#   B0=diag(omega,omega^-1)(omega=Z/691^2の原始3乗根、mod691の値をTeichmuller冪で
#   リフト)を乱択共役 v'=g*B0*g^-1 でサンプルし、各uについて u':=v'*sigma1^u を計算、
#   (u')^2=I かつ u'<>I(=位数ちょうど2)を厳密判定。見つかれば決定的witness(存在証明)。
#   見つからなければ「サンプル内でNOT FOUND」として正直に報告(存在しない証明ではない)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

p := 691;;
p2 := p^2;;
Zp2 := Integers mod p2;;

# ---- reconstruct sigma1 exactly as in q3_r1_lift_v1.g ----
ahat := [[483,28],[59,208]] * One(Zp2);;
bhat := [[245,158],[69,445]] * One(Zp2);;
DetMod := function(M) return M[1][1]*M[2][2] - M[1][2]*M[2][1];; end;;
detA := DetMod(ahat);;  detB := DetMod(bhat);;
lamA := -(detA^-1);;  lamB := detB^-1;;
DiagMod := function(d1, d2) return [[d1, Zero(Zp2)], [Zero(Zp2), d2]];; end;;
a0 := DiagMod(lamA, One(Zp2)) * ahat;;
b0 := DiagMod(lamB, One(Zp2)) * bhat;;
atilde := a0^p;;
btilde := b0^p;;
sigma1 := btilde^-1 * atilde;;
sigma2 := atilde * btilde^2;;
Print("sigma1 (再構成) = ", List(sigma1, r -> List(r, Int)), "\n");
Print("(期待 [[158625,469515],[262365,86342]])\n");
sigma1Ok := (sigma1 = [[158625,469515],[262365,86342]]*One(Zp2));;
Print("[", PF(sigma1Ok), "] sigma1 再構成一致: ", sigma1Ok, "\n");
if not sigma1Ok then
  Error("q3_m1_v1: sigma1 reconstruction mismatch -- refusing to proceed");
fi;

xbar := sigma1^2;;
ybar := sigma2^2;;
Nord := 47679;;
Print("N_ord = ", Nord, "\n");

# ---- canonical order-3 element B0 = diag(omega, omega^-1) mod 691^2 (Teichmuller lift) ----
Zp := Integers mod p;;
omegaP := fail;;
for cand in Elements(Zp) do
  if cand <> Zero(Zp) and cand^3 = One(Zp) and cand <> One(Zp) then omegaP := cand; break;; fi;
od;
if omegaP = fail then Error("no primitive cube root mod 691"); fi;
Print("omega mod 691 = ", Int(omegaP), "\n");
omegaHat := Int(omegaP) * One(Zp2);;
omegaTilde := omegaHat^p;;   # Teichmuller lift to mod 691^2
Print("omega mod 691^2 (Teichmuller) = ", Int(omegaTilde), "\n");
omegaCheck := (omegaTilde^3 = One(Zp2));;
Print("[", PF(omegaCheck), "] omega_tilde^3 == 1 (mod 691^2): ", omegaCheck, "\n");
if not omegaCheck then Error("Teichmuller cube root lift failed"); fi;

B0 := DiagMod(omegaTilde, omegaTilde^-1);;
b0Order3check := (B0^3 = IdentityMat(2,Zp2)) and (B0 <> IdentityMat(2,Zp2));;
Print("[", PF(b0Order3check), "] B0 has order exactly 3: ", b0Order3check, "\n");

# ---- witness search: for each charming u (excluding +-1), sample conjugates of B0,
#      check if v' * sigma1^u has order exactly 2 ----
IdMod := IdentityMat(2, Zp2);;

RandomInvertibleMatMod := function(ring)
  local M, det, tries;
  tries := 0;;
  repeat
    M := RandomMat(2, 2, ring);;
    det := DeterminantMat(M);;
    tries := tries + 1;;
  until (det <> Zero(ring) and Gcd(Int(det), p) = 1) or tries > 1000;
  return M;;
end;;

HasOrderExactly2 := function(M)
  return (M*M = IdMod) and (M <> IdMod);;
end;;

charmingU := Filtered([1..Nord-1], uu -> Gcd(uu, Nord) = 1);;
targetUs := Filtered(charmingU, uu -> uu <> 1 and uu <> Nord-1);;
Print("charming u total = ", Length(charmingU), " ; targets (u notin {+-1}) = ", Length(targetUs), "\n");

seed := 20260813;;
Reset(GlobalMersenneTwister, seed);;
SAMPLES_PER_U := 8;;
t0 := GAPLIB_WallElapsedMs();;

witnessFound := fail;;
uTried := 0;;
for uu in targetUs do
  uTried := uTried + 1;;
  Mu := sigma1^uu;;
  found := false;;
  for s in [1..SAMPLES_PER_U] do
    g := RandomInvertibleMatMod(Zp2);;
    vprime := g * B0 * g^-1;;
    uprime := vprime * Mu;;
    if HasOrderExactly2(uprime) then
      witnessFound := rec(u := uu, g := g, vprime := vprime, uprime := uprime, sample := s);;
      found := true;;
      break;;
    fi;
  od;
  if found then break; fi;
  if uTried mod 5000 = 0 then
    Print("  progress: tried ", uTried, "/", Length(targetUs), " (", GAPLIB_WallElapsedMs()-t0, "ms)\n");
  fi;
od;
t1 := GAPLIB_WallElapsedMs();;

Print("\nu values tried = ", uTried, " / ", Length(targetUs), "\n");
Print("elapsed_ms = ", t1-t0, "\n");

# ====================================================================
# 補強: 1パラメータ族での全数探索(統計的サンプリングの弱さを補う、より強い決定的探索)
# g_s := [[1,s],[0,1]]  (s in Z/691^2, 全477481値) を conjugator として v'=g_s B0 g_s^-1 を
# 網羅し、代表的な u の少数サンプルについて trace(v'*Mu) が目標trace(-2 or 0)を
# 達成するかを全数判定する(乱択8回よりはるかに強い検出力・ただし全30358uには及ばない
# ことを正直に申告)。
# ====================================================================
exhaustiveWitness := fail;;
exhaustiveUsChecked := [];;
if witnessFound = fail then
  Print("\n=== 補強探索: 1パラメータ族(477481値)での代表u全数チェック ===\n");
  repU := List([0..14], k -> targetUs[1 + Int(k * (Length(targetUs)-1) / 14)]);;
  Print("代表u = ", repU, "\n");
  t2 := GAPLIB_WallElapsedMs();;
  for uu in repU do
    Mu := sigma1^uu;;
    Add(exhaustiveUsChecked, uu);;
    hitFound := false;;
    for s in [0..p2-1] do
      gs := [[One(Zp2), s*One(Zp2)], [Zero(Zp2), One(Zp2)]];;
      vprime := gs * B0 * gs^-1;;
      uprime := vprime * Mu;;
      if HasOrderExactly2(uprime) then
        exhaustiveWitness := rec(u := uu, s := s, vprime := vprime, uprime := uprime);;
        hitFound := true;;
        break;;
      fi;
    od;
    Print("  u=", uu, ": 1パラメータ全数(", p2, "値)チェック -- hit=", hitFound, "\n");
    if hitFound then break; fi;
  od;
  t3 := GAPLIB_WallElapsedMs();;
  Print("補強探索 elapsed_ms = ", t3-t2, " (代表u数=", Length(exhaustiveUsChecked), ")\n");
fi;

status := "NOT_FOUND_IN_SAMPLE";;
if witnessFound = fail and exhaustiveWitness <> fail then
  witnessFound := exhaustiveWitness;;
fi;
if witnessFound <> fail then
  status := "POSITIVE_WITNESS_FOUND";;
  Print("\n*** POSITIVE WITNESS FOUND: u=", witnessFound.u, " ***\n");
  Print("v' = ", List(witnessFound.vprime, r -> List(r, Int)), "\n");
  Print("u' = v' * sigma1^u = ", List(witnessFound.uprime, r -> List(r, Int)), "\n");
  Print("check (u')^2 = I: ", witnessFound.uprime^2 = IdMod, "\n");
  Print("==> [Q3-M1] YES: hexagon solvable for u notin {+-1} ==> NON-ISOLATED confirmed (via this witness)\n");
else
  Print("\n status = NOT_FOUND_IN_SAMPLE (", SAMPLES_PER_U, " samples per u, ", Length(targetUs),
        " u values) -- NOT a proof of absence, only a negative result within this sample budget.\n");
  Print("==> [Q3-M1] inconclusive at this sample depth -- (M2) remains open per design doc.\n");
fi;

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_q3m1.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

MatJson := function(M)
  return Concatenation("[[", String(Int(M[1][1])), ",", String(Int(M[1][2])), "],[",
                        String(Int(M[2][1])), ",", String(Int(M[2][2])), "]]");
end;;

scriptSha256 := ComputeSha256File("search/q3_m1_v1.g");;

witnessJson := "null";;
if witnessFound <> fail then
  witnessSourceStr := "random_sample";;
  if IsBound(witnessFound.s) then witnessSourceStr := "exhaustive_1param"; fi;
  witnessJson := Concatenation("{\"u\":", String(witnessFound.u),
    ",\"source\":\"", witnessSourceStr, "\"",
    ",\"v_prime\":", MatJson(witnessFound.vprime),
    ",\"u_prime\":", MatJson(witnessFound.uprime), "}");
fi;

cert := Concatenation(
  "{\"schema\":\"q3_m1/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/q3_m1_v1.g\",\"order\":\"裁定1064 [Q3-M1] / docs/notes/q3_decision_design_v1.md §4\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"method\":\"exact witness search: v' = random conjugate of canonical order-3 element B0; check if v'*sigma1^u has order exactly 2, for each u notin {+-1}\"",
  ",\"N_ord\":", String(Nord),
  ",\"charming_total\":", String(Length(charmingU)),
  ",\"target_u_count\":", String(Length(targetUs)),
  ",\"samples_per_u\":", String(SAMPLES_PER_U),
  ",\"random_seed\":", String(seed),
  ",\"u_values_tried\":", String(uTried),
  ",\"statistical_power_caveat\":\"重要: この乱択サンプリング(1 uあたり", String(SAMPLES_PER_U),
    "回)は統計的検出力が低い可能性がある。SL2のFricke指標多様体理論(古典的事実: 固定した",
    "trace(v')=-1・trace(M)=一定に対し、v'がその共役類全体を動くとき tr(v'M) は(退化例外を",
    "除き)Z/691^2の値をほぼ一様にカバーしうる)が正しければ、目的のtraceに一致する乱択",
    "サンプルの的中確率は概ね 2/691^2 ~ 8.8e-6 程度と推定され、1uあたり", String(SAMPLES_PER_U),
    "回のサンプルでは期待的中数が0に近い。したがってこの run のNOT_FOUND結果は「存在しない",
    "強い証拠」ではなく「この乱択サンプル規模では検出できなかった」という弱い結果である",
    "可能性が高い。より確度の高い判定には(a)1uあたりのサンプル数を大幅増加(~1e5規模)、",
    "または(b)1パラメータ族での全数探索(477481値)等、統計的でなく決定的な探索法への",
    "切替えが必要 -- 実装係の自己申告(後出しなく明記)。\"",
  ",\"exhaustive_1param_check\":{",
    "\"performed\":", JB(Length(exhaustiveUsChecked) > 0),
    ",\"representative_u_count\":", String(Length(exhaustiveUsChecked)),
    ",\"representative_us\":", JArr(List(exhaustiveUsChecked, String)),
    ",\"s_values_per_u\":", String(p2),
    ",\"note\":\"各代表uについてg_s=[[1,s],[0,1]](s=0..477480の全477481値)でv'=g_s*B0*g_s^-1を",
      "網羅し、trace一致による絞り込みなしにHasOrderExactly2を直接判定(乱択よりはるかに強い",
      "決定的検出力・ただし1パラメータ族に限定・全共役類を尽くしていない)\"",
  "}",
  ",\"status\":\"", status, "\"",
  ",\"witness\":", witnessJson,
  ",\"u_touched\":false,\"c_touched\":false,\"prereg_value_computed\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/q3_m1_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
