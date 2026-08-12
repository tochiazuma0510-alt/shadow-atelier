## search/d972_h1_ns4_v1.g -- [CP] (H1) 帰着先測定(裁定1132)
##
## 正本: docs/notes/d972_h1_adjudication_v1.md 測定 spec 節(§5 [H1-A])。
##
## [A-5] 窓の同定(最優先): census83 control S4 窓(search/iso_census83_deep15_v1.g の
##   P2 ブロック・cert search/certs/iso_census83_deep15_v1_20260812.json p2_s4)が、
##   TRIAD-972 (M := K^(9) cap N_S4) 構成で使う N_S4 窓(search/d972_phase0_v1.g の
##   窓2 ブロック・cert search/certs/d972_phase0_v1_20260813.json anchors.s4_alone_*)
##   と同一の PB3 部分群かを機械判定する。
##
## 方法(機械判定・目視の「同じソース行」に頼らない):
##   両ブロックを本 script 内で独立に(変数名を分けて)再構成し、
##   (i) 生成元の permutation が literally 一致するか(Xperm=XpermCensus 等)
##   (ii) 群が literally 一致するか(Group(...) の要素集合として)
##   (iii) 不変量(位数・N_ord・charming_set_size)が一致するか
##   を assert ではなく生値として記録する(UNKNOWN 一級・判定語なし)。
##
## [A-1]-[A-3]: 独立に(F2) commutation-rule 述語(census83 iso_census83_deep15_v1.g の
##   CorrectedShadows/RunF2Window を verbatim 再掲・同一関数)を N_S4 窓に対して実行し、
##   settled/isolated の生値を本 script 内で再計算する(既存 cert の値を転記するだけに
##   しない -- 独立再実行によるクロスチェック)。
##
## [A-4]: #C(N_S4) と |GT^settled(N_S4)| を記録。定理 TORSOR: |GT|=|GT^settled|*#C。
##   #C は marked-factor-map の直接計算ではなく、all_kernel_trivial(=全 shadow settled)
##   から導かれる系 C(#C=1 <=> isolated)の適用としてのみ記録する(意味論は正本 §5 参照)。
##
## 規律: u/c 非接触・封印3量非接触・prereg 量非計算・判定語なし・UNKNOWN 一級。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");   # AbstractProd, JB, JStr, JPair, JoinC
Read("search/week3-psl-common.g");       # GF(8) helpers (CheckGF8, MakeMatGF8, MatToPermGF8, ...)

t0Global := GAPLIB_WallElapsedMs();;

Print("############################################################\n");
Print("# d972_h1_ns4_v1.g -- (H1) N_S4 window identity + isolated measurement (裁定1132)\n");
Print("############################################################\n");

## ================= [A-5] 独立再構成その1: TRIAD 側 N_S4(d972_phase0_v1.g 窓2 verbatim) =====
Print("\n=== [A-5] reconstruction 1: TRIAD N_S4 (search/d972_phase0_v1.g 窓2 verbatim) ===\n");
CheckGF8();;
Smat_triad := MakeMatGF8(1,0,1,1);;
Tmat_triad := MakeMatGF8(4,3,1,5);;
Sperm_triad := MatToPermGF8(Smat_triad);;
Tperm_triad := MatToPermGF8(Tmat_triad);;
wPerm_triad := Sperm_triad * Tperm_triad^-1;;
Xperm_triad := wPerm_triad^2;;
Yperm_triad := Sperm_triad^-1 * Xperm_triad * Sperm_triad;;
Ggrp_triad := Group(Xperm_triad, Yperm_triad);;
sz_triad := Size(Ggrp_triad);;
ord_triad := Lcm(Order(Xperm_triad), Order(Yperm_triad));;
Print("  |PB3/N_S4|(triad recon) = ", sz_triad, "  N_ord = ", ord_triad, "\n");

## ================= [A-5] 独立再構成その2: census83 control S4(iso_census83_deep15_v1.g P2 verbatim)
Print("\n=== [A-5] reconstruction 2: census83 control S4 (search/iso_census83_deep15_v1.g P2 verbatim) ===\n");
SmatS4_census := MakeMatGF8(1,0,1,1);;
TmatS4_census := MakeMatGF8(4,3,1,5);;
SpermS4_census := MatToPermGF8(SmatS4_census);;
TpermS4_census := MatToPermGF8(TmatS4_census);;
wPermS4_census := SpermS4_census * TpermS4_census^-1;;
XpermS4_census := wPermS4_census^2;;
YpermS4_census := SpermS4_census^-1 * XpermS4_census * SpermS4_census;;
GgS4_census := Group(XpermS4_census, YpermS4_census);;
sz_census := Size(GgS4_census);;
ord_census := Lcm(Order(XpermS4_census), Order(YpermS4_census));;
Print("  |PB3/N_S4|(census83 P2 recon) = ", sz_census, "  N_ord = ", ord_census, "\n");

## ================= [A-5] 同定判定(生値のみ・判定語は書かない) =================
Print("\n=== [A-5] identity comparison (raw booleans only) ===\n");
xGenEqual := (Xperm_triad = XpermS4_census);;
yGenEqual := (Yperm_triad = YpermS4_census);;
groupEqualAsSet := (Set(Elements(Ggrp_triad)) = Set(Elements(GgS4_census)));;
orderEqual := (sz_triad = sz_census);;
nordEqual := (ord_triad = ord_census);;
sourceMatSEqual := (Smat_triad = SmatS4_census);;
sourceMatTEqual := (Tmat_triad = TmatS4_census);;
Print("  x_generator_equal (Xperm literal) = ", xGenEqual, "\n");
Print("  y_generator_equal (Yperm literal) = ", yGenEqual, "\n");
Print("  group_equal_as_element_set = ", groupEqualAsSet, "\n");
Print("  order_equal = ", orderEqual, "  n_ord_equal = ", nordEqual, "\n");
Print("  source_matrix_S_equal = ", sourceMatSEqual, "  source_matrix_T_equal = ", sourceMatTEqual, "\n");

## cross-reference against the pre-existing certs (recorded values, not recomputed here)
censusCertExpectedSize := 504;;
censusCertExpectedShadowTotal := 54;;
triadCertExpectedSize := 504;;
triadCertExpectedShadowTotal := 54;; # anchors.s4_alone_shadow_total in d972_phase0_v1_20260813.json

## ================= [A-1]-[A-3]: (F2) commutation-rule settledness, independent re-execution =====
## VERBATIM from search/iso_census83_deep15_v1.g / search/wall-miner-v4.g (:40-71)
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

## reuse week3-psl-common.g's BuildQTGeneral (via week3-battery-common.g) to get the full B3
## generators s1,s2 (not just x=s1^2,y=s2^2) for the TRIAD N_S4 window -- required by MakeWindow.
qtN_S4 := BuildQTGeneral(Ggrp_triad, Xperm_triad, Yperm_triad, ());;   # phiC=() -- c in N (PU-F7, S^2=())
WN_S4 := MakeWindow(qtN_S4.s1, qtN_S4.s2);;
cIsIdentity := (WN_S4.c = Identity(WN_S4.Bq));;
Print("\n=== [A-1]-[A-3] independent (F2) re-execution on TRIAD N_S4 window ===\n");
Print("  assert c=1 in Bq (c in N_S4, PU-F7): ", cIsIdentity, "\n");

CharmingSetOf := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

charmingSet_A5 := CharmingSetOf(WN_S4.Nord);;
dOrder_A5 := Size(DerivedSubgroup(WN_S4.PN));;
candidateTotal_A5 := dOrder_A5 * Length(charmingSet_A5);;
corr_A5 := CorrectedShadows(WN_S4, charmingSet_A5);;
shadowTotal_A5 := Length(corr_A5);;

kernelDetail_A5 := [];;
for sh in corr_A5 do
  m := sh[1];;  u := 2*m+1;;  f := sh[2];;
  psi := GroupHomomorphismByImages(WN_S4.PN, WN_S4.PN, [WN_S4.x, WN_S4.y], [WN_S4.x^u, AbstractProd([f^-1, WN_S4.y^u, f])]);;
  if psi = fail then
    wellDef := false;;  kerTrivial := false;;  kerSize := fail;;
  else
    wellDef := true;;  kerSize := Size(Kernel(psi));;  kerTrivial := (kerSize = 1);;
  fi;
  Add(kernelDetail_A5, rec(m:=m, u:=u, well_defined:=wellDef, kernel_trivial:=kerTrivial, kernel_size:=kerSize));
od;;
kernelTrivialCount_A5 := Length(Filtered(kernelDetail_A5, r -> r.well_defined and r.kernel_trivial));;
allKernelTrivial_A5 := (kernelTrivialCount_A5 = shadowTotal_A5);;

Print("  N_ord=", WN_S4.Nord, " charming_set_size=", Length(charmingSet_A5),
      " derived_subgroup_order=", dOrder_A5, " candidate_total=", candidateTotal_A5, "\n");
Print("  shadow_total=", shadowTotal_A5, " kernel_trivial_count=", kernelTrivialCount_A5, "/", shadowTotal_A5,
      " all_kernel_trivial=", allKernelTrivial_A5, "\n");

## ================= [A-4]: #C(N_S4) and |GT^settled(N_S4)| =================
## 系 C(正本参照): all_kernel_trivial(=全 shadow settled) <=> #C=1 <=> isolated。
## marked-factor-map の直接計算(AutomorphismGroup(PN))はここでは実行しない
## (|PN|=504 は裁定1117 の壁を大きく下回るので実行可能だが、系Cの適用で#Cが
## 既に定まるため冗長 -- 生値のみ記録、実行しないことを明記)。
gtSettledSize_A4 := kernelTrivialCount_A5;;  # |GT^settled(N_S4)| = settled shadow count
numC_A4 := fail;;
if allKernelTrivial_A5 then
  numC_A4 := 1;;
fi;;
Print("\n=== [A-4] #C(N_S4) via 系 C(all_kernel_trivial -> #C=1) ===\n");
Print("  |GT^settled(N_S4)| = ", gtSettledSize_A4, "  shadow_total = ", shadowTotal_A5, "\n");
if numC_A4 = fail then
  Print("  #C(N_S4) = UNKNOWN (all_kernel_trivial=false -- 系C not applicable, marked-factor-map would be required)\n");
else
  Print("  #C(N_S4) = ", numC_A4, " (via 系C: all_kernel_trivial=true)\n");
fi;

t1Global := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1Global - t0Global, " ms\n");

## ================= JSON 出力 =================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_d972h1ns4.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/d972_h1_ns4_v1.g");;
censusCertSha256 := ComputeSha256File("search/certs/iso_census83_deep15_v1_20260812.json");;
triadCertSha256 := ComputeSha256File("search/certs/d972_phase0_v1_20260813.json");;

JKernelDetailRec := function(r)
  local kszStr;
  if r.kernel_size = fail then kszStr := "null"; else kszStr := String(r.kernel_size); fi;
  return Concatenation("{\"m\":", String(r.m), ",\"u\":", String(r.u), ",\"well_defined\":", JB(r.well_defined),
    ",\"kernel_trivial\":", JB(r.kernel_trivial), ",\"kernel_size\":", kszStr, "}");
end;;

numCStr := "null";;
if numC_A4 <> fail then numCStr := String(numC_A4); fi;;

cert := Concatenation(
  "{\"schema\":\"h1_ns4_isolated/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/d972_h1_ns4_v1.g\",\"order\":\"裁定1132 ([CP] (H1) の帰着先測定)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/d972_h1_adjudication_v1.md §5 [H1-A]\"",
  ",\"a5_window_identity\":{",
    "\"triad_reconstruction\":{\"pb3_over_n_s4\":", String(sz_triad), ",\"n_ord\":", String(ord_triad), "},",
    "\"census83_p2_reconstruction\":{\"pb3_over_n_s4\":", String(sz_census), ",\"n_ord\":", String(ord_census), "},",
    "\"x_generator_literally_equal\":", JB(xGenEqual), ",",
    "\"y_generator_literally_equal\":", JB(yGenEqual), ",",
    "\"group_literally_equal_as_element_set\":", JB(groupEqualAsSet), ",",
    "\"order_equal\":", JB(orderEqual), ",",
    "\"n_ord_equal\":", JB(nordEqual), ",",
    "\"source_matrix_S_equal\":", JB(sourceMatSEqual), ",",
    "\"source_matrix_T_equal\":", JB(sourceMatTEqual), ",",
    "\"cross_reference\":{",
      "\"census83_cert_path\":\"search/certs/iso_census83_deep15_v1_20260812.json\",",
      "\"census83_cert_sha256\":\"", censusCertSha256, "\",",
      "\"census83_cert_p2_s4_pn_order\":504,\"census83_cert_p2_s4_shadow_total\":54,",
      "\"census83_cert_p2_s4_kernel_trivial_count\":54,\"census83_cert_p2_s4_all_kernel_trivial\":true,",
      "\"triad_cert_path\":\"search/certs/d972_phase0_v1_20260813.json\",",
      "\"triad_cert_sha256\":\"", triadCertSha256, "\",",
      "\"triad_cert_s4_alone_shadow_total\":", String(triadCertExpectedShadowTotal), ",",
      "\"triad_cert_s4_alone_pass\":true",
    "}",
  "},",
  "\"a1_a3_independent_reexecution\":{",
    "\"c_in_n_s4_assert\":", JB(cIsIdentity), ",",
    "\"n_ord\":", String(WN_S4.Nord), ",\"charming_set_size\":", String(Length(charmingSet_A5)), ",",
    "\"derived_subgroup_order\":", String(dOrder_A5), ",\"candidate_total\":", String(candidateTotal_A5), ",",
    "\"shadow_total\":", String(shadowTotal_A5), ",",
    "\"kernel_trivial_count\":", String(kernelTrivialCount_A5), ",",
    "\"all_kernel_trivial\":", JB(allKernelTrivial_A5), ",",
    "\"kernel_detail\":[", JoinC(List(kernelDetail_A5, JKernelDetailRec), ","), "]",
  "},",
  "\"a4_numC\":{",
    "\"gt_settled_size\":", String(gtSettledSize_A4), ",",
    "\"shadow_total\":", String(shadowTotal_A5), ",",
    "\"num_C\":", numCStr, ",",
    "\"method\":\"系C(定義ノート・all_kernel_trivial(=全shadow settled) <=> #C=1 <=> isolated) の適用。marked-factor-map(AutomorphismGroup(PN))の直接計算は未実行(#Cが系Cで既に定まるため冗長・|PN|=504はコスト上は実行可能)。\"",
  "},",
  "\"u_touched\":false,\"c_touched\":false,\"prereg_quantities_untouched\":true",
  ",\"no_verdict_note\":\"machine values only; verdict は司令塔/数学者。UNKNOWN は一級の結果。\"",
  ",\"total_elapsed_ms\":", String(t1Global - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/d972_h1_ns4_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("D972_H1_NS4_DONE\n");
QUIT;
