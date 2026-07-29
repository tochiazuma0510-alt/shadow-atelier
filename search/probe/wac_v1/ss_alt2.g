#############################################################################
## search/probe/wac_v1/ss_alt2.g -- realize the two alternating second-strike
## windows: n=18 lam(u)=(13,2,2,1) [N_ord=13] and n=20 lam(u)=(15,2,2,1)
## [N_ord=15=3*5].  Single lane. NOT a ledger claim. No commit.
#############################################################################
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

Realize := function(n, uu, k, j, tries)
  local Sn, An, inv, i, a1, b1, G, want, hits;
  Sn := SymmetricGroup(n); An := AlternatingGroup(n);
  inv := WacBlock(k,2);
  want := SortedList(Concatenation(List([1..j],z->3), List([1..n-3*j],z->1)));
  hits := 0;
  Print("n=", n, "  u type=", WacCT(uu,n), " ord=", Order(uu),
        "  xbar=", WacCT(uu^2,n), " ord=", Order(uu^2),
        "  a'=2^", k, "  b'=3^", j, "\n");
  for i in [1..tries] do
    a1 := inv ^ Random(Sn);
    b1 := a1 * uu^-1;
    if WacCT(b1,n) = want then
      hits := hits + 1;
      G := Group(a1,b1);
      if G = An then
        Print("  FOUND at try ", i, " (class hits so far ", hits, ")\n");
        Print("  a1 := ", a1, ";;\n  b1 := ", b1, ";;\n");
        return rec(a1:=a1, b1:=b1, n:=n);
      fi;
    fi;
  od;
  Print("  class hits=", hits, "  generating A", n, ": 0  -> NOT FOUND\n");
  return fail;
end;;

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
  Print("\n[", tag, "] braid=", s1*s2*s1 = s2*s1*s2,
        "  c=(s1s2)^3=1: ", (s1*s2)^3 = One(D),
        "  <s1,s2>=E: ", Group(s1,s2)=D, "\n");
  Print("  [B3:N]=", Size(D), "   |P|=|A", n, "|=", Size(P),
        "   P=ker: ", P = Kernel(Projection(D,2)), "\n");
  Print("  ord(s1)=", Order(s1), "  xbar type=", WacCT(x1,n),
        "  N_ord=", Nord, "  c_m=phi(", 2*Nord, ")=", cm, "\n");
  Print("  C_P(ybar)=", Size(cy), " solv=", IsSolvableGroup(cy),
        " (", StructureDescription(cy), ")\n");
  Print("  Stab=C_S", n, "(xbar)=", Size(sx), " solv=", IsSolvableGroup(sx),
        " (", StructureDescription(sx), ")\n");
  Print("  naive budget = ", cm, "*|A", n, "| = ", cm*Size(P), "\n");
  Print("  Xi budget    = ", cm, "*", Size(cy), "*", Size(sx), " = ",
        cm*Size(cy)*Size(sx), "\n");
  Print("  JUDGE_S1_IMG := ", s1, ";;\n  JUDGE_S2_IMG := ", s2, ";;\n");
  Print("  degree(E)=", LargestMovedPoint(D), "\n");
end;;

r18 := Realize(18, (1,2,3,4,5,6,7,8,9,10,11,12,13)*(14,15)*(16,17), 8, 6, 1200000);;
if r18 <> fail then Build(r18, "W-D-A18-13a"); fi;
r20 := fail;;
if r20 <> fail then Build(r20, "W-D-A20-15a"); fi;
Print("\nSS_ALT2_DONE\n");
QUIT;
