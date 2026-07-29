#############################################################################
## search/probe/wac_v1/ss_alt.g -- second-strike slate, alternating branch
## n = 17..20, both parities of k; structure constants; targeted realization.
## Single lane. NOT a ledger claim. No commit. No u (sealed symbol).
#############################################################################
SqType := function(lam)
  local out, p;
  out := [];
  for p in lam do
    if p mod 2 = 0 then Add(out, p/2); Add(out, p/2); else Add(out, p); fi;
  od;
  return SortedList(out);
end;;
MaxMult := function(l) return Maximum(List(Set(l), v -> Number(l, w -> w = v))); end;;
WacCT := function(p, n) return SortedList(List(Orbits(Group(p),[1..n]), Length)); end;;
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

Print("===== SA-1: survivors n=17..20 (both parities) + structure constants =====\n");
surv := [];;
for n in [17..20] do
  for lam in Partitions(n) do
    t := Length(lam);
    if Lcm(lam) < 7 then continue; fi;
    s := SqType(lam);
    if MaxMult(s) < 5 or Lcm(s) < 3 then continue; fi;
    kpar := (n - t) mod 2;
    for k in [1..QuoInt(n,2)] do
      for j in [1..QuoInt(n,3)] do
        if k mod 2 = kpar and k + 2*j + 2 - n >= t then
          Add(surv, rec(n:=n, lam:=SortedList(lam), t:=t, k:=k, j:=j, sq:=s));
        fi;
      od;
    od;
  od;
od;
for r in surv do
  n := r.n;
  tbl := CharacterTable("Symmetric", n);;
  parts := ClassParameters(tbl);;
  ia := First([1..Length(parts)], i -> SortedList(parts[i][2]) =
        SortedList(Concatenation(List([1..r.k],z->2), List([1..n-2*r.k],z->1))));
  ib := First([1..Length(parts)], i -> SortedList(parts[i][2]) =
        SortedList(Concatenation(List([1..r.j],z->3), List([1..n-3*r.j],z->1))));
  ic := First([1..Length(parts)], i -> SortedList(parts[i][2]) = r.lam);
  cc := ClassMultiplicationCoefficient(tbl, ia, ib, ic);
  # budget quantities
  cs := 1;; for v in Set(r.sq) do
    m := Number(r.sq, w -> w = v); cs := cs * v^m * Factorial(m); od;
  Nord := Lcm(r.sq);
  Print("n=", n, " lam(u)=", r.lam, " -> xbar=", r.sq, " N_ord=", Nord,
        "  a'=2^", r.k, "1^", n-2*r.k, " b'=3^", r.j, "1^", n-3*r.j,
        "  structconst=", cc,
        "  |C_Sn(x)|=", cs, "  budget=", Phi(2*Nord)*(cs/2)*cs, "\n");
od;

Print("\n===== SA-2: targeted realization =====\n");
Realize := function(n, lam, k, j, tries)
  local Sn, An, uu, inv, i, a1, b1, G, want;
  Sn := SymmetricGroup(n); An := AlternatingGroup(n);
  uu := (); i := 0;
  for v in lam do
    if v > 1 then uu := uu * WacCyc(List([1..v], z -> i+z)); fi;
    i := i + v;
  od;
  inv := WacBlock(k, 2);
  want := SortedList(Concatenation(List([1..j],z->3), List([1..n-3*j],z->1)));
  Print("  n=", n, " u=", WacCT(uu,n), " ord=", Order(uu),
        " xbar=", WacCT(uu^2,n), " ord=", Order(uu^2), "\n");
  for i in [1..tries] do
    a1 := inv ^ Random(Sn);
    b1 := a1 * uu^-1;
    if WacCT(b1,n) = want then
      G := Group(a1,b1);
      if G = An or G = Sn then
        Print("  FOUND (", Size(G) = Size(An), " = is A_n)\n");
        Print("    a1 := ", a1, ";;\n    b1 := ", b1, ";;\n");
        return rec(a1:=a1, b1:=b1, n:=n);
      fi;
    fi;
  od;
  Print("  NOT FOUND in ", tries, " tries\n");
  return fail;
end;;
r18 := Realize(18, [13,2,2,1], 8, 6, 400000);;
r20 := Realize(20, [15,2,2,1], 10, 6, 400000);;

Print("\n===== SA-3: window build =====\n");
Build := function(r, tag)
  local n, An, S3, D, e1, e2, a, b, s1, s2, P, x1, y1, cy, sx, Nord, cm;
  n := r.n; An := AlternatingGroup(n); S3 := SymmetricGroup(3);
  D := DirectProduct(An, S3); e1 := Embedding(D,1); e2 := Embedding(D,2);
  a := Image(e1,r.a1)*Image(e2,(1,3)); b := Image(e1,r.b1)*Image(e2,(1,3,2));
  s1 := b^-1*a; s2 := a^-1*b^2;
  P := Group(s1^2, s2^2);
  x1 := PreImagesRepresentative(e1, s1^2); y1 := PreImagesRepresentative(e1, s2^2);
  cy := Centralizer(An, y1); sx := Centralizer(SymmetricGroup(n), x1);
  Nord := Order(s1^2); cm := Phi(2*Nord);
  Print("[", tag, "] n=", n, " braid=", s1*s2*s1 = s2*s1*s2,
        " c=1:", (s1*s2)^3 = One(D), " <s1,s2>=E:", Group(s1,s2)=D, "\n");
  Print("  [B3:N]=", Size(D), "  |P|=", Size(P), "  P=ker:", P=Kernel(Projection(D,2)), "\n");
  Print("  ord(s1)=", Order(s1), " xbar type=", WacCT(x1,n), " N_ord=", Nord,
        " c_m=", cm, "\n");
  Print("  C_P(ybar)=", Size(cy), " solv=", IsSolvableGroup(cy),
        " (", StructureDescription(cy), ")\n");
  Print("  Stab=C_Sn(xbar)=", Size(sx), " solv=", IsSolvableGroup(sx),
        " (", StructureDescription(sx), ")\n");
  Print("  naive budget=", cm*Size(DerivedSubgroup(P)),
        "   Xi budget=", cm*Size(cy)*Size(sx), "\n");
  Print("  JUDGE_S1_IMG := ", s1, ";;\n  JUDGE_S2_IMG := ", s2, ";;\n");
  Print("  degree(E)=", LargestMovedPoint(D), "\n");
end;;
if r18 <> fail then Build(r18, "W-D-A18-13a"); fi;
if r20 <> fail then Build(r20, "W-D-A20-15a"); fi;
Print("\nSS_ALT_DONE\n");
QUIT;
