## search/m5_win_chk_v1.g -- M5-WIN-CHK (裁定803 [1], HA-GAP-3 最優先).
## Question: is M5 <= PB3, i.e. does B3/M5 (=G_M5, order 3240) admit a homomorphism to S3
## sending the images of sigma1,sigma2 (qt.s1,qt.s2, per the SAME BuildQTGeneral construction
## already used and verified in search/hcen_ab_v1.g, itself a verbatim-copied reconstruction of
## search/week3-M5-explorer.g's machinery -- NOT re-copied here a third time; this script
## re-derives it once more, independently, as its own self-contained measurement) to the SAME
## two transpositions (1,2),(2,3) used throughout this project's convention for the standard
## B3->S3 map. Existence of such a homomorphism is EXACTLY the statement "the composite
## B3 -> B3/M5 -> S3 (via qt.s1,qt.s2 |-> (1,2),(2,3)) equals the standard B3->S3 map", which
## holds iff M5 <= ker(standard B3->S3) = PB3 (M5 is normal in B3 by construction, being a
## kernel -- see week3-M5-explorer.g's own header comment).
## This is a STRONGER/DIRECT check than "e=|(B3/M5)^ab| even" (already measured =10 in
## search/certs/hcen_ab_v1_20260811.json -- that is only a NECESSARY condition per addendum_a
## theorem (I), since PB3 properly sits inside ker(B3->Z/2) -- exponent-sum parity alone would
## only test membership in the LARGER subgroup ker(B3->S3^ab)=ker(B3->Z/2), not PB3 itself,
## which requires the FULL non-abelian S3 image to be trivial, not just even).
## Raw boolean result only. No verdict language.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

S3 := SymmetricGroup(3);;

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

## the direct window-compatibility test: does G_M5 admit a hom to S3 sending
## (image of sigma1, image of sigma2) = (qt.s1, qt.s2) to the standard transpositions?
hom := fail;;
if gm5OrderOk then
  hom := GroupHomomorphismByImages(GM5, S3, [qtM5.s1, qtM5.s2], [(1,2),(2,3)]);
fi;
m5InPB3 := (hom <> fail);;

## secondary/weaker necessary-condition cross-check: e = |(B3/M5)^ab| already measured = 10
## in search/certs/hcen_ab_v1_20260811.json (M5 control, abelian_invariants=[2,5]) -- recompute
## here independently (via DerivedSubgroup on the SAME G_M5 object) for a same-script sanity tie.
eVal := 0;;
eEven := false;;
if gm5OrderOk then
  Gab := GM5 / DerivedSubgroup(GM5);;
  invs := AbelianInvariants(Gab);;
  eVal := Product(invs, x->x, 1);;
  eEven := (eVal mod 2 = 0);;
fi;

Print("gm5Order=", gm5Order, " order_ok=", gm5OrderOk, "\n");
Print("M5_leq_PB3 (direct hom-to-S3 test) = ", m5InPB3, "\n");
Print("e = |(B3/M5)^ab| = ", eVal, " (even=", eEven, ", necessary-condition cross-check)\n");

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/m5_win_chk_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a803[1] (HA-GAP-3, docs/notes/hunting_chapter_v1_addendum_a.md \\u00a73/\\u00a77)\",",
  "\"method_note\":\"direct test: does G=B3/M5 (order 3240, reconstructed via BuildQTGeneral -- same construction independently re-derived here, verbatim-copied machinery from search/week3-M5-explorer.g / search/hcen_ab_v1.g) admit GroupHomomorphismByImages(G,S3,[image_of_sigma1,image_of_sigma2],[(1,2),(2,3)])? Existence <=> M5<=ker(standard B3->S3)=PB3 (M5 normal in B3, being a kernel by construction). STRONGER than the exponent-sum-parity/e-even necessary condition (that only tests membership in the larger ker(B3->S3^ab)=ker(B3->Z/2), not PB3 itself).\",",
  "\"order_of_B3_mod_M5\":", String(gm5Order), ",",
  "\"order_expected\":3240,",
  "\"order_ok\":", JB(gm5OrderOk), ",",
  "\"M5_leq_PB3\":", JB(m5InPB3), ",",
  "\"e_abelianization_order\":", String(eVal), ",",
  "\"e_even_necessary_condition\":", JB(eEven), ",",
  "\"cross_reference\":\"e=10 already measured in search/certs/hcen_ab_v1_20260811.json (M5_control.abelian_invariants=[2,5]) -- recomputed independently in this script for a same-run sanity tie, not imported.\",",
  "\"no_verdict_note\":\"raw boolean M5_leq_PB3 only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/m5_win_chk_v1_20260811.json", out);;
Print("Wrote search/certs/m5_win_chk_v1_20260811.json\n");
Print("M5_WIN_CHK_DONE\n");
QUIT;
