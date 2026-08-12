## search/at4_qstab_coarsen_v1.g -- 発案7号 札AT-4(Q-STAB 粗化検定) 裁定1088実行
##
## 正本: docs/notes/ideas_arith_torsor_v1.md 札AT-4「検証の一手目」節。
##   源 = 既列挙48元([1008,521] slot1)・粗い側 H = B3/N(位数1008)の正規部分群で
##   PB3/N(位数168)内の最小非自明なものを1つ取り、その preimage を H とする。
##
## 測定する2項目(どちらに転んでも一級・生死判定はしない):
##   (a) settled 24元の像が H-settled か(Q-STAB 直接検定):
##       H-settled := Aut(P_H) の対角作用で (x_H, y_H)(= m=0,f=1 の像)と共役なクラス。
##   (b) 2類(settled/non-settled)の行き先の類が類ごとに一定か(類写像の well-defined 性):
##       48元全体を Aut(P_H) 軌道で分類し、元の2クラスの各メンバーが同一H-クラスに
##       揃うかを全数検査。
##
## 規律: u/c 非接触(m の範囲・f の値のみ操作、u=2m+1 は charming/marking のみ)。
##   marked-factor-map 法を踏襲(GAP の部分群比較でなく Aut(PN)/Aut(P_H) 軌道)。

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

## generic marked-factor-map classifier: takes a list of rec(genA:=.., genB:=..) pairs
## (already in the ambient group Q) and classifies them under the diagonal Aut(Q) action.
ClassifyPairsGeneric := function(Q, pairs)
  local Aut, autElts, classes, assigned, i, j, gA, gB, hA, hB, found, al, members, out;
  Aut := AutomorphismGroup(Q);;
  autElts := Elements(Aut);;
  classes := [];;
  assigned := List([1 .. Length(pairs)], k -> false);;
  for i in [1 .. Length(pairs)] do
    if assigned[i] then continue; fi;
    gA := pairs[i].genA;;  gB := pairs[i].genB;;
    members := [i];;
    assigned[i] := true;;
    for j in [i+1 .. Length(pairs)] do
      if assigned[j] then continue; fi;
      hA := pairs[j].genA;;  hB := pairs[j].genB;;
      found := false;;
      for al in autElts do
        if Image(al, gA) = hA and Image(al, gB) = hB then found := true; break; fi;
      od;
      if found then Add(members, j); assigned[j] := true; fi;
    od;
    Add(classes, rec(rep_index := i, size := Length(members), members := members));;
  od;
  out := rec(aut_order := Size(Aut), num_classes := Length(classes), classes := classes);;
  return out;
end;;

Print("############################################################\n");
Print("# at4_qstab_coarsen_v1.g -- AT-4 Q-STAB 粗化検定(裁定1088)\n");
Print("############################################################\n");

## ================= 源: [1008,521] slot1 の48 shadow(既存 fixture と同一構成) =================
Print("\n=== 源: [1008,521] slot1 の 48 shadow を再構成 ===\n");
Read("search/iso_census83_deep15_data.g");;
entryFix := DEEP15[1];;
if entryFix.id <> [1008, 521] then
  Error("at4: DEEP15[1].id != [1008,521], got ", entryFix.id);
fi;
W := BuildWindowFromWords(entryFix.index, entryFix.words);;
Print("  |Bq|=", Size(W.Bq), " |PN|=", Size(W.PN), " N_ord=", W.Nord, " z(order of c)=", Order(W.c), "\n");

charmingSetFix := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
corrFix := CorrectedShadows(W, charmingSetFix);;
shadowsFix := List(corrFix, sh -> rec(m := sh[1], f := sh[2]));;
Print("  shadow_total=", Length(shadowsFix), " (期待 48)\n");
if Length(shadowsFix) <> 48 then
  Error("at4: shadow_total != 48, refusing to proceed (fixture mismatch)");
fi;

## classify by marked-factor-map on PN, to recover the settled(rep_m=0) / non-settled(rep_m=2)
## split by index -- same method as set_surgery_fixture_v1.g's check_a
pairsN := List(shadowsFix, sh -> rec(m := sh.m, f := sh.f,
              genA := W.x^(2*sh.m+1),
              genB := AbstractProd([sh.f^-1, W.y^(2*sh.m+1), sh.f])));;
classNresult := ClassifyPairsGeneric(W.PN, pairsN);;
Print("  N-level classification: num_classes=", classNresult.num_classes,
      " class_sizes=", List(classNresult.classes, c -> c.size), "\n");
if classNresult.num_classes <> 2 then
  Error("at4: expected 2 N-level classes (settled/non-settled), got ", classNresult.num_classes);
fi;
## identify which class is settled (contains shadow index 1, which is m=0,f=identity by
## construction order -- verify explicitly rather than assume)
settledNClassIdx := 0;;
for i in [1 .. Length(classNresult.classes)] do
  if 1 in classNresult.classes[i].members then settledNClassIdx := i; fi;
od;
if settledNClassIdx = 0 or shadowsFix[1].m <> 0 or shadowsFix[1].f <> Identity(W.PN) then
  Error("at4: shadow index 1 is not the expected (m=0,f=1) settled representative");
fi;
nonsettledNClassIdx := 3 - settledNClassIdx;;  ## the other of {1,2}
Print("  settled N-class index=", settledNClassIdx, " size=", classNresult.classes[settledNClassIdx].size,
      " ; non-settled N-class index=", nonsettledNClassIdx, " size=", classNresult.classes[nonsettledNClassIdx].size, "\n");

## ================= 粗化: H := B3/N の正規部分群のうち PN 内で最小非自明なもの =================
Print("\n=== 粗化側 H の構成 ===\n");
Bq := W.Bq;;  PNgrp := W.PN;;
allNsubs := NormalSubgroups(Bq);;
candNsubs := Filtered(allNsubs, K -> IsSubgroup(PNgrp, K) and Size(K) > 1);;
Print("  candidate normal subgroups of Bq inside PN (size>1): sizes=", Set(List(candNsubs, Size)), "\n");
if Length(candNsubs) = 0 then
  Error("at4: no nontrivial normal subgroup of Bq lies inside PN -- coarsening construction fails, reporting UNKNOWN");
fi;
minSize := Minimum(List(candNsubs, Size));;
HbarCandidates := Filtered(candNsubs, K -> Size(K) = minSize);;
Hbar := HbarCandidates[1];;
Print("  |Hbar| (minimal nontrivial normal subgroup of Bq inside PN) = ", Size(Hbar),
      " (", Length(HbarCandidates), " candidate(s) of this size, took the first)\n");

natHom := NaturalHomomorphismByNormalSubgroup(Bq, Hbar);;
QBq := Image(natHom);;
xH := Image(natHom, W.x);;
yH := Image(natHom, W.y);;
PH := Group(xH, yH);;
Print("  |B3/H| = |Bq/Hbar| = ", Size(QBq), "  |P_H| = ", Size(PH), "\n");

## ================= 押し出し R_{N,H}: 全48 shadow を H に落とす =================
Print("\n=== 押し出し R_{N,H} と分類 ===\n");
pairsH := List(shadowsFix, sh -> rec(m := sh.m,
              genA := xH^(2*sh.m+1),
              genB := AbstractProd([Image(natHom, sh.f)^-1, yH^(2*sh.m+1), Image(natHom, sh.f)])));;

classHresult := ClassifyPairsGeneric(PH, pairsH);;
Print("  H-level classification: num_classes=", classHresult.num_classes,
      " class_sizes=", List(classHresult.classes, c -> c.size), "\n");

## H-settled class = the class containing shadow index 1 (m=0,f=1 -> genA=xH,genB=yH by construction)
HsettledClassIdx := 0;;
for i in [1 .. Length(classHresult.classes)] do
  if 1 in classHresult.classes[i].members then HsettledClassIdx := i; fi;
od;
Print("  H-settled class index=", HsettledClassIdx, " size=", classHresult.classes[HsettledClassIdx].size, "\n");

## (a) settled N-class (24 members) -- how many of their H-images land in the H-settled class?
settledNmembers := classNresult.classes[settledNClassIdx].members;;
settledLandInHsettled := Filtered(settledNmembers, idx -> idx in classHresult.classes[HsettledClassIdx].members);;
qstabDirectCount := Length(settledLandInHsettled);;
qstabDirectTotal := Length(settledNmembers);;
Print("[a] settled N-shadows whose H-image lands in H-settled class: ", qstabDirectCount, "/", qstabDirectTotal, "\n");

## (b) well-definedness of the class map: for each N-class, do ALL members land in the SAME
## H-class? (regardless of whether that H-class is H-settled or not)
CheckHomogeneous := function(Nmembers)
  local hclassOf, idx, k, found;
  hclassOf := [];;
  for idx in Nmembers do
    found := 0;;
    for k in [1 .. Length(classHresult.classes)] do
      if idx in classHresult.classes[k].members then found := k; fi;
    od;
    Add(hclassOf, found);;
  od;
  return rec(h_classes_hit := Set(hclassOf), homogeneous := (Length(Set(hclassOf)) = 1));;
end;;

settledMapCheck := CheckHomogeneous(settledNmembers);;
nonsettledNmembers := classNresult.classes[nonsettledNClassIdx].members;;
nonsettledMapCheck := CheckHomogeneous(nonsettledNmembers);;
Print("[b] settled N-class -> H-classes hit: ", settledMapCheck.h_classes_hit,
      " homogeneous=", settledMapCheck.homogeneous, "\n");
Print("[b] non-settled N-class -> H-classes hit: ", nonsettledMapCheck.h_classes_hit,
      " homogeneous=", nonsettledMapCheck.homogeneous, "\n");
classMapWellDefined := settledMapCheck.homogeneous and nonsettledMapCheck.homogeneous;;
Print("[b] class map well-defined overall (both N-classes land homogeneously): ", classMapWellDefined, "\n");
qstabAllSettledLandSame := (settledMapCheck.homogeneous and Length(settledLandInHsettled) = qstabDirectTotal);;
Print("[a] Q-STAB direct (all 24 settled land in H-settled, and only there): ", qstabAllSettledLandSame, "\n");

## ================= JSON output =================
JIntList := function(l) return JArr(List(l, String)); end;;

JClassSizeRec := function(cl) return String(cl.size); end;;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/at4_qstab_coarsen_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/at4_qstab_coarsen_v1.g\",\"order\":\"裁定1088(発案7号札AT-4 Q-STAB粗化検定)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/ideas_arith_torsor_v1.md 札AT-4 3.(検証の一手目)\"",
  ",\"window\":\"[1008,521] slot1 (search/iso_census83_deep15_data.g DEEP15[1])\"",
  ",\"n_source\":{\"bq_order\":", String(Size(W.Bq)), ",\"pn_order\":", String(Size(W.PN)),
    ",\"n_ord\":", String(W.Nord), ",\"shadow_total\":", String(Length(shadowsFix)), "}",
  ",\"n_level_classes\":{\"num_classes\":", String(classNresult.num_classes),
    ",\"class_sizes\":", JIntList(List(classNresult.classes, c -> c.size)),
    ",\"settled_class_index\":", String(settledNClassIdx),
    ",\"settled_class_size\":", String(classNresult.classes[settledNClassIdx].size),
    ",\"nonsettled_class_size\":", String(classNresult.classes[nonsettledNClassIdx].size), "}",
  ",\"coarsening_H\":{\"candidate_normal_subgroup_sizes_in_PN\":", JIntList(Set(List(candNsubs, Size))),
    ",\"num_minimal_candidates\":", String(Length(HbarCandidates)),
    ",\"hbar_order\":", String(Size(Hbar)),
    ",\"bq_over_hbar_order\":", String(Size(QBq)),
    ",\"ph_order\":", String(Size(PH)), "}",
  ",\"h_level_classes\":{\"num_classes\":", String(classHresult.num_classes),
    ",\"class_sizes\":", JIntList(List(classHresult.classes, c -> c.size)),
    ",\"h_settled_class_index\":", String(HsettledClassIdx),
    ",\"h_settled_class_size\":", String(classHresult.classes[HsettledClassIdx].size), "}",
  ",\"check_a_qstab_direct\":{\"settled_landing_in_h_settled\":", String(qstabDirectCount),
    ",\"settled_total\":", String(qstabDirectTotal),
    ",\"all_settled_land_in_h_settled_and_only_there\":", JB(qstabAllSettledLandSame), "}",
  ",\"check_b_class_map_welldefined\":{",
    "\"settled_h_classes_hit\":", JIntList(settledMapCheck.h_classes_hit),
    ",\"settled_homogeneous\":", JB(settledMapCheck.homogeneous),
    ",\"nonsettled_h_classes_hit\":", JIntList(nonsettledMapCheck.h_classes_hit),
    ",\"nonsettled_homogeneous\":", JB(nonsettledMapCheck.homogeneous),
    ",\"overall_well_defined\":", JB(classMapWellDefined), "}",
  ",\"u_touched\":true,\"u_touch_note\":\"u=2m+1 charming coordinate reused from existing marking (same object as set_surgery_fixture_v1 cert), not the sealed K(5) instance quantity\"",
  ",\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  "}"
);;

outPath := "search/certs/at4_qstab_coarsen_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
QUIT;
