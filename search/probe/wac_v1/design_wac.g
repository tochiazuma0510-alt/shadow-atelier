#############################################################################
## search/probe/wac_v1/design_wac.g -- WA-c reverse design (裁定161 委嘱)
##
## Single-lane GAP check for docs/notes/wac_reverse_design_v1.md.
## NOT a ledger claim. No u (sealed symbol). No commit.
#############################################################################

WacCT := function(p, n)
  return SortedList(List(Orbits(Group(p), [1..n]), Length));
end;;

WacCyc := function(l)
  local i, img, m;
  m := Maximum(l);
  img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base + j));
    base := base + len;
  od;
  return p;
end;;

WacReport := function(name, g, n)
  local cp, cs, P, Sn;
  P := AlternatingGroup(n); Sn := SymmetricGroup(n);
  cp := Centralizer(P, g);
  cs := Centralizer(Sn, g);
  Print(name, ": type=", WacCT(g,n), " ord=", Order(g), "\n");
  Print("   |C_An|=", Size(cp), " solvable=", IsSolvableGroup(cp),
        " struct=", StructureDescription(cp), "\n");
  Print("   |C_Sn|=", Size(cs), " solvable=", IsSolvableGroup(cs),
        " struct=", StructureDescription(cs), "\n");
end;;

Print("\n===== D-1: audit A13 target (re-verify) =====\n");
Print("gen <xbar,ybar> = A13 ? ",
      Group((7,8,9,10,11,12,13),(1,2,3,4,5,6,7)) = AlternatingGroup(13), "\n");
WacReport("A13 xbar", (7,8,9,10,11,12,13), 13);
WacReport("A13 ybar", (1,2,3,4,5,6,7), 13);

Print("\n===== D-2: A12 candidate (smaller P) =====\n");
Print("gen <x,y> = A12 ? ",
      Group((6,7,8,9,10,11,12),(1,2,3,4,5,6,7)) = AlternatingGroup(12), "\n");
WacReport("A12 xbar(7cyc,5fix)", (6,7,8,9,10,11,12), 12);

Print("\n===== D-3: search for (a1,b1), u=b1^-1*a1 of target type =====\n");

SearchPair := function(n, targetType, tries)
  local An, Sn, invk, ordk, i, a1, b1, u, ty;
  An := AlternatingGroup(n); Sn := SymmetricGroup(n);
  invk := Filtered([1..QuoInt(n,2)], k -> k mod 2 = 0);
  ordk := [1..QuoInt(n,3)];
  for i in [1..tries] do
    a1 := WacBlock(Random(invk), 2) ^ Random(Sn);
    b1 := WacBlock(Random(ordk), 3) ^ Random(Sn);
    u := b1^-1 * a1;
    ty := WacCT(u, n);
    if ty = targetType and Group(a1, b1) = An then
      Print("FOUND n=", n, " after ", i, " tries\n");
      Print("  a1 = ", a1, "  type ", WacCT(a1,n), "\n");
      Print("  b1 = ", b1, "  type ", WacCT(b1,n), "\n");
      Print("  u  = ", u, "  ord=", Order(u), " type=", ty, "\n");
      Print("  xbar = u^2 = ", u^2, " ord=", Order(u^2), " type=", WacCT(u^2,n), "\n");
      return rec(a1 := a1, b1 := b1, u := u, n := n);
    fi;
  od;
  Print("NOT FOUND n=", n, " in ", tries, " tries\n");
  return fail;
end;;

res13 := SearchPair(13, [1,1,2,2,7], 20000);;
res12 := SearchPair(12, [1,2,2,7], 20000);;

Print("\n===== D-4: build E = A_n x S3, verify window =====\n");

BuildWindow := function(res)
  local n, An, S3, D, e1, e2, a, b, s1, s2, P, K, pr2, x1, y1;
  n := res.n;
  An := AlternatingGroup(n); S3 := SymmetricGroup(3);
  D := DirectProduct(An, S3);
  e1 := Embedding(D, 1); e2 := Embedding(D, 2);
  a := Image(e1, res.a1) * Image(e2, (1,3));
  b := Image(e1, res.b1) * Image(e2, (1,3,2));
  Print("n=", n, "  a^2=1? ", a^2 = One(D), "  b^3=1? ", b^3 = One(D), "\n");
  s1 := b^-1 * a;
  s2 := a^-1 * b^2;
  Print("  braid s1s2s1 = s2s1s2 ? ", s1*s2*s1 = s2*s1*s2, "\n");
  Print("  c=(s1 s2)^3 = 1 ? ", (s1*s2)^3 = One(D), "  (c in N window)\n");
  Print("  ord(s1)=", Order(s1), " ord(s2)=", Order(s2), "\n");
  Print("  <s1,s2>=E ? ", Group(s1,s2) = D, "  |E|=", Size(D),
        "  =6|A", n, "|? ", Size(D) = 6*Size(An), "\n");
  P := Group(s1^2, s2^2);
  pr2 := Projection(D, 2); K := Kernel(pr2);
  Print("  |P|=", Size(P), "  P=ker(E->>S3)? ", P = K,
        "  ord(xbar)=", Order(s1^2), " ord(ybar)=", Order(s2^2), "\n");
  x1 := PreImagesRepresentative(e1, s1^2);
  y1 := PreImagesRepresentative(e1, s2^2);
  Print("  xbar type=", WacCT(x1,n), " ybar type=", WacCT(y1,n),
        " overlap=", Size(Intersection(MovedPoints(x1), MovedPoints(y1))), "\n");
  WacReport("  win xbar", x1, n);
  WacReport("  win ybar", y1, n);
  Print("  N_ord = lcm(ord x, ord y, ord c) = ",
        Lcm(Order(s1^2), Order(s2^2), 1), "\n");
  Print("  JUDGE_S1_IMG := ", s1, ";;\n");
  Print("  JUDGE_S2_IMG := ", s2, ";;\n");
  Print("  (E is a perm group of degree ", LargestMovedPoint(D), ")\n");
  return rec(D := D, s1 := s1, s2 := s2, P := P);
end;;

if res13 <> fail then w13 := BuildWindow(res13);; fi;
if res12 <> fail then w12 := BuildWindow(res12);; fi;

Print("\nWAC_DESIGN_DONE\n");
QUIT;
