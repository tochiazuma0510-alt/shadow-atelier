## search/meas_chi_83win_v1.g -- CHI-MODULAR-83 (札6, docs/notes/ideas_chidoor_83win_v1.md 札6,
## 検分 docs/notes/win83_audit_and_unram3_v1.md I.3 "GO", 委嘱: 司令塔発注 2026-08-12).
##
## Flows search/meas_chi_m5_v1.g's mechanism (ChiefSeries -> per-factor (p,dim,|G/C_G(W)|,
## ord_chi_w) via ActionHomomorphism, dim=1 special case only) onto the 15 delta>1 ("A-type",
## e=6, deep c-notin-N) windows from search/certs/zcensus83_v2_20260812.json's target83_detail.
##
## SCOPE (拘束の明記):
##  - dim=1 factors only get ord_chi_w (Aut(F_p) cyclic special case). dim>=2 / non-abelian
##    factors report (p,dim,|G/C_G(W)|) with ord_chi_w=null (same null-bookkeeping convention as
##    search/pchi1_v2.g / search/meas_chi_m5_v1.g -- CHI-CARRY, REP-3CLASS avoidance).
##  - This is a DESCRIPTIVE census only. No prediction is frozen here. No verdict language.
##  - If ord_chi_w > 6 appears for some factor, that is NOT written up as a break of any
##    SEC-MOD weak form (CHI-CARRY: this predicate's object is a chief-factor conjugation
##    character, a DIFFERENT object from SEC-MOD's normal-section + det construction -- 検分
##    I.3 / 札6 self-disclosure). Recorded raw only.
##  - u is not touched anywhere in this script.
##
## POSITIVE CONTROL (裁定961 mandatory), TWO PARTS:
##  (P1) M5 (G=B3/M5, order 3240) vs the ALREADY-COMMITTED cert search/certs/
##       meas_chi_m5_v1_20260811.json: M5 is reconstructed here via the SAME direct permutation
##       group path (BuildQTGeneral, verbatim-copied from search/meas_chi_m5_v1.g /
##       search/week3-M5-explorer.g) that already established the THEOREM-backed prediction
##       P-CHI-M5 (max ord(chi_W) over dim=1 factors divides 2, docs/notes/card_pchi_m5_v1.md
##       SS2.1/2.2 TWIST-GCD). Its fresh chief-factor data (via THIS script's MeasureAllFactorsG,
##       a reimplementation) is compared against the values already recorded in that committed
##       cert -- known/theorem-backed external ground truth. NOTE: order 3240 = 2^3*3^4*5 exceeds
##       GAP's SmallGroups library range (IdGroup errors "identification ... not available"), so
##       M5 itself CANNOT be used for a fresh SmallGroup(id)-reconstruction dual-path check (that
##       is exactly why part P2 below uses a smaller in-library object instead).
##  (P2) K^(3) (BuildPn3(3), order 108, the SAME known calibration window already used as the
##       dry-run object in search/iso_census83_skeleton_v1.g) reconstructed via TWO independent
##       paths within this script: path A = direct permutation group (BuildPn3(3)); path B =
##       SmallGroup(IdGroup(path-A-group)) reconstruction -- the SAME isomorphism-type lookup
##       method used for the 83-window census below. This exercises the actual SmallGroup(id)
##       mechanism the census relies on, in-library-range.
## Any mismatch in either part is reported as a machine fact (positive_control.*), not silently
## assumed, and stops the script before touching the 83-window targets (Error()).
##
## Window data source (target83_detail, delta>1 entries only -- 15 records, verbatim copied from
## the COMMITTED cert search/certs/zcensus83_v2_20260812.json; id_group/e/z/z_ab/delta values are
## the cert's own machine-computed fields, not re-derived here -- this script only adds the
## chief-factor / chi measurement layer on top of already-committed id_group values):
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

## ============ generic chief-factor measurement (verbatim pattern, search/pchi1_v2.g /
## search/meas_chi_m5_v1.g -- takes an already-constructed group G, no filter, dim=1 special case) ============
MeasureAllFactorsG := function(G)
  local cs, out, i, N1, N2, wSize, nat, Q, isElemAb, pVal, dimVal, actFun, hom, imgOrd, ordChiW;
  cs := ChiefSeries(G);
  out := [];
  for i in [1..Length(cs)-1] do
    N1 := cs[i];  N2 := cs[i+1];
    wSize := Size(N1)/Size(N2);
    nat := NaturalHomomorphismByNormalSubgroup(N1, N2);
    Q := Image(nat);
    isElemAb := IsElementaryAbelian(Q);
    pVal := fail;  dimVal := fail;
    if isElemAb and wSize > 1 then
      pVal := FactorsInt(wSize)[1];
      dimVal := LogInt(wSize, pVal);
    fi;
    actFun := function(q, g)
      local n;
      n := PreImagesRepresentative(nat, q);
      return Image(nat, n^g);
    end;
    hom := ActionHomomorphism(G, Elements(Q), actFun);
    imgOrd := Size(Image(hom));
    ordChiW := fail;
    if dimVal = 1 then ordChiW := imgOrd; fi;
    Add(out, rec(factor_index:=i, w_size:=wSize, is_elementary_abelian:=isElemAb,
                 p:=pVal, dim:=dimVal, g_mod_cg_w:=imgOrd, ord_chi_w:=ordChiW));
  od;
  return out;
end;;

DimSummary := function(factorRecs)
  local dim1Recs, dim1Orders, maxOrdDim1, dimGe2Recs, nonAbelianRecs;
  dim1Recs := Filtered(factorRecs, r -> r.dim = 1);
  dim1Orders := List(dim1Recs, r -> r.ord_chi_w);
  maxOrdDim1 := 0;
  if Length(dim1Orders) > 0 then maxOrdDim1 := Maximum(dim1Orders); fi;
  dimGe2Recs := Filtered(factorRecs, r -> r.is_elementary_abelian and r.dim <> fail and r.dim >= 2);
  nonAbelianRecs := Filtered(factorRecs, r -> not r.is_elementary_abelian);
  return rec(max_ord_dim1:=maxOrdDim1, dim1_orders:=dim1Orders,
             dimGe2_count:=Length(dimGe2Recs), nonabelian_count:=Length(nonAbelianRecs));
end;;

CanonFactorStrs := function(factorRecs)
  local strs;
  strs := List(factorRecs, r -> Concatenation(String(r.w_size), ":", String(r.p), ":",
                                               String(r.dim), ":", String(r.g_mod_cg_w), ":",
                                               String(r.ord_chi_w)));
  Sort(strs);
  return strs;
end;;

## ============ positive control: M5 dual-path reconstruction ============
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y), r := r, s := s);
end;;

BuildQTGeneral := function(Qgrp, phiX, phiY, phiC)
  local Qelts, posDict, posOf, phiXi, phiYi, np, imgS1, imgS2, t, i, d, pt, val, tp;
  Qelts := Elements(Qgrp);
  np := Length(Qelts);
  posDict := NewDictionary(Qelts[1], true);
  for i in [1..np] do AddDictionary(posDict, Qelts[i], i); od;
  posOf := function(v) return LookupDictionary(posDict, v); end;
  phiXi := phiX^-1;  phiYi := phiY^-1;
  imgS1 := [];;  imgS2 := [];;
  for t in [1..6] do
    for i in [1..np] do
      d := Qelts[i];  pt := (t-1)*np + i;
      if t=1 then val:=d; tp:=2;
      elif t=2 then val:=d*phiX; tp:=1;
      elif t=3 then val:=d; tp:=5;
      elif t=4 then val:=d; tp:=6;
      elif t=5 then val:=d*phiXi*phiYi*phiC; tp:=3;
      else val:=d*phiY; tp:=4; fi;
      imgS1[pt] := (tp-1)*np + posOf(val);
      if t=1 then val:=d; tp:=3;
      elif t=2 then val:=d; tp:=4;
      elif t=3 then val:=d*phiY; tp:=1;
      elif t=4 then val:=d*phiYi*phiXi*phiC; tp:=2;
      elif t=5 then val:=d; tp:=6;
      else val:=d*phiX; tp:=5; fi;
      imgS2[pt] := (tp-1)*np + posOf(val);
    od;
  od;
  return rec(s1:=PermList(imgS1), s2:=PermList(imgS2), np:=np, elts:=Qelts, posOf:=posOf);
end;;

gnM5 := MakeGn(3);;
tPermM5 := PermList(Concatenation([2..5],[1]));;
ShiftC5M5 := function(p) return PermList(Concatenation(List([1..9],j->j), List([1..5], j -> 9 + (j^p)))); end;;
xhatM5 := gnM5.x * ShiftC5M5(tPermM5^2);;
yhatM5 := gnM5.y * ShiftC5M5(tPermM5^2);;
chatM5 := ShiftC5M5(tPermM5);;
QMm5 := Group(xhatM5, yhatM5);;
qtM5 := BuildQTGeneral(QMm5, xhatM5, yhatM5, chatM5);;
GM5direct := Group(qtM5.s1, qtM5.s2);;
gm5Order := Size(GM5direct);;
if gm5Order <> 3240 then Error("positive control P1: GM5direct order mismatch: got ", gm5Order); fi;

factorsM5Fresh := MeasureAllFactorsG(GM5direct);;
summaryM5Fresh := DimSummary(factorsM5Fresh);;
canonM5Fresh := CanonFactorStrs(factorsM5Fresh);;

## ground truth: verbatim from the COMMITTED cert search/certs/meas_chi_m5_v1_20260811.json's
## "chief_factors" array (THEOREM-backed P-CHI-M5 measurement, docs/notes/card_pchi_m5_v1.md).
M5_COMMITTED_FACTORS := [
  rec(factor_index:=1, w_size:=2,  is_elementary_abelian:=true, p:=2, dim:=1, g_mod_cg_w:=1,  ord_chi_w:=1),
  rec(factor_index:=2, w_size:=3,  is_elementary_abelian:=true, p:=3, dim:=1, g_mod_cg_w:=2,  ord_chi_w:=2),
  rec(factor_index:=3, w_size:=4,  is_elementary_abelian:=true, p:=2, dim:=2, g_mod_cg_w:=6,  ord_chi_w:=fail),
  rec(factor_index:=4, w_size:=27, is_elementary_abelian:=true, p:=3, dim:=3, g_mod_cg_w:=24, ord_chi_w:=fail),
  rec(factor_index:=5, w_size:=5,  is_elementary_abelian:=true, p:=5, dim:=1, g_mod_cg_w:=1,  ord_chi_w:=1)
];;
canonM5Committed := CanonFactorStrs(M5_COMMITTED_FACTORS);;
p1Match := (canonM5Fresh = canonM5Committed);;
p1AgreesTheorem := (summaryM5Fresh.max_ord_dim1 = 2);;

Print("[positive control P1] M5 fresh-vs-committed: fresh_max_ord_dim1=", summaryM5Fresh.max_ord_dim1,
      " committed_match=", p1Match, " agrees_P_CHI_M5_theorem=", p1AgreesTheorem, "\n");
if not p1Match then
  Error("POSITIVE CONTROL P1 FAILED: fresh M5 chief-factor data does not match the committed meas_chi_m5_v1_20260811.json cert -- measurement pipeline bug, stopping before touching the 83-window targets");
fi;
if not p1AgreesTheorem then
  Error("POSITIVE CONTROL P1 FAILED: fresh M5 max_ord_dim1 != 2, contradicting P-CHI-M5 theorem -- stopping before touching the 83-window targets");
fi;

## ---- P2: K^(3) (order 108, search/iso_census83_skeleton_v1.g's own calibration window) --
## dual-path check of the ACTUAL SmallGroup(id) mechanism the 83-window census below relies on.
BuildPn3ForControl := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, Gfull;
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
  Gfull := Group(a1,a2,a3,q1,q2);
  return Gfull;
end;;

K3direct := BuildPn3ForControl(3);;
k3OrderA := Size(K3direct);;
if k3OrderA <> 108 then Error("positive control P2: K3direct order mismatch: got ", k3OrderA); fi;
idK3 := IdGroup(K3direct);;
K3fromId := SmallGroup(idK3[1], idK3[2]);;
k3OrderB := Size(K3fromId);;
if k3OrderB <> 108 then Error("positive control P2: K3fromId order mismatch: got ", k3OrderB); fi;

factorsK3A := MeasureAllFactorsG(K3direct);;
factorsK3B := MeasureAllFactorsG(K3fromId);;
summaryK3A := DimSummary(factorsK3A);;
summaryK3B := DimSummary(factorsK3B);;
canonK3A := CanonFactorStrs(factorsK3A);;
canonK3B := CanonFactorStrs(factorsK3B);;
p2Match := (canonK3A = canonK3B);;

Print("[positive control P2] K^(3) dual-path: id_group=", idK3, " pathA_max_ord_dim1=", summaryK3A.max_ord_dim1,
      " pathB_max_ord_dim1=", summaryK3B.max_ord_dim1, " canon_match=", p2Match, "\n");
if not p2Match then
  Error("POSITIVE CONTROL P2 FAILED: K^(3) direct-construction vs SmallGroup(id) chief-factor data mismatch -- SmallGroup(id) reconstruction mechanism bug, stopping before touching the 83-window targets");
fi;

## ============ 15 delta>1 windows (target83_detail, source: search/certs/zcensus83_v2_20260812.json) ============
WINDOWS := [
  rec(index:=1008, id_group:=[1008,521],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=1),
  rec(index:=1008, id_group:=[1008,521],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=2),
  rec(index:=1008, id_group:=[1008,683],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=1),
  rec(index:=1008, id_group:=[1008,683],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=2),
  rec(index:=1134, id_group:=[1134,55],    e:=6, z:=3, z_ab:=1, delta:=3, twin_slot:=1),
  rec(index:=1134, id_group:=[1134,55],    e:=6, z:=3, z_ab:=1, delta:=3, twin_slot:=2),
  rec(index:=1134, id_group:=[1134,53],    e:=6, z:=3, z_ab:=1, delta:=3, twin_slot:=1),
  rec(index:=1134, id_group:=[1134,53],    e:=6, z:=3, z_ab:=1, delta:=3, twin_slot:=2),
  rec(index:=1152, id_group:=[1152,154161],e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=1),
  rec(index:=1152, id_group:=[1152,154163],e:=6, z:=4, z_ab:=1, delta:=4, twin_slot:=1),
  rec(index:=1152, id_group:=[1152,154163],e:=6, z:=4, z_ab:=1, delta:=4, twin_slot:=2),
  rec(index:=1872, id_group:=[1872,568],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=1),
  rec(index:=1872, id_group:=[1872,568],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=2),
  rec(index:=1872, id_group:=[1872,780],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=1),
  rec(index:=1872, id_group:=[1872,780],   e:=6, z:=2, z_ab:=1, delta:=2, twin_slot:=2)
];;

if Length(WINDOWS) <> 15 then Error("WINDOWS list length != 15, got ", Length(WINDOWS)); fi;

winResults := [];;
allDim1OrdsAll := [];;
maxOrdOverall := 0;;
anyOrdGt6 := false;;
for w in WINDOWS do
  G := SmallGroup(w.id_group[1], w.id_group[2]);;
  if Size(G) <> w.index then
    Error("window order mismatch: id_group=", w.id_group, " Size(G)=", Size(G), " expected index=", w.index);
  fi;
  factorRecs := MeasureAllFactorsG(G);;
  summ := DimSummary(factorRecs);;
  Add(winResults, rec(w:=w, factors:=factorRecs, summary:=summ));
  for v in summ.dim1_orders do
    Add(allDim1OrdsAll, v);
    if v > maxOrdOverall then maxOrdOverall := v; fi;
    if 6 mod v <> 0 then anyOrdGt6 := true; fi;
  od;
  Print("window index=", w.index, " id_group=", w.id_group, " e=", w.e, " z=", w.z, " delta=", w.delta,
        " max_ord_dim1=", summ.max_ord_dim1, " dim1_orders=", summ.dim1_orders,
        " dimGe2_count=", summ.dimGe2_count, " nonabelian_count=", summ.nonabelian_count, "\n");
od;

Print("overall: total_windows=", Length(WINDOWS), " max_ord_dim1_overall=", maxOrdOverall,
      " any_ord_not_dividing_6=", anyOrdGt6, "\n");

## ============ JSON output ============
JFactorRec := function(r)
  local pStr, dimStr, ordStr;
  if r.p = fail then pStr := "null"; else pStr := String(r.p); fi;
  if r.dim = fail then dimStr := "null"; else dimStr := String(r.dim); fi;
  if r.ord_chi_w = fail then ordStr := "null"; else ordStr := String(r.ord_chi_w); fi;
  return Concatenation("{",
    "\"factor_index\":", String(r.factor_index), ",",
    "\"w_size\":", String(r.w_size), ",",
    "\"is_elementary_abelian\":", JB(r.is_elementary_abelian), ",",
    "\"p\":", pStr, ",",
    "\"dim\":", dimStr, ",",
    "\"g_mod_cg_w\":", String(r.g_mod_cg_w), ",",
    "\"ord_chi_w\":", ordStr,
    "}");
end;;

JWindowRec := function(r)
  return Concatenation("{",
    "\"index\":", String(r.w.index), ",",
    "\"id_group\":", JPair(r.w.id_group[1], r.w.id_group[2]), ",",
    "\"e\":", String(r.w.e), ",",
    "\"z\":", String(r.w.z), ",",
    "\"z_ab\":", String(r.w.z_ab), ",",
    "\"delta\":", String(r.w.delta), ",",
    "\"twin_slot\":", String(r.w.twin_slot), ",",
    "\"chief_factors\":[", JoinC(List(r.factors, JFactorRec), ","), "],",
    "\"dim1_summary\":{",
      "\"max_ord_dim1\":", String(r.summary.max_ord_dim1), ",",
      "\"dim1_orders\":", JArr(List(r.summary.dim1_orders, String)), "},",
    "\"dimGe2_factors_count\":", String(r.summary.dimGe2_count), ",",
    "\"nonabelian_factors_count\":", String(r.summary.nonabelian_count),
    "}");
end;;

JFactorList := function(recs) return JArr(List(recs, JFactorRec)); end;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/meas_chi_83win_v1\",",
  "\"authority\":\"\\u53f8\\u4ee4\\u5854\\u767a\\u6ce8 2026-08-12 \\u672d6 CHI-MODULAR-83 (\\u691c\\u5206 docs/notes/win83_audit_and_unram3_v1.md I.3 GO)\",",
  "\"domain_note\":\"15 delta>1 (A-type, e=6, deep c-notin-N) window records from target83_detail, search/certs/zcensus83_v2_20260812.json (id_group/e/z/z_ab/delta verbatim from that committed cert; 8 distinct isomorphism types across 15 window records due to twin-pair duplication in the source census, per that cert's own '\\u53cc\\u8a18\\u9332\\u9650\\u5b9a' convention).\",",
  "\"mechanism_note\":\"MeasureAllFactorsG = ChiefSeries(G) + per-factor conjugation-action ActionHomomorphism, no filter, ord_chi_w reported only when dim=1 (Aut(F_p) cyclic special case) -- verbatim pattern of search/meas_chi_m5_v1.g / search/pchi1_v2.g. Purely a function of the isomorphism type SmallGroup(id_group); does not touch B3 presentation, theta/tau, or c at all (independent of the theta word-level-vs-quotient question raised for \\u672d3).\",",
  "\"positive_control\":{",
    "\"p1_m5_vs_committed\":{",
      "\"object\":\"M5 (G=B3/M5, order 3240), reconstructed here via the SAME BuildQTGeneral direct-permutation-group path as search/meas_chi_m5_v1.g\",",
      "\"note\":\"order 3240 exceeds GAP SmallGroups library range (IdGroup errors), so no fresh SmallGroup(id) dual-path is possible for M5 itself -- compared instead against the already-committed cert's chief_factors array (external theorem-backed ground truth)\",",
      "\"committed_cert_ref\":\"search/certs/meas_chi_m5_v1_20260811.json\",",
      "\"fresh_max_ord_dim1\":", String(summaryM5Fresh.max_ord_dim1), ",",
      "\"fresh_factors\":", JFactorList(factorsM5Fresh), ",",
      "\"committed_factors\":", JFactorList(M5_COMMITTED_FACTORS), ",",
      "\"canon_multiset_match\":", JB(p1Match), ",",
      "\"agrees_P_CHI_M5_theorem\":", JB(p1AgreesTheorem), ",",
      "\"P_CHI_M5_theorem_ref\":\"docs/notes/card_pchi_m5_v1.md \\u00a72.1/2.2 TWIST-GCD: max ord(chi_W) over dim=1 factors divides 2\"",
    "},",
    "\"p2_k3_dual_path\":{",
      "\"object\":\"K^(3) (BuildPn3(3), order 108, the calibration window already used in search/iso_census83_skeleton_v1.g), reconstructed via TWO independent paths within this script\",",
      "\"path_a\":\"direct permutation group via BuildPn3(3)\",",
      "\"path_b\":\"SmallGroup(IdGroup(path_a_group)) reconstruction -- the SAME mechanism used for the 83-window census below\",",
      "\"id_group\":", JPair(idK3[1], idK3[2]), ",",
      "\"path_a_max_ord_dim1\":", String(summaryK3A.max_ord_dim1), ",",
      "\"path_b_max_ord_dim1\":", String(summaryK3B.max_ord_dim1), ",",
      "\"path_a_factors\":", JFactorList(factorsK3A), ",",
      "\"path_b_factors\":", JFactorList(factorsK3B), ",",
      "\"canon_multiset_match\":", JB(p2Match),
    "}",
  "},",
  "\"windows\":[", JoinC(List(winResults, JWindowRec), ","), "],",
  "\"overall_summary\":{",
    "\"total_windows\":", String(Length(WINDOWS)), ",",
    "\"max_ord_dim1_overall\":", String(maxOrdOverall), ",",
    "\"any_ord_not_dividing_6\":", JB(anyOrdGt6),
  "},",
  "\"chi_carry_note\":\"\\u4f4d\\u6570 >6 \\u304c\\u51fa\\u3066\\u3082 SEC-MOD \\u5f31\\u5f62\\u306e\\u7834\\u308c\\u3067\\u306f\\u306a\\u3044(\\u5bfe\\u8c61\\u304c\\u5225 -- CHI-CARRY\\u3001\\u691c\\u5206 I.3\\u30fb\\u672d6\\u81ea\\u5df1\\u7533\\u544a\\u3069\\u304a\\u308a)\\u3002\\u8a18\\u8ff0\\u7d71\\u8a08\\u306e\\u307f\\u3002\",",
  "\"u_touched\":false,",
  "\"no_verdict_note\":\"raw chief-factor data (p,dim,w_size,is_elementary_abelian,g_mod_cg_w,ord_chi_w) and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\",",
  "\"elapsed_wall_ms\":", String(GAPLIB_WallElapsedMs()),
  "}"
);;

WriteFile("search/certs/meas_chi_83win_v1_20260812.json", out);;
Print("Wrote search/certs/meas_chi_83win_v1_20260812.json\n");
Print("MEAS_CHI_83WIN_DONE\n");
QUIT;
