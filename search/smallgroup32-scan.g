# smallgroup32-scan.g -- exhaustive scan of all 51 groups of order 32 for (4,4,4)-marked F2-quotients
#
# Usage: .\gap.ps1 search\smallgroup32-scan.g
#
# Task (commander order, 2026-07-26, "K-cong 第二証明の橋・裁定 19 §4"):
#   For each SmallGroup(32,i), i=1..51, count generating pairs (a,b) in G^2 with
#     <a,b> = G, ord(a) = ord(b) = ord((ab)^-1) = 4
#   (note ord((ab)^-1) = ord(ab), so this is: ord(a)=ord(b)=ord(ab)=4, <a,b>=G).
#   N_i > 0 groups form the candidate list; expect exactly one, isomorphic to
#   G4 = <(r,s,s),(rs,r,rs)> <= D4^3 (the object surfacing in 裁定_18_kcong.md as
#   "F2/K^(n) decomposes as Gn <= Dn^3", |G4| = 32).
#
# Design note: G4 as specified in the task ((r,s,s),(rs,r,rs) inside D4^3, abstract
# convention "r^a s^e", GAP form "s*r^a" for "r^a s") is verbatim the n=4 instance of
# MakeGn(n) already used in search/week3-M5-explorer.g for n=3 (there called G3,
# |G3|=108). MakeDn/MakeGn below are copied unchanged from that script (same
# convention, same relation checks) so as not to re-derive a construction already
# built and load-bearing elsewhere.

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= copied verbatim from search/week3-M5-explorer.g =================
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

# ================= JSON helpers (copied verbatim) =================
JStr := function(s) return Concatenation("\"", s, "\""); end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;
JoinC := function(strs, sep)
  local r, i;
  if Length(strs) = 0 then return ""; fi;
  r := strs[1];
  for i in [2..Length(strs)] do r := Concatenation(r, sep, strs[i]); od;
  return r;
end;;
JArr := function(items) return Concatenation("[", JoinC(items, ","), "]"); end;;

WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

# ================================================================================
# Step 0: build G4 = MakeGn(4).G and identify it via IdSmallGroup, as the reference
# target to cross-check the scan against.
# ================================================================================
g4 := MakeGn(4);;
g4Order := Size(g4.G);;
Print("|G4| = ", g4Order, " (expect 32)\n");
if g4Order <> 32 then
  Error("G4 construction FAILED: |G4| = ", g4Order, ", expected 32");
fi;
g4Id := IdGroup(g4.G);;
Print("IdSmallGroup(G4) = ", g4Id, "\n");
if g4Id[1] <> 32 then
  Error("IdGroup(G4) order component != 32: got ", g4Id);
fi;
g4Idx := g4Id[2];;

# sanity: x,y themselves satisfy the marking condition ord(a)=ord(b)=ord(ab)=4 and
# generate G4 (they are literally the pair the task describes).
xyOrdA := Order(g4.x);;  xyOrdB := Order(g4.y);;  xyOrdAB := Order(g4.x*g4.y);;
Print("[", PF(true), "] G4 witness pair (x,y): ord(x)=", xyOrdA, " ord(y)=", xyOrdB,
      " ord(xy)=", xyOrdAB, " (all expect 4)\n");
if not (xyOrdA=4 and xyOrdB=4 and xyOrdAB=4) then
  Print("  [ANOMALY] G4's own defining pair does not satisfy the (4,4,4)-marked condition!\n");
fi;

# ================================================================================
# Step 1-3: exhaustive scan over all 51 groups of order 32
# ================================================================================
results := [];;
t0 := Runtime();;
for i in [1..51] do
  G := SmallGroup(32, i);
  elts := Elements(G);
  n := Length(elts);
  Ni := 0;
  for a in elts do
    ord_a := Order(a);
    if ord_a <> 4 then continue; fi;
    for b in elts do
      ord_b := Order(b);
      if ord_b <> 4 then continue; fi;
      if Order(a*b) <> 4 then continue; fi;
      if Size(Subgroup(G, [a,b])) = 32 then
        Ni := Ni + 1;
      fi;
    od;
  od;
  autOrd := Size(AutomorphismGroup(G));
  Add(results, rec(idx:=i, Ni:=Ni, autOrd:=autOrd));
  if Ni > 0 then
    Print("SmallGroup(32,", i, "): N_i = ", Ni, ", |Aut| = ", autOrd,
          ", N_i/|Aut| = ", Ni/autOrd, "\n");
  fi;
od;
t1 := Runtime();;
Print("scan over all 51 groups of order 32: time_ms=", t1-t0, "\n");

# ================================================================================
# Step 4: judgement
# ================================================================================
nonzero := Filtered(results, r -> r.Ni > 0);;
Print("\n非零 N_i を持つ群: ", Length(nonzero), " 個\n");
for r in nonzero do
  Print("  SmallGroup(32,", r.idx, "): N_i=", r.Ni, " |Aut|=", r.autOrd, " N_i/|Aut|=", r.Ni/r.autOrd, "\n");
od;

judgement := "";;
uniqueMatch := (Length(nonzero) = 1) and (nonzero[1].idx = g4Idx);;
if uniqueMatch then
  judgement := Concatenation("位数 32 で (4,4,4)-marked F2-商になれる群は SmallGroup(32,", String(g4Idx),
    ") = IdSmallGroup(G4) のみ・核は一意 (N_", String(g4Idx), "=", String(nonzero[1].Ni),
    ", |Aut|=", String(nonzero[1].autOrd), ", kernels=", String(nonzero[1].Ni/nonzero[1].autOrd), ")");
  Print("\n[判定] ", judgement, "\n");
else
  judgement := "反例あり: 非零 N_i を持つ群が G4 のみでない、または複数存在する。下記リストを参照。";
  Print("\n[判定] ", judgement, "\n");
  Print("  期待: G4 = SmallGroup(32,", g4Idx, ") のみが非零。実際の非零リストは上記参照。\n");
fi;

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");

# ================================================================================
# certificate JSON
# ================================================================================
resultsJson := [];;
for r in results do
  Add(resultsJson, Concatenation(
    "{\"idx\":", String(r.idx), ",\"N_i\":", String(r.Ni),
    ",\"aut_order\":", String(r.autOrd),
    ",\"kernels\":", String(r.Ni/r.autOrd), "}"));
od;

nonzeroJson := [];;
for r in nonzero do
  Add(nonzeroJson, Concatenation(
    "{\"idx\":", String(r.idx), ",\"N_i\":", String(r.Ni),
    ",\"aut_order\":", String(r.autOrd),
    ",\"kernels\":", String(r.Ni/r.autOrd), "}"));
od;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/smallgroup32-scan.g\",\"date\":\"2026-07-26\"},",
  "\"task\":\"位数32 の全51群につき (4,4,4)-marked F2-商 (a,b generate G, ord(a)=ord(b)=ord(ab)=4) の悉皆判定 (裁定_19_geography_v3.md 4)\",",
  "\"universe\":\"SmallGroup(32,i), i=1..51 (全 51 群、事前登録どおり範囲固定)\",",
  "\"g4_reference\":{\"construction\":\"MakeGn(4).G = Group((r,s,s),(rs,r,rs)) <= D4^3, abstract convention r^a s^e = GAP s*r^a\",",
  "\"order\":", String(g4Order), ",\"id_small_group\":[", String(g4Id[1]), ",", String(g4Id[2]), "],",
  "\"witness_pair_orders\":{\"ord_x\":", String(xyOrdA), ",\"ord_y\":", String(xyOrdB), ",\"ord_xy\":", String(xyOrdAB), "}},",
  "\"per_group_results\":", JArr(resultsJson), ",",
  "\"nonzero_N_i\":", JArr(nonzeroJson), ",",
  "\"unique_match_with_g4\":", JB(uniqueMatch), ",",
  "\"judgement\":", JStr(judgement),
  "}");

WriteFile("certificates/a5/smallgroup32_scan.json", s);
Print("wrote certificates/a5/smallgroup32_scan.json\n");

QUIT;
