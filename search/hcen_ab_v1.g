## search/hcen_ab_v1.g -- h^cen-AB (裁定795 4, 796, 798, 797(5)) "表読み" measurement.
## Scope (per commander's final clarification, 裁定797(5)):
##   target = census exotic 23 pairs (定義正本 = 裁定642/644; 構成 = 10(750-clique)+1(384/[384,608])
##   +12(index<384 both-fixed)). Source: search/certs/r6a_summary_v1_20260806.json (set_i_750_clique_B_members,
##   set_ii_lt384_pairs, classification=BOTH_FIXED) + search/certs/lins_twin_census_v1_20260806.json
##   (id_group per member, matched by pair-index ordering within the index<384 subset -- verified pair0
##   has index 24/id_group=[24,3] matching h^cen=24 SL(2,3) and pair30 has index 336/id_group=[336,208]
##   matching the single documented both-c-in-N exotic pair, per docs/notes/theorem_check_mirrorall_l3vacuous_v1.md
##   §G.6.b/§G.6.c -- both anchors confirm the join is correct).
## Task: for each of the 23 pairs, both members' quotient group G=SmallGroup(id_group), report
##   AbelianInvariants(G) raw, |G^ab|=d, and machine-checked booleans (is_cyclic, d_even, j=d/2 if
##   cyclic&even, j_divides_3) -- NO verdict language (raw values/booleans only; interpretation is
##   the commander's). This is a table-read (G^ab from an already-fixed finite group), NOT a predicate
##   evaluation on B3/N itself -- per hunting_chapter_v1.md §3.3, this does not touch T-1 (c∉N checker
##   moratorium), since no GTSh-theoretic predicate (hexagon/charming/settled/isolated/SURJ) is evaluated.
## M5 control (outside the 23-pair prediction set, explicitly flagged): G = B3/M5 (order 3240),
##   reconstructed via the QxT transversal-cocycle machinery copied VERBATIM from
##   search/week3-M5-explorer.g (MakeDn/MakeGn/BuildQTGeneral, calls: gn:=MakeGn(3); tPerm; ShiftC5;
##   xhat,yhat,chat; QM:=Group(xhat,yhat); qt:=BuildQTGeneral(QM,xhat,yhat,chat);
##   G_M5 := Group(qt.s1,qt.s2)) -- the frozen original script is NOT modified/re-run; this is an
##   independent minimal reconstruction of the same construction for the sole purpose of computing
##   AbelianInvariants(G_M5), with a sanity check that |G_M5|=3240 (matching the original script's own
##   documented expectation) before trusting the abelianization.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

## ============ 23-pair target list (data assembled+cross-checked from the two census certs above) ============
PAIRS := [
  rec(pair_fiber:="lt384:idx24:pair0",  index:=24,  m0_id:=[24,3],   m1_id:=[24,3]),
  rec(pair_fiber:="lt384:idx72:pair2",  index:=72,  m0_id:=[72,3],   m1_id:=[72,3]),
  rec(pair_fiber:="lt384:idx120:pair6", index:=120, m0_id:=[120,15], m1_id:=[120,15]),
  rec(pair_fiber:="lt384:idx120:pair7", index:=120, m0_id:=[120,5],  m1_id:=[120,5]),
  rec(pair_fiber:="lt384:idx168:pair11",index:=168, m0_id:=[168,22], m1_id:=[168,22]),
  rec(pair_fiber:="lt384:idx216:pair16",index:=216, m0_id:=[216,3],  m1_id:=[216,3]),
  rec(pair_fiber:="lt384:idx264:pair24",index:=264, m0_id:=[264,12], m1_id:=[264,12]),
  rec(pair_fiber:="lt384:idx312:pair27",index:=312, m0_id:=[312,25], m1_id:=[312,25]),
  rec(pair_fiber:="lt384:idx336:pair30",index:=336, m0_id:=[336,208],m1_id:=[336,208]),
  rec(pair_fiber:="lt384:idx336:pair35",index:=336, m0_id:=[336,114],m1_id:=[336,114]),
  rec(pair_fiber:="lt384:idx360:pair38",index:=360, m0_id:=[360,14], m1_id:=[360,14]),
  rec(pair_fiber:="lt384:idx360:pair39",index:=360, m0_id:=[360,51], m1_id:=[360,51]),
  rec(pair_fiber:="idx384:608",         index:=384, m0_id:=[384,608],m1_id:=[384,608]),
  rec(pair_fiber:="idx750:pair0", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair1", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair2", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair3", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair4", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair5", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair6", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair7", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair8", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair9", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
];;

MeasureAb := function(idpair)
  local G, Gab, invs, d, isCyclic, dEven, jVal, jDiv3;
  G := SmallGroup(idpair[1], idpair[2]);
  invs := AbelianInvariants(G);
  d := Product(invs, x -> x, 1);
  Gab := G / DerivedSubgroup(G);
  isCyclic := IsCyclic(Gab);
  dEven := (d mod 2 = 0);
  if isCyclic and dEven then
    jVal := d / 2;
    jDiv3 := (3 mod jVal = 0);
  else
    jVal := fail;
    jDiv3 := fail;
  fi;
  return rec(id_group:=idpair, invariants:=invs, d:=d, is_cyclic:=isCyclic, d_even:=dEven, j:=jVal, j_divides_3:=jDiv3);
end;;

results := [];;
for pr in PAIRS do
  Add(results, rec(pair_fiber:=pr.pair_fiber, index:=pr.index,
                    m0:=MeasureAb(pr.m0_id), m1:=MeasureAb(pr.m1_id)));
od;

## ============ M5 control (independent reconstruction, verbatim-copied machinery) ============
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

m5Invs := [];;  m5D := 0;;  m5IsCyclic := false;;  m5DEven := false;;
if gm5OrderOk then
  m5Invs := AbelianInvariants(GM5);
  m5D := Product(m5Invs, x -> x, 1);
  m5GabM5 := GM5 / DerivedSubgroup(GM5);
  m5IsCyclic := IsCyclic(m5GabM5);
  m5DEven := (m5D mod 2 = 0);
fi;

Print("23-pair table: ", Length(results), " pairs measured\n");
Print("M5 control: |G_M5|=", gm5Order, " order_ok=", gm5OrderOk, " AbelianInvariants=", m5Invs, "\n");

## ============ JSON output ============
JAbRec := function(r)
  local invStr, jStr, jd3Str;
  invStr := JArr(List(r.invariants, String));
  if r.j = fail then jStr := "null"; else jStr := String(r.j); fi;
  if r.j_divides_3 = fail then jd3Str := "null"; else jd3Str := JB(r.j_divides_3); fi;
  return Concatenation("{",
    "\"id_group\":", JPair(r.id_group[1], r.id_group[2]), ",",
    "\"abelian_invariants\":", invStr, ",",
    "\"d\":", String(r.d), ",",
    "\"is_cyclic\":", JB(r.is_cyclic), ",",
    "\"d_even\":", JB(r.d_even), ",",
    "\"j\":", jStr, ",",
    "\"j_divides_3\":", jd3Str,
    "}");
end;;

JPairRec := function(pr)
  return Concatenation("{",
    "\"pair_fiber\":", JStr(pr.pair_fiber), ",",
    "\"index\":", String(pr.index), ",",
    "\"m0\":", JAbRec(pr.m0), ",",
    "\"m1\":", JAbRec(pr.m1),
    "}");
end;;

m5InvStr := JArr(List(m5Invs, String));;
m5JField := "null";;
m5JDiv3Field := "null";;
if gm5OrderOk and m5IsCyclic and m5DEven then
  m5JField := String(m5D/2);
  m5JDiv3Field := JB(3 mod (m5D/2) = 0);
fi;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/hcen_ab_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a797(5)/798/799 -- docs/notes/hunting_chapter_v1.md \\u00a73.3 (AB-2J) \\u306e\\u8868\\u8aad\\u307f\",",
  "\"target_definition\":\"census exotic 23\\u5bfe(\\u88c1\\u5b9a642/644\\u30fb\\u69cb\\u6210=10(750-clique)+1(384/[384,608])+12(index<384 both-fixed)\\u30fbsource=search/certs/r6a_summary_v1_20260806.json+search/certs/lins_twin_census_v1_20260806.json\\u30fb\\u30af\\u30ed\\u30b9\\u30c1\\u30a7\\u30c3\\u30af\\u6e08\\u307f: pair0(idx24)=[24,3]=SL(2,3)\\u3068pair30(idx336)=[336,208]=PSL(3,2):C2\\u304c\\u6587\\u732e\\u5024\\u3068\\u4e00\\u81f4\",",
  "\"t1_non_interference_note\":\"G^ab\\u306e\\u8aad\\u307f\\u53d6\\u308a\\u306f\\u56fa\\u5b9a\\u6e08\\u307f\\u306e\\u6709\\u9650\\u7fa4G\\u4e0a\\u306e\\u8a08\\u7b97\\u3067\\u3042\\u308a\\u3001B3/N\\u4e0a\\u306eGTSh\\u8ff0\\u8a9e(hexagon/charming/settled/isolated/SURJ/kernel_multiplicity)\\u3092\\u4e00\\u5207\\u8a55\\u4fa1\\u3057\\u3066\\u3044\\u306a\\u3044\\u306e\\u3067T-1\\u306b\\u62b5\\u89e6\\u3057\\u306a\\u3044(hunting_chapter_v1.md \\u00a73.3 \\u81ea\\u8eab\\u306e\\u6839\\u62e0)\\u3002\",",
  "\"pairs\":[", JoinC(List(results, JPairRec), ","), "],",
  "\"m5_control\":{",
    "\"note\":\"outside_the_23pair_prediction_set -- M5 is NOT part of the census exotic 23; included as a separate c-notin-N reference object per docs/week1-\\u5b9a\\u7fa9\\u30ce\\u30fc\\u30c8.md \\u00a72 (\\u8fd1\\u9053\\u304c\\u58ca\\u308c\\u308b\\u4f8b) and hunting_chapter_v1.md \\u00a73.3. G=B3/M5 reconstructed independently via BuildQTGeneral (verbatim-copied from search/week3-M5-explorer.g); original frozen script NOT modified or re-run.\",",
    "\"order\":", String(gm5Order), ",",
    "\"order_expected\":3240,",
    "\"order_ok\":", JB(gm5OrderOk), ",",
    "\"abelian_invariants\":", m5InvStr, ",",
    "\"d\":", String(m5D), ",",
    "\"is_cyclic\":", JB(m5IsCyclic), ",",
    "\"d_even\":", JB(m5DEven), ",",
    "\"j\":", m5JField, ",",
    "\"j_divides_3\":", m5JDiv3Field,
  "},",
  "\"no_verdict_note\":\"raw AbelianInvariants/d/j and machine-checked booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/hcen_ab_v1_20260811.json", out);;
Print("Wrote search/certs/hcen_ab_v1_20260811.json\n");
Print("HCEN_AB_DONE\n");
QUIT;
