## search/iset4_bprime_v1.g -- 【検算B'】I-SET-4 座標捻りの再測定(裁定1089・実装係タスクA)
##
## 正本: docs/notes/iset4_remeasure_spec_v1.md (§3 測定仕様 [B'])
## 前提: docs/notes/set_surgery_vetting_v1.md §6・定義ノート L153-173・cert
##   search/certs/set_surgery_fixture_v1_20260813.json
##
## 対象: (i) N=[1008,521] slot1 (既列挙48 shadow) -- 完走。
##       (ii) K^(9)(isolated・陽性対照)-- 【実装障害・blocked】σ1 の実像を持つ B3 内
##       実現が現行コードベースに存在しない(既存 K(9) 構成 search/k9-package.g の
##       BuildPn(9) は X=σ1^2,Y=σ2^2 のみを直接構成する抽象 dihedral-wreath モデルで、
##       σ1 自身の実像も B3 との具体的な埋め込みも持たない)。D_1:=C_Q(σ̄1) の計算には
##       σ1 の実像が必須であり、C_Q(X) を代用するのは根拠のない飛躍(σ1 の平方根の
##       非一意性)。速達で司令塔へ報告済み(2026-08-13)。[B'-3](W4) は UNKNOWN として
##       cert に記帳し、本 script は実行しない。
##
## 規律: u/c 非接触・封印非接触・prereg 非抵触。判定語なし・cert は生値のみ。
##   ★ D0/D1 の定義(spec §2): D_1 := C_Q(σ̄_1) = C_{B3/N}(σ̄_1) ∩ Q (Q 内・PN でない)。
##   D_0 := D_1 ∩ [Q,Q]。charming 側の gcd(u,N_ord) 条件は捻りで不変ゆえ q ごとに
##   再評価しない(spec 本文の注記どおり)。
##   ★ (S) 全射性は常に "full B_3/N 版"(Group(s1^u, g^-1 s2^u g) の生成が Size(Bq) に
##   一致するか)で評価する -- Prop 3.6 の近道(x,y 生成が Size(Q) に一致)は charming
##   前提下でのみ full 版と同値であり、(C) が偽の対でこの近道を使うと spec の警告に
##   抵触する。よって全 (t,q) で一律に full 版を使う(分岐しない・常に正しい側を採用)。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;

## ================= (F2) machinery, VERBATIM from search/set_surgery_fixture_v1.g
##   (itself verbatim from search/iso_census83_deep15_v1.g / search/wall-miner-v4.g) =================
MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProd([s1, s2, s1]);  dd := AbstractProd([s1, s2]);
  cc := DD^2;  zz := AbstractProd([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;
TT := function(W, g) return AbstractProd([W.dlt, g, W.dlt^-1]); end;;
TH := function(W, g) return AbstractProd([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W, m, f)
  local Wd;
  Wd := AbstractProd([W.y^m, f]);
  return AbstractProd([TT(W, TT(W, Wd)), TT(W, Wd), Wd]);
end;;
CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m, f]);
    od;
  od;
  return Set(out);
end;;

BF3 := FreeGroup("a", "b");;
brelD := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brelD];;
ga := B3.1;;  gb := B3.2;;
a := ga;;  b := gb;;

BuildWindowFromWords := function(indexExpected, words)
  local genElts, N, idxOk, isNormal, hm, Gimg, isoQ, s1, s2;
  genElts := List(words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  idxOk := (Index(B3, N) = indexExpected);;
  isNormal := IsNormal(B3, N);;
  if not (idxOk and isNormal) then
    Error("BuildWindowFromWords: index/normality mismatch, idx_ok=", idxOk, " is_normal=", isNormal);
  fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gimg := Image(hm);;
  isoQ := IsomorphismPermGroup(Gimg);;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;
  return MakeWindow(s1, s2);;
end;;

Print("############################################################\n");
Print("# iset4_bprime_v1.g -- 検算B' 座標捻り再測定(裁定1089)\n");
Print("############################################################\n");

## ================= 窓の構成: [1008,521] slot1 =================
Print("\n=== 窓: [1008,521] slot1 ===\n");
Read("search/iso_census83_deep15_data.g");;
entryFix := DEEP15[1];;
if entryFix.id <> [1008, 521] then
  Error("iset4_bprime_v1: DEEP15[1].id != [1008,521], got ", entryFix.id, " -- fixture mismatch, refusing to proceed");
fi;
W := BuildWindowFromWords(entryFix.index, entryFix.words);;
if not (W.c <> Identity(W.Bq)) then
  Error("iset4_bprime_v1: expected c notin N for this (deep, non-isolated) window");
fi;
Print("  |Bq|=", Size(W.Bq), " |Q(=W.PN)|=", Size(W.PN), " N_ord=", W.Nord, " z(order of c)=", Order(W.c), "\n");

## ================= [B'-0] 土台量 =================
Print("\n=== [B'-0] 土台量 ===\n");
Qgrp := W.PN;;
PNfull := Subgroup(W.Bq, [W.x, W.y, W.c]);;
qSize := Size(Qgrp);;
pnFullSize := Size(PNfull);;
zFull := Order(W.c);;
z0 := Index(PNfull, Qgrp);;
Dcomm := DerivedSubgroup(Qgrp);;
DcommIndex := Index(Qgrp, Dcomm);;
D1 := Intersection(Centralizer(W.Bq, W.s1), Qgrp);;
D0 := Intersection(D1, Dcomm);;
d1Size := Size(D1);;
d0Size := Size(D0);;
d0IsTrivial := (d0Size = 1);;
Print("  |Q|=", qSize, "  |PN_full(=PB3/N image)|=", pnFullSize, "  ord(c-bar)=", zFull, "  z0=[PN_full:Q]=", z0, "\n");
Print("  |[Q,Q]|=", Size(Dcomm), "  [Q:[Q,Q]]=", DcommIndex, "\n");
Print("  |D_1|=|C_Q(sigma1-bar)|=", d1Size, "  |D_0|=|D_1 cap [Q,Q]|=", d0Size, "\n");
Print("  d0_is_trivial (early-vacuous flag, machine value only) = ", d0IsTrivial, "\n");

## ================= shadow 列挙 =================
Print("\n=== shadow 列挙 ===\n");
charmingSetFix := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
corrFix := CorrectedShadows(W, charmingSetFix);;
shadowsFix := List(corrFix, sh -> rec(m := sh[1], f := sh[2]));;
Print("  shadow_total=", Length(shadowsFix), " (期待 48)\n");
shadowTotal48 := (Length(shadowsFix) = 48);;

## ================= [B'-1]+[B'-2] 全数走査: 3述語を独立評価 =================
Print("\n=== [B'-1]/[B'-2] 全数走査 (3述語×|Q| per shadow) ===\n");
QElts := Elements(Qgrp);;
Print("  |Q elements to scan per shadow|=", Length(QElts), "  total trials=", Length(shadowsFix)*Length(QElts), "\n");

tScan0 := GAPLIB_WallElapsedMs();;

## pattern histogram: index by (C,S,H) as 1..8 via bit code C*4+S*2+H
patternCounts := List([1..8], i -> 0);;
BInt := function(b) if b then return 1; else return 0; fi; end;;
PatIdx := function(c,s,h) return (BInt(c))*4 + (BInt(s))*2 + (BInt(h)) + 1; end;;

perShadow := [];;  ## rec(m, f_string, survive_count, surv_q_strings, surv_in_d1, surv_in_d0)
sepIndicatorHits := [];;  ## list of rec(m, f_string, q_string) with q in D0\{1}, C=true, H=false
w1Detail := [];;  ## rec(m, f_string, surv_count)
w2AllPass := true;;
w3Violations := [];;  ## (t,q) with q notin Dcomm but C=true or survive=true (should never happen)

sIdx := 0;;
for sh in shadowsFix do
  sIdx := sIdx + 1;;
  if GAPLIB_CheckCap(500.0, Concatenation("bprime-scan-", String(sIdx))) then
    Print("[CAP WARNING] stopping full scan at shadow ", sIdx, "\n");
    break;
  fi;
  m := sh.m;;  f := sh.f;;  u := 2*m + 1;;
  survQ := [];;
  for q in QElts do
    g := AbstractProd([f, q]);;
    Cval := (g in Dcomm);;
    genA := W.s1^u;;
    genB := AbstractProd([g^-1, W.s2^u, g]);;
    Sval := (Size(Group(genA, genB)) = Size(W.Bq));;
    hTheta := (AbstractProd([g, TH(W, g)]) = Identity(W.Bq));;
    hTau := (RtOf(W, m, g) = W.c^m);;
    Hval := hTheta and hTau;;
    patternCounts[PatIdx(Cval, Sval, Hval)] := patternCounts[PatIdx(Cval, Sval, Hval)] + 1;;
    if Cval and Sval and Hval then
      Add(survQ, q);;
    fi;
    ## (W3) sanity: q notin [Q,Q] should give C=false and no survival (since f in [Q,Q] by
    ## construction, g=f*q in [Q,Q] iff q in [Q,Q])
    if not (q in Dcomm) then
      if Cval or (Cval and Sval and Hval) then
        Add(w3Violations, rec(m := m, f_string := String(f), q_string := String(q)));
      fi;
    fi;
    ## (d) separation indicator: q in D0\{1}, C true, H false
    if (q in D0) and (q <> Identity(Qgrp)) and Cval and (not Hval) then
      Add(sepIndicatorHits, rec(m := m, f_string := String(f), q_string := String(q)));
    fi;
  od;
  if not (Identity(Qgrp) in survQ) then w2AllPass := false; fi;
  Add(w1Detail, rec(m := m, f_string := String(f), surv_count := Length(survQ)));
  Add(perShadow, rec(m := m, f_string := String(f), survive_count := Length(survQ),
    surv_q_strings := List(survQ, String),
    surv_in_d1 := Filtered(survQ, q -> q in D1), surv_in_d0 := Filtered(survQ, q -> q in D0)));
od;

tScan1 := GAPLIB_WallElapsedMs();;
Print("  scan elapsed_ms=", tScan1-tScan0, "\n");
Print("  pattern histogram (C,S,H order, bit index 1..8=CSH..csh): ", patternCounts, "\n");

## ================= (a) N_m 集計・(W1) 定理 SURV-EXACT の検算 =================
mVals := Set(List(w1Detail, r -> r.m));;
NmByM := List(mVals, mm -> rec(m := mm,
  counts := Set(List(Filtered(w1Detail, r -> r.m = mm), r -> r.surv_count))));;
w1AllUniform := ForAll(NmByM, r -> Length(r.counts) = 1);;
Print("\n=== (a) N_m by m (定理 SURV-EXACT: 全 t で |Surv(t)|=N_m のはず) ===\n");
for r in NmByM do
  Print("  m=", r.m, " distinct surv_counts seen=", r.counts, " uniform=", (Length(r.counts)=1), "\n");
od;
Print("[", PF(w1AllUniform), "] W1: |Surv(t)| は t の m のみに依存(全 m で一様): ", w1AllUniform, "\n");
Print("[", PF(w2AllPass), "] W2: 1 in Surv(t) for all t: ", w2AllPass, "\n");
w3AllPass := (Length(w3Violations) = 0);;
Print("[", PF(w3AllPass), "] W3: q notin [Q,Q] ==> C=false かつ生存なし (violations=", Length(w3Violations), "): ", w3AllPass, "\n");

## ================= (d) 分離指標 =================
Print("\n=== (d) 分離指標: D_0\\{1} で C=true・H=false の頻度 ===\n");
Print("  hits=", Length(sepIndicatorHits), " (over ", Length(shadowsFix), " shadows x |D_0\\{1}|=", d0Size-1, ")\n");

## ================= JSON output =================
JPerShadowRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"survive_count\":", String(r.survive_count),
    ",\"surv_q_strings\":", JArr(List(r.surv_q_strings, JStr)),
    ",\"surv_in_d1\":", JArr(List(r.surv_in_d1, x -> JStr(String(x)))),
    ",\"surv_in_d0\":", JArr(List(r.surv_in_d0, x -> JStr(String(x)))), "}");
end;;

JSepHitRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"q_perm_string\":", JStr(r.q_string), "}");
end;;

JW3ViolationRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"q_perm_string\":", JStr(r.q_string), "}");
end;;

JNmRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"distinct_surv_counts\":",
    JArr(List(r.counts, String)), ",\"uniform\":", JB(Length(r.counts)=1), "}");
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_bprime.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/iset4_bprime_v1.g");;
wordsSha256 := ComputeSha256File("search/iso_census83_deep15_data.g");;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/iset4_bprime/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/iset4_bprime_v1.g\",\"order\":\"裁定1089(検算B' I-SET-4座標捻り再測定)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/iset4_remeasure_spec_v1.md §3\"",
  ",\"window\":{",
    "\"id\":[1008,521],\"slot\":1,",
    "\"bq_order\":", String(Size(W.Bq)), ",\"n_ord\":", String(W.Nord), ",\"z_order_of_c\":", String(Order(W.c)), ",",
    "\"shadow_total\":", String(Length(shadowsFix)), ",\"shadow_total_matches_48\":", JB(shadowTotal48),
  "},",
  "\"b_prime_0_base_quantities\":{",
    "\"q_size\":", String(qSize), ",\"pn_full_size\":", String(pnFullSize), ",",
    "\"z_full_ord_cbar\":", String(zFull), ",\"z0_index_pnfull_over_q\":", String(z0), ",",
    "\"dcomm_size\":", String(Size(Dcomm)), ",\"dcomm_index\":", String(DcommIndex), ",",
    "\"d1_size\":", String(d1Size), ",\"d0_size\":", String(d0Size), ",",
    "\"d0_is_trivial\":", JB(d0IsTrivial),
  "},",
  "\"b_prime_1_2_scan\":{",
    "\"total_trials\":", String(Length(shadowsFix)*Length(QElts)), ",",
    "\"pattern_histogram_csh_bitindex_1to8\":", JArr(List(patternCounts, String)), ",",
    "\"pattern_histogram_note\":\"index = C*4+S*2+H+1 (C,S,H each 0/1); index1=(F,F,F)...index8=(T,T,T)\",",
    "\"per_shadow\":[", JoinC(List(perShadow, JPerShadowRec), ","), "]",
  "},",
  "\"n_m_by_m\":[", JoinC(List(NmByM, JNmRec), ","), "],",
  "\"w1_surv_exact\":{\"all_uniform\":", JB(w1AllUniform), "},",
  "\"w2_identity_survives\":{\"all_pass\":", JB(w2AllPass), "},",
  "\"w3_charming_regression\":{\"all_pass\":", JB(w3AllPass), ",\"violation_count\":", String(Length(w3Violations)),
    ",\"violations\":[", JoinC(List(w3Violations, JW3ViolationRec), ","), "]},",
  "\"d_separation_indicator\":{\"hit_count\":", String(Length(sepIndicatorHits)), ",",
    "\"d0_minus_1_size\":", String(d0Size-1), ",",
    "\"hits\":[", JoinC(List(sepIndicatorHits, JSepHitRec), ","), "]},",
  "\"k9_positive_control\":{\"status\":\"UNKNOWN_BLOCKED\",",
    "\"reason\":\"D_1:=C_Q(sigma1-bar) requires an actual image of sigma1 in the K^(9) window. The only existing K^(9) construction in this codebase (search/k9-package.g BuildPn(9)) builds an abstract dihedral-wreath permutation model that directly gives X=sigma1^2, Y=sigma2^2 only, with no concrete sigma1 element or embedding into an actual B3 subgroup (unlike [1008,521], which was built via BuildWindowFromWords from real B3 relator words). Substituting C_Q(X) for C_Q(sigma1-bar) would be unjustified (no established equality, non-unique square roots). Flagged to coordinator via express route before this run; not computed.\",",
    "\"w4_type_degeneracy_control\":\"not run\"},",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\",\"deep15_data_sha256\":\"", wordsSha256, "\"}",
  "}"
);;

outPath := "search/certs/iset4_remeasure_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
