## search/iso_census83_deep15_v1.g -- ISO-CENSUS-83 本走(裁定986: (F2)商規律への差替え・
## 対象=delta>1 15窓のみ + 札7 witness[1728,31095]のコスト実測)
##
## METHOD (裁定986【1】): wcp5d_resolution_v1.md(裁定166)が supersede した (F2) 商規律。
## theta~=Ad(Delta)・tau~=Ad(delta) を PB3/N 内の共役として構成(語を一切使わない)。
## 判定式: f*theta~(f)=1((3.10)側) AND tau~^2(y^m f)*tau~(y^m f)*(y^m f) = c^m ((3.11)側、
## =1 ではない)。参照実装 = search/wall-miner-v4.g の CorrectedShadows/TH/TT/RtOf(:90-113、
## この script で verbatim 再掲)。EnumerateWordLevelHexagon(week3-battery-common.g、語レベル版)
## は呼ばない(失効宣言済み、裁定166 SS6)。
##
## 較正2段(陽性対照、裁定986 維持):
##  P1 = K^(3)(BuildPn3(3), 位数108, search/iso_census83_skeleton_v1.g の既存較正窓、c∈N)。
##       商内で c=1 に退化することを assert c=Identity(Bq) として記録した上で、旧式(骨格の
##       較正済12/12、本 script 実行時に再確認)と完全一致することを比較。
##  P2 = S4窓(PSL(2,8)/GF(8), 位数504, search/week3-psl-S4.g の構成、c∈N)。
##       (F2) 機構での再計算が既存 cert search/certs/s4_settled54_v2_20260812.json
##       (shadow_total=54, kernel_trivial_count=54/54, g_size=504, n_ord=9, charming_set_size=6)
##       と一致することを比較。
##       ★ NAME NOTE(要司令塔確認・ブロックせず記録): 発注文言は「s4_fullpre_census_v2」を
##       比較対象として指定したが、そのファイル(search/certs/s4_fullpre_census_v2_20260812.json)
##       は Hol(Z/9) の部分群 census(K9/S4-order 系統・裁定955)であって、hexagon/shadow 列挙
##       や theta/tau・c を一切扱わない別対象(target_group=Hol(Z/9), idgroup=[54,6])。
##       (F2) 較正として意味を持つのは shadow 列挙の既存確立値を持つ s4_settled54_v2(S4-SETTLED-54
##       系統・PSL(2,8)窓・裁定889/891/892)であるため、そちらを使用した。
##
## 対象窓データ: search/iso_census83_deep15_data.g の DEEP15(search/extract_deep15_data.g が
## search/zcensus83_data.g の TARGET83 から抽出した、delta>1(A型・e=6)15レコードの canonical
## words -- search/certs/zcensus83_v2_20260812.json target83_detail と対応)。
##
## 規律: 判定語なし(W-48)・UNKNOWN一級・600秒cap(shard可、GAPLIB_CheckCap使用)・u非接触。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");   # AbstractProd, BuildQTGeneral, PF, JStr/JB/JoinC/JArr/WriteFile
Read("search/week3-psl-common.g");       # GF(8) helpers (CheckGF8, MakeMatGF8, MatToPermGF8, ...)

t0Global := GAPLIB_WallElapsedMs();;

## ================= (F2) machinery, VERBATIM from search/wall-miner-v4.g (:77-113) =================
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

## ================= I2-style per-window runner (a=enum, b=kernel eq, c=citation, d=c-status/z) ====
RunF2Window := function(W, label)
  local charmingSet, corr, shadowTotal, dOrder, candidateTotal, kernelDetail, sh, m, u, f, psi,
        wellDef, kerTrivial, kerSize, kernelTrivialCount, allKernelTrivial, centerOrder, zVal,
        zNotDividesUAll, cCitation;
  charmingSet := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
  dOrder := Size(DerivedSubgroup(W.PN));;
  candidateTotal := dOrder * Length(charmingSet);;
  corr := CorrectedShadows(W, charmingSet);;
  shadowTotal := Length(corr);;

  kernelDetail := [];;
  for sh in corr do
    m := sh[1];;  u := 2*m+1;;  f := sh[2];;
    psi := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y], [W.x^u, AbstractProd([f^-1, W.y^u, f])]);;
    if psi = fail then
      wellDef := false;;  kerTrivial := false;;  kerSize := fail;;
    else
      wellDef := true;;  kerSize := Size(Kernel(psi));;  kerTrivial := (kerSize = 1);;
    fi;
    Add(kernelDetail, rec(m:=m, u:=u, well_defined:=wellDef, kernel_trivial:=kerTrivial, kernel_size:=kerSize));
  od;;
  kernelTrivialCount := Length(Filtered(kernelDetail, r -> r.well_defined and r.kernel_trivial));;
  allKernelTrivial := (kernelTrivialCount = shadowTotal);;

  centerOrder := Size(Center(W.PN));;
  zVal := Order(W.c);;
  # I.1.4 note (kept, group-theoretic, independent of theta/tau bug): necessary condition for
  # c notin ker T_{m,f} is z does-not-divide u=2m+1. Recorded descriptively, no verdict.
  zNotDividesUAll := ForAll(corr, s -> ((2*s[1]+1) mod zVal <> 0)) or zVal = 1;;

  cCitation := "裁定529, docs/notes/auto_settled_check_v1.md 付録A.1 (AS-GAP-3 -- EnumerateReducedHexagon は descent 判定を呼ばない、共有関数につき窓非依存で成立。本 script は (F2) 経路につき EnumerateReducedHexagon 自体を呼ばないが、descent 判定を経由しない構造は CorrectedShadows でも同様)";;

  Print("  [", label, "] |Bq|=", Size(W.Bq), " |PN|=", Size(W.PN), " N_ord=", W.Nord,
        " charming=", Length(charmingSet), " candidate_total=", candidateTotal,
        " shadow_total=", shadowTotal, " kernel_trivial=", kernelTrivialCount, "/", shadowTotal,
        " z=", zVal, " center_order=", centerOrder, "\n");

  return rec(label:=label, bq_order:=Size(W.Bq), pn_order:=Size(W.PN), n_ord:=W.Nord,
             charming_set_size:=Length(charmingSet), derived_subgroup_order:=dOrder,
             candidate_total:=candidateTotal, shadow_total:=shadowTotal,
             kernel_trivial_count:=kernelTrivialCount, all_kernel_trivial:=allKernelTrivial,
             center_order:=centerOrder, z:=zVal, c_is_identity:=(W.c = Identity(W.Bq)),
             z_notdivides_u_all:=zNotDividesUAll, c_staleness_citation:=cCitation,
             kernel_detail:=kernelDetail);
end;;

## ================= shared B3 = <a,b|aba=bab> setup (words -> N -> B3/N, verbatim pattern from
## search/wall-miner-v4.g / search/zcensus83_v1.g) =================
BF3 := FreeGroup("a", "b");;
brelD := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brelD];;
ga := B3.1;;  gb := B3.2;;
a := ga;;  b := gb;;   # global bind for EvalString(word) below (search/zcensus83_data.g's words
                       # use bare "a","b" identifiers, per search/zcensus83_v1.g convention)

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
Print("# iso_census83_deep15_v1.g -- (F2) commutation-rule ISO-CENSUS-83 (裁定986)\n");
Print("############################################################\n");

## ================= P1: K^(3) calibration (c in N) =================
Print("\n=== positive control P1: K^(3) (order 108, c in N) ===\n");
BuildPn3ForCal := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, X, Y, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);  a2 := tr(r,2);  a3 := tr(r,3);
  q1 := tr(s,2)*tr(s,3);  q2 := tr(s,1)*tr(s,3);
  X := AbstractProd([a1,q1]);  Y := AbstractProd([a1,a2,a3,q2]);
  Gfull := Group(a1,a2,a3,q1,q2);
  return rec(x:=X, y:=Y, G:=Gfull);
end;;

k3rec := BuildPn3ForCal(3);;
if Size(k3rec.G) <> 108 then Error("P1: K3 PN order mismatch, got ", Size(k3rec.G)); fi;
qtK3 := BuildQTGeneral(k3rec.G, k3rec.x, k3rec.y, ());;   # phiC=() -- c assumed trivial (c in N)
WK3 := MakeWindow(qtK3.s1, qtK3.s2);;
if not (WK3.c = Identity(WK3.Bq)) then
  Error("P1 FAILED: K^(3) c did not degenerate to identity in the quotient -- c_in_N assumption violated");
fi;
Print("  [P1] assert c=1 in Bq: ", (WK3.c = Identity(WK3.Bq)), "\n");
p1Result := RunF2Window(WK3, "P1-K3");;
p1MatchesBaseline := (p1Result.shadow_total = 12) and (p1Result.kernel_trivial_count = 12)
                      and (p1Result.pn_order = 108) and (p1Result.n_ord = 6);;
Print("  [P1] matches skeleton baseline (shadow_total=12, kernel_trivial=12/12, |PN|=108, N_ord=6): ",
      p1MatchesBaseline, "\n");
if not p1MatchesBaseline then
  Error("POSITIVE CONTROL P1 FAILED: (F2) machinery on K^(3) does not reproduce the skeleton's committed 12/12 baseline -- stopping before touching the 15 target windows");
fi;

## ================= P2: S4 (PSL(2,8)) calibration (c in N) =================
Print("\n=== positive control P2: S4 window (PSL(2,8)/GF(8), order 504, c in N) ===\n");
CheckGF8();;
SmatS4 := MakeMatGF8(1,0,1,1);;
TmatS4 := MakeMatGF8(4,3,1,5);;
SpermS4 := MatToPermGF8(SmatS4);;
TpermS4 := MatToPermGF8(TmatS4);;
wPermS4 := SpermS4 * TpermS4^-1;;
XpermS4 := wPermS4^2;;
YpermS4 := SpermS4^-1 * XpermS4 * SpermS4;;
GgS4 := Group(XpermS4, YpermS4);;
if Size(GgS4) <> 504 then Error("P2: S4 PN order mismatch, got ", Size(GgS4)); fi;
qtS4 := BuildQTGeneral(GgS4, XpermS4, YpermS4, ());;   # phiC=() -- c in N per PU-F7 (S^2=())
WS4 := MakeWindow(qtS4.s1, qtS4.s2);;
if not (WS4.c = Identity(WS4.Bq)) then
  Error("P2 FAILED: S4 c did not degenerate to identity in the quotient -- c_in_N assumption violated");
fi;
Print("  [P2] assert c=1 in Bq: ", (WS4.c = Identity(WS4.Bq)), "\n");
p2Result := RunF2Window(WS4, "P2-S4");;
p2MatchesBaseline := (p2Result.shadow_total = 54) and (p2Result.kernel_trivial_count = 54)
                      and (p2Result.pn_order = 504) and (p2Result.n_ord = 9)
                      and (p2Result.charming_set_size = 6);;
Print("  [P2] matches s4_settled54_v2 baseline (shadow_total=54, kernel_trivial=54/54, |PN|=504, N_ord=9, charming=6): ",
      p2MatchesBaseline, "\n");
if not p2MatchesBaseline then
  Error("POSITIVE CONTROL P2 FAILED: (F2) machinery on S4 window does not reproduce the committed s4_settled54_v2 baseline -- stopping before touching the 15 target windows");
fi;

## ================= main: 15 delta>1 windows =================
Print("\n=== main census: 15 delta>1 (A-type, e=6) windows, (F2) commutation rule ===\n");
Read("search/iso_census83_deep15_data.g");;   # defines DEEP15
if Length(DEEP15) <> 15 then Error("DEEP15 length != 15, got ", Length(DEEP15)); fi;

## the 15 records' (index,id,e,z,z_ab,delta) from search/certs/zcensus83_v2_20260812.json
## target83_detail (delta>1 subset), matched by id_group to DEEP15 entries in the same order
## produced by search/extract_deep15_data.g's Filtered() call (which preserves TARGET83's own
## iteration order -- verified below by cross-checking id_group match per entry).
CERT15 := [
  rec(id:=[1008,521],    e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1008,521],    e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1008,683],    e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1008,683],    e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1134,55],     e:=6, z_cert:=3, z_ab:=1, delta:=3),
  rec(id:=[1134,55],     e:=6, z_cert:=3, z_ab:=1, delta:=3),
  rec(id:=[1134,53],     e:=6, z_cert:=3, z_ab:=1, delta:=3),
  rec(id:=[1134,53],     e:=6, z_cert:=3, z_ab:=1, delta:=3),
  rec(id:=[1152,154161], e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1152,154163], e:=6, z_cert:=4, z_ab:=1, delta:=4),
  rec(id:=[1152,154163], e:=6, z_cert:=4, z_ab:=1, delta:=4),
  rec(id:=[1872,568],    e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1872,568],    e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1872,780],    e:=6, z_cert:=2, z_ab:=1, delta:=2),
  rec(id:=[1872,780],    e:=6, z_cert:=2, z_ab:=1, delta:=2)
];;

deep15Results := [];;
i := 0;;
for entry in DEEP15 do
  i := i + 1;;
  cmeta := CERT15[i];;
  if entry.id <> cmeta.id then
    Error("DEEP15/CERT15 order mismatch at position ", i, ": ", entry.id, " vs ", cmeta.id);
  fi;
  if GAPLIB_CheckCap(500.0, Concatenation("deep15-", String(i))) then
    Print("[CAP WARNING] stopping deep15 loop at position ", i, "\n");
    break;
  fi;
  Wwin := BuildWindowFromWords(entry.index, entry.words);;
  if not (Wwin.c <> Identity(Wwin.Bq)) then
    Error("window ", i, " (id=", entry.id, "): c IS identity -- expected c notin N for a delta>1 window");
  fi;
  r := RunF2Window(Wwin, Concatenation("deep15-", String(i), "-id", String(entry.id[1]), "-", String(entry.id[2])));;
  r.index := entry.index;;  r.id_group := entry.id;;  r.e_cert := cmeta.e;;
  r.z_cert := cmeta.z_cert;;  r.z_ab_cert := cmeta.z_ab;;  r.delta_cert := cmeta.delta;;
  r.z_cross_check_ok := (r.z = cmeta.z_cert);;
  if not r.z_cross_check_ok then
    Print("  [ANOMALY] window ", i, " (id=", entry.id, "): z from (F2) reconstruction (", r.z,
          ") != z from zcensus83_v2 cert (", cmeta.z_cert, ")\n");
  fi;
  Add(deep15Results, r);;
od;;

Print("\n15 window census complete: ", Length(deep15Results), "/15 processed\n");

## ================= [1728,31095] cost-only run (札7 witness, delta=1, C-type -- separate from
## the 15-window target list per 裁定986 point 2; NOT part of the delta>1 target, run once here
## for a real measured cost data point per 札7's cost-formula calibration request) =================
Print("\n=== 札7 witness cost run: [1728,31095] (delta=1, C-type, NOT part of the 15-window target) ===\n");
witnessWords := [ "a^-8", "b^-8", "a*b^-8*a^-1", "a^-1*b^-8*a", "a^2*b^-8*a^-2", "a^-2*b^-8*a^2",
  "(a^-1*b*a^-1)^2*(b^2*a^-1)^2", "a^-1*(b*a^-1*b)^2*b*a^-2*b*a^-1", "b*a^-2*(b*a^-1*b)^2*b*a^-2",
  "(b*a^-1)^6", "(b*a^-1*b)^2*(b*a^-2)^2", "b*a^-1*b^7*a^-1*b*a", "b*(b*a^-2)^2*b*a^-1*b^2*a^-1",
  "(b^2*a^-1)^2*(a^-1*b*a^-1)^2", "(b^-1*a^2)^2*(b^-2*a)^2", "b^-1*a*(a*b^-2)^2*a*b^-1*a^2",
  "b^-1*(a*b^-1*a)^2*a*b^-2*a*b^-1", "(b^-1*a)^6", "(b^-1*a*b^-1)^2*(a^2*b^-1)^2",
  "b^-1*a*b^-7*a*b^-1*a^-1", "b^-2*(a*b^-1*a)^2*a*b^-2*a", "(b^-2*a)^2*(b^-1*a^2)^2",
  "a^3*b^-8*a^-3", "a*b*a^-2*(b*a^-1*b)^2*b*a^-3", "a*(b*a^-1)^6*a^-1",
  "a*(b*a^-1*b)^2*(b*a^-2)^2*a^-1", "a*b^-1*(a*b^-1*a)^2*a*b^-2*a*b^-1*a^-1",
  "a*(b^-1*a*b^-1)^2*(a^2*b^-1)^2*a^-1", "(a*b^-1)^2*b^-6*a*b^-1*a^-2", "a^-3*b^-8*a^3",
  "(a^-2*b^2)^2*(b*a^-1)^3", "(a^-1*b)^2*b^6*a^-1*b*a^2", "a^-1*b^2*(b*a^-1)^3*a^-2*b^2*a^-1",
  "a^-1*(b^-1*a^2)^2*(b^-2*a)^2*a", "a^-1*b^-1*a*(a*b^-2)^2*a*b^-1*a^3", "a^-1*(b^-1*a)^6*a",
  "a^-1*(b^-2*a)^2*(b^-1*a^2)^2*a", "b*a^-2*b^7*a^-1*b^2*a", "(b*a^-1)^2*a^-7*b^-1*a*b^-1",
  "(b*a^-1)^2*(a^-2*b^2)^2*b*a^-1", "b^2*a^-2*b^2*(b*a^-1)^3*a^-2", "b^2*a^-1*b^7*a^-2*b*a",
  "b^2*(b*a^-1)^3*a^-2*b^2*a^-2", "b^-1*a^2*b^-7*a*b^-2*a^-1", "(b^-1*a)^2*b^-1*(b^-2*a^2)^2*a",
  "b^-1*a*b^-1*(b^-2*a^2)^2*a*b^-1*a", "b^-2*a*b^-7*a^2*b^-1*a^-1", "b^-1*(b^-2*a^2)^2*(a*b^-1)^2*a",
  "a^4*b^-8*a^-4", "a^2*b*a^-2*(b*a^-1*b)^2*b*a^-4", "a^2*(b*a^-1*b)^2*(b*a^-2)^2*a^-2",
  "a^2*b^-1*(a*b^-1*a)^2*a*b^-2*a*b^-1*a^-2", "a^2*(b^-1*a*b^-1)^2*(a^2*b^-1)^2*a^-2",
  "a*(a*b^-1)^2*b^-6*a*b^-1*a^-3", "a*(b*a^-1)^2*(a^-2*b^2)^2*b*a^-2", "a*b^2*a^-2*b^2*(b*a^-1)^3*a^-3",
  "a*b^2*(b*a^-1)^3*a^-2*b^2*a^-3", "a*b^-1*a^2*b^-7*a*b^-2*a^-2", "(a*b^-2)^2*b^-5*a^2*b^-1*a^-2",
  "a^-2*(a^-1*b^2)^2*b^2*a^-3*b^2*a^-1", "a^-3*b^-1*a*(a*b^-2)^2*a*b^-1*a^-3",
  "a^-3*(b^-1*a)^2*b^-3*a^2*b^-2*a^-2", "a^-3*b^-1*a*b^-4*a^3*b^-3*a^-1",
  "a^-3*(b^-2*a)^2*b^-1*a^2*b^-1*a^-3", "a^-2*b^-1*a*(a*b^-2)^2*a*b^-1*a^-4", "a^-2*(b^-1*a)^6*a^2",
  "a^-2*(b^-2*a)^2*b^-1*a^2*b^-1*a^-4", "a^-1*(b*a^-2*b^3)^2*a^-3", "(a^-1*b)^2*a^-8*(b^-1*a)^2",
  "a^-1*b^3*a^-3*b^3*(b*a^-1)^2*a^-2", "a^-1*b^3*(b*a^-1)^2*a^-3*b^3*a^-2",
  "a^-1*(b^-1*a)^2*b^-3*a^2*b^-2*a^-4", "a^-1*b^-1*a*b^-1*(b^-2*a^2)^2*a*b^-1*a^2",
  "(a^-1*b^-2*a^-1)^4", "(b^2*a^-2)^4", "b^3*a^-3*b^3*(b*a^-1)^2*a^-3" ];;

GASMAN("collect");;
memBefore := GasmanStatistics();;
wallBefore := GAPLIB_WallElapsedMs();;
cpuBefore := Runtime();;
Wwitness := BuildWindowFromWords(1728, witnessWords);;
witnessResult := RunF2Window(Wwitness, "witness-1728-31095");;
cpuAfter := Runtime();;
wallAfter := GAPLIB_WallElapsedMs();;
GASMAN("collect");;
memAfter := GasmanStatistics();;
witnessWallMs := wallAfter - wallBefore;;
witnessCpuMs := cpuAfter - cpuBefore;;
witnessMemKbLiveBefore := memBefore.full.livekb;;
witnessMemKbLiveAfter := memAfter.full.livekb;;
Print("  witness cost: wall_ms=", witnessWallMs, " cpu_ms=", witnessCpuMs,
      " gasman_live_kb_before=", witnessMemKbLiveBefore,
      " gasman_live_kb_after=", witnessMemKbLiveAfter, "\n");

## ================= JSON output =================
JKernelDetailRec := function(r)
  local kszStr;
  if r.kernel_size = fail then kszStr := "null"; else kszStr := String(r.kernel_size); fi;
  return Concatenation("{\"m\":", String(r.m), ",\"u\":", String(r.u), ",\"well_defined\":", JB(r.well_defined),
    ",\"kernel_trivial\":", JB(r.kernel_trivial), ",\"kernel_size\":", kszStr, "}");
end;;

JRunResult := function(r)
  return Concatenation(
    "\"bq_order\":", String(r.bq_order), ",\"pn_order\":", String(r.pn_order),
    ",\"n_ord\":", String(r.n_ord), ",\"charming_set_size\":", String(r.charming_set_size),
    ",\"derived_subgroup_order\":", String(r.derived_subgroup_order),
    ",\"candidate_total\":", String(r.candidate_total), ",\"shadow_total\":", String(r.shadow_total),
    ",\"kernel_trivial_count\":", String(r.kernel_trivial_count),
    ",\"all_kernel_trivial\":", JB(r.all_kernel_trivial),
    ",\"center_order\":", String(r.center_order), ",\"z\":", String(r.z),
    ",\"c_is_identity\":", JB(r.c_is_identity), ",\"z_notdivides_u_all\":", JB(r.z_notdivides_u_all),
    ",\"kernel_detail\":[", JoinC(List(r.kernel_detail, JKernelDetailRec), ","), "]"
  );
end;;

JDeep15Rec := function(r)
  return Concatenation("{",
    "\"index\":", String(r.index), ",\"id_group\":", JPair(r.id_group[1], r.id_group[2]), ",",
    "\"e_cert\":", String(r.e_cert), ",\"z_cert\":", String(r.z_cert), ",\"z_ab_cert\":", String(r.z_ab_cert),
    ",\"delta_cert\":", String(r.delta_cert), ",\"z_cross_check_ok\":", JB(r.z_cross_check_ok), ",",
    JRunResult(r),
    "}");
end;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/iso_census83_deep15_v1\",",
  "\"authority\":\"\\u88c1\\u5b9a986 (\\u8a2d\\u8a08=docs/notes/win83_audit_and_unram3_v1.md I.1.3, \\u5dee\\u66ff\\u5f8c=(F2)\\u5546\\u898f\\u5f8b, wcp5d_resolution_v1.md \\u88c1\\u5b9a166 supersede)\",",
  "\"method\":\"(F2) commutation rule: theta~=Ad(Delta), tau~=Ad(delta) constructed as conjugation inside PB3/N (no word-level evaluation). Predicate: f*theta~(f)=1 AND tau~^2(y^m f)*tau~(y^m f)*(y^m f) = c^m. Reference implementation: search/wall-miner-v4.g CorrectedShadows/TH/TT/RtOf, verbatim-reused in this script. EnumerateWordLevelHexagon is NOT called (superseded per 裁定166).\",",
  "\"positive_control\":{",
    "\"p1_k3\":{\"object\":\"K^(3) (BuildPn3(3), order 108, c in N)\",",
      "\"assert_c_is_identity\":", JB(WK3.c = Identity(WK3.Bq)), ",",
      JRunResult(p1Result), ",",
      "\"matches_skeleton_baseline\":", JB(p1MatchesBaseline), ",",
      "\"baseline_ref\":\"search/iso_census83_skeleton_v1.g dry-run (re-run this session): shadow_total=12, kernel_trivial_count=12/12, |PN|=108, N_ord=6\"",
    "},",
    "\"p2_s4\":{\"object\":\"S4 window (PSL(2,8)/GF(8), search/week3-psl-S4.g construction, order 504, c in N)\",",
      "\"assert_c_is_identity\":", JB(WS4.c = Identity(WS4.Bq)), ",",
      JRunResult(p2Result), ",",
      "\"matches_baseline\":", JB(p2MatchesBaseline), ",",
      "\"baseline_ref\":\"search/certs/s4_settled54_v2_20260812.json: shadow_total=54, kernel_trivial_count=54/54, g_size=504, n_ord=9, charming_set_size=6\",",
      "\"name_note\":\"\\u767a\\u6ce8\\u6587\\u8a00\\u306f s4_fullpre_census_v2 \\u3092\\u6307\\u5b9a\\u3057\\u305f\\u304c\\u3001\\u305d\\u306e cert \\u306f Hol(Z/9) \\u90e8\\u5206\\u7fa4 census\\uff08K9/S4-order\\u7cfb\\u7d71\\u3001\\u88c1\\u5b9a955\\uff09\\u3067 hexagon/shadow/theta/tau/c \\u3092\\u4e00\\u5207\\u6271\\u308f\\u306a\\u3044\\u5225\\u5bfe\\u8c61\\u3002(F2)\\u8f03\\u6b63\\u3068\\u3057\\u3066\\u610f\\u5473\\u3092\\u6301\\u3064 shadow \\u5217\\u6319\\u306e\\u65e2\\u78ba\\u7acb\\u5024\\u3092\\u6301\\u3064 s4_settled54_v2\\uff08PSL(2,8)\\u7a93\\u3001\\u88c1\\u5b9a889/891/892\\uff09\\u3092\\u4ee3\\u7528\\u3057\\u305f -- \\u53f8\\u4ee4\\u5854\\u78ba\\u8a8d\\u4e8b\\u9805\\u3002\"",
    "}",
  "},",
  "\"deep15_windows\":[", JoinC(List(deep15Results, JDeep15Rec), ","), "],",
  "\"witness_1728_31095\":{",
    "\"note\":\"\\u672d7\\u306e\\u6700\\u5b89witness\\u3002delta=1(C\\u578b)\\u3067\\u3001\\u672c\\u8d70(delta>1 15\\u7a93)\\u3068\\u306f\\u5225\\u96c6\\u5408\\uff08\\u88c1\\u5b9a986\\u30011\\u3064\\u9078\\u3093\\u3067\\u5b9f\\u6e2c\\u30b3\\u30b9\\u30c8\\u3092\\u8a18\\u9332\\uff08\\u672d7\\u8cbb\\u7528\\u5f0f\\u306e\\u8f03\\u6b63\\u5b9f\\u6e2c1\\u70b9\\uff09\\u3002\",",
    JRunResult(witnessResult), ",",
    "\"cost\":{\"wall_ms\":", String(witnessWallMs), ",\"cpu_ms\":", String(witnessCpuMs),
      ",\"gasman_live_kb_before\":", String(witnessMemKbLiveBefore),
      ",\"gasman_live_kb_after\":", String(witnessMemKbLiveAfter), "}",
  "},",
  "\"u_touched\":false,",
  "\"no_verdict_note\":\"raw window/shadow/kernel/center data and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002UNKNOWN \\u306f\\u4e00\\u7d1a\\u306e\\u7d50\\u679c\\u3002\",",
  "\"elapsed_wall_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  "}"
);;

WriteFile("search/certs/iso_census83_deep15_v1_20260812.json", out);;
Print("\nWrote search/certs/iso_census83_deep15_v1_20260812.json\n");
Print("ISO_CENSUS83_DEEP15_DONE\n");
QUIT;
