#############################################################################
## search/probe/wac_v1/a13_check4.g
##  Sol F84-4.2 への応答: 「72」は固定 w0 に対する ORDERED PAIR の個数である。
##  固定 w0 の解集合上の C_{S_n}(w0)-軌道の個数 = そこから得られる相異なる窓 N の個数
##  (同じ w0 をもつ 2 解が S_n-共役 <=> 共役元が C(w0) に入る <=> 同一軌道。
##   共役な対は B3 -> E の合成を Aut(E) で捻るだけなので kernel N は文字どおり同一)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
WacCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;

OrbitReport := function(nn, w0, label)
  local Snn, Ann, k, a, b, sols, C, orbs, o, rest, reps, r;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  sols := [];
  for k in [1..Int(nn/2)] do
    for a in AsList(ConjugacyClass(Snn, WacBlock(k,2))) do
      b := a * w0^-1;
      if b^3 = () and b <> () then
        if Group(a,b) = Ann or Group(a,b) = Snn then Add(sols, a); fi;
      fi;
    od;
  od;
  C := Centralizer(Snn, w0);
  Print("== ", label, " ==\n");
  Print("   w0 = ", w0, "   |C_{S_n}(w0)| = ", Size(C), "\n");
  Print("   #ordered pairs (a1,b1) with fixed w0 = ", Length(sols), "\n");
  orbs := Orbits(C, sols, OnPoints);
  Print("   #C(w0)-orbits = ", Length(orbs),
        "   orbit sizes = ", SortedList(List(orbs, Length)), "\n");
  Print("   => #distinct windows N from this w0 = ", Length(orbs), "\n");
  reps := List(orbs, o -> o[1]);
  for r in reps do
    Print("      rep a1 = ", r, "\n");
  od;
  return;
end;;

OrbitReport(10, WacCyc([1..9]),                     "W-E-A10-9t1  (t=1)");
OrbitReport(11, WacCyc([1..9])*(10,11),             "W-E-A11-9t2  (t=2)");
OrbitReport(12, WacCyc([1..9])*(10,11),             "W-E-A12-9t3  (t=3)");
OrbitReport(13, WacCyc([1..9])*(10,11)*(12,13),     "W-E-A13-9t4  (t=4)");
Print("\nA13_CHECK4_DONE\n");
QUIT;
