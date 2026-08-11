## search/meas_chi_m5_v1.g -- MEAS-CHI-M5 (裁定805, docs/notes/card_pchi_m5_v1.md SS5).
## G = B3/M5 (order 3240), reconstructed via the SAME BuildQTGeneral machinery independently
## re-derived once more (verbatim-copied from search/week3-M5-explorer.g, same pattern as
## search/hcen_ab_v1.g and search/m5_win_chk_v1.g -- each script rebuilds G_M5 from scratch
## rather than importing another search/ script, per this project's search-side conventions).
##
## For each chief factor W = N1/N2 of a ChiefSeries(G): report
##   p        = the characteristic (only meaningful if W is elementary abelian; if W is a
##              non-abelian chief factor, p and dim are reported as "n/a" and the raw order is
##              given instead -- disclosed, not silently coerced)
##   dim      = dim_Fp(W) = log_p(|W|), only if W is elementary abelian
##   G_mod_CG_W = |G / C_G(W)|, computed uniformly for ANY chief factor (abelian or not) via
##              ActionHomomorphism(G, Elements(W), conjugation-action-function); Size(Image(hom))
##   ord_chi_W = G_mod_CG_W when dim=1 (Aut(F_p) is cyclic, so the image order IS the twist
##              character's order -- same number, dim=1 special case only, per the card's own
##              request "ord(chi_W) [dim=1のときのみ]")
##
## Frozen prediction P-CHI-M5 (card_pchi_m5_v1.md §2.2, a THEOREM per TWIST-GCD, not a mere
## guess): max ord(chi_W) over 1-dim factors divides 2 (equivalently: 5 never divides
## ord(chi_W)). |G|=3240=2^3*3^4*5, so composition-factor characteristic p in {2,3,5} only, and
## gcd(e,p-1) for e=10: p=2->1, p=3->2, p=5->2 (upper bounds per TWIST-GCD).
## Canary role (card's own framing): if ord does NOT divide 2, treat as a measurement-pipeline
## bug signal FIRST (group identity / e recomputation / chief-factor characteristic), not as a
## disproof of the theorem -- reported raw regardless, no verdict language written here.
## Also reports (p,dim,|G/C_G(W)|) for dim>=2 factors (card §5 "同時に出すと価値が高い").
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

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
GM5 := Group(qtM5.s1, qtM5.s2);;
gm5Order := Size(GM5);;
gm5OrderOk := (gm5Order = 3240);;
if not gm5OrderOk then Error("G_M5 order mismatch: got ", gm5Order, " expected 3240"); fi;

cs := ChiefSeries(GM5);;
factorRecs := [];;

for i in [1..Length(cs)-1] do
  N1 := cs[i];  N2 := cs[i+1];
  wSize := Size(N1)/Size(N2);
  nat := NaturalHomomorphismByNormalSubgroup(N1, N2);
  Q := Image(nat);
  isElemAb := IsElementaryAbelian(Q);
  pVal := fail;;  dimVal := fail;;
  if isElemAb and wSize > 1 then
    pVal := FactorsInt(wSize)[1];
    dimVal := LogInt(wSize, pVal);
  fi;
  actFun := function(q, g)
    local n;
    n := PreImagesRepresentative(nat, q);
    return Image(nat, n^g);
  end;;
  hom := ActionHomomorphism(GM5, Elements(Q), actFun);;
  imgOrd := Size(Image(hom));;
  ordChiW := fail;;
  if dimVal = 1 then
    ordChiW := imgOrd;
  fi;
  Add(factorRecs, rec(factor_index:=i, w_size:=wSize, is_elementary_abelian:=isElemAb,
                       p:=pVal, dim:=dimVal, g_mod_cg_w:=imgOrd, ord_chi_w:=ordChiW));
  Print("factor ", i, ": |W|=", wSize, " elem_ab=", isElemAb, " p=", pVal, " dim=", dimVal,
        " |G/C_G(W)|=", imgOrd, " ord_chi_w=", ordChiW, "\n");
od;

dim1Recs := Filtered(factorRecs, r -> r.dim = 1);;
dim1Orders := List(dim1Recs, r -> r.ord_chi_w);;
maxOrdDim1 := 0;;
if Length(dim1Orders) > 0 then maxOrdDim1 := Maximum(dim1Orders); fi;
allDim1DivideBy2 := ForAll(dim1Orders, x -> (2 mod x) = 0);;
any5DividesOrd := ForAny(dim1Orders, x -> x mod 5 = 0);;

dimGe2Recs := Filtered(factorRecs, r -> r.is_elementary_abelian and r.dim <> fail and r.dim >= 2);;
nonAbelianRecs := Filtered(factorRecs, r -> not r.is_elementary_abelian);;
dimGe2WithFive := Filtered(dimGe2Recs, r -> r.g_mod_cg_w mod 5 = 0);;

Print("max_ord_dim1=", maxOrdDim1, " all_dim1_divide_2=", allDim1DivideBy2,
      " any_5_divides_ord=", any5DividesOrd, "\n");
Print("dimGe2_count=", Length(dimGe2Recs), " nonAbelian_count=", Length(nonAbelianRecs), "\n");

## ============ JSON output ============
JFactor := function(r)
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

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/meas_chi_m5_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a805 -- docs/notes/card_pchi_m5_v1.md \\u00a75 (MEAS-CHI-M5)\",",
  "\"domain_note\":\"single point: G=B3/M5, order 3240 (M5<=PB3 confirmed true, search/certs/m5_win_chk_v1_20260811.json, 115ffeb). Reconstructed independently via BuildQTGeneral (verbatim-copied machinery, 3rd independent re-derivation across search/hcen_ab_v1.g / search/m5_win_chk_v1.g / this script).\",",
  "\"order\":", String(gm5Order), ",",
  "\"order_expected\":3240,",
  "\"order_ok\":", JB(gm5OrderOk), ",",
  "\"P_CHI_M5_prediction\":\"THEOREM (TWIST-GCD, card_pchi_m5_v1.md SS2.1/2.2): max ord(chi_W) over dim=1 factors divides 2 (equivalently 5 never divides ord(chi_W))\",",
  "\"chief_factors\":[", JoinC(List(factorRecs, JFactor), ","), "],",
  "\"dim1_summary\":{",
    "\"max_ord_dim1\":", String(maxOrdDim1), ",",
    "\"all_dim1_divide_2\":", JB(allDim1DivideBy2), ",",
    "\"any_5_divides_ord\":", JB(any5DividesOrd),
  "},",
  "\"dimGe2_factors_count\":", String(Length(dimGe2Recs)), ",",
  "\"nonabelian_factors_count\":", String(Length(nonAbelianRecs)), ",",
  "\"dimGe2_with_5_in_g_mod_cg_w_count\":", String(Length(dimGe2WithFive)), ",",
  "\"no_verdict_note\":\"raw chief-factor data (p,dim,|G/C_G(W)|,ord) and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/meas_chi_m5_v1_20260811.json", out);;
Print("Wrote search/certs/meas_chi_m5_v1_20260811.json\n");
Print("MEAS_CHI_M5_DONE\n");
QUIT;
