#############################################################################
## search/probe/wac_v1/a15.g -- WA-c: n=15 (image S15), Ebar = S3 x_{C2} S15
## Single lane. NOT a ledger claim. No commit.
#############################################################################
WacCT := function(p, n)
  return SortedList(List(Orbits(Group(p), [1..n]), Length));
end;;
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
    p := p * WacCyc(List([1..len], j -> base + j)); base := base + len;
  od;
  return p;
end;;

S15 := SymmetricGroup(15);; A15 := AlternatingGroup(15);;
inv := WacBlock(7,2);;   # 2^7 1  (odd)
Print("a' class type=", WacCT(inv,15), " sign=", SignPerm(inv), "\n");

Try := function(uu, label, tries)
  local i, a1, b1, G, hit, gen;
  hit := 0; gen := 0;
  Print("\n--- ", label, ": u type=", WacCT(uu,15), " ord=", Order(uu),
        " ; xbar=u^2 type=", WacCT(uu^2,15), " ord=", Order(uu^2), "\n");
  for i in [1..tries] do
    a1 := inv ^ Random(S15);
    b1 := a1 * uu^-1;
    if WacCT(b1,15) = [3,3,3,3,3] then
      hit := hit + 1;
      G := Group(a1,b1);
      if G = S15 then
        gen := gen + 1;
        if gen = 1 then
          Print("  FOUND: a' := ", a1, ";;\n         b' := ", b1, ";;\n");
          Print("  check b'^-1*a' = u ? ", b1^-1*a1 = uu,
                "  ord(a')=", Order(a1), " ord(b')=", Order(b1), "\n");
          return rec(a1:=a1, b1:=b1, u:=uu);
        fi;
      fi;
    fi;
  od;
  Print("  class hits=", hit, "  <a',b'>=S15: ", gen, "  -> NOT FOUND\n");
  return fail;
end;;

r9  := Try((1,2,3,4,5,6,7,8,9)*(10,11)*(12,13)*(14,15), "lam=(9,2,2,2)", 300000);;
if r9 = fail then
  r10 := Try((1,2,3,4,5,6,7,8,9,10)*(11,12)*(13,14), "lam=(10,2,2,1)", 300000);;
else r10 := fail; fi;

Build := function(r)
  local S3, D, e1, e2, a, b, s1, s2, P, x1, y1, cy, sx, Nord, cm;
  S3 := SymmetricGroup(3);
  D := DirectProduct(SymmetricGroup(15), S3);
  e1 := Embedding(D,1); e2 := Embedding(D,2);
  a := Image(e1,r.a1)*Image(e2,(1,3));
  b := Image(e1,r.b1)*Image(e2,(1,3,2));
  Print("\n=== window build (n=15) ===\n");
  Print("a^2=1? ", a^2=One(D), " b^3=1? ", b^3=One(D), "\n");
  s1 := b^-1*a; s2 := a^-1*b^2;
  Print("braid? ", s1*s2*s1 = s2*s1*s2, "  c=(s1s2)^3=1? ", (s1*s2)^3=One(D), "\n");
  Print("|E| = ", Size(Group(s1,s2)), "  = 6*|A15| = ", 6*Size(AlternatingGroup(15)),
        " ? ", Size(Group(s1,s2)) = 6*Size(AlternatingGroup(15)), "\n");
  P := Group(s1^2, s2^2);
  Print("|P| = ", Size(P), "  = |A15|? ", Size(P) = Size(AlternatingGroup(15)), "\n");
  Print("ord(s1)=", Order(s1), " ord(xbar)=", Order(s1^2),
        " ord(ybar)=", Order(s2^2), "\n");
  x1 := PreImagesRepresentative(e1, s1^2);
  y1 := PreImagesRepresentative(e1, s2^2);
  Print("xbar type=", WacCT(x1,15), " ybar type=", WacCT(y1,15), "\n");
  cy := Centralizer(AlternatingGroup(15), y1);
  sx := Centralizer(SymmetricGroup(15), x1);
  Print("C_P(ybar)=", Size(cy), " solv=", IsSolvableGroup(cy),
        " (", StructureDescription(cy), ")\n");
  Print("Stab_Aut(P)(xbar)=", Size(sx), " solv=", IsSolvableGroup(sx),
        " (", StructureDescription(sx), ")\n");
  Nord := Order(s1^2); cm := Phi(2*Nord);
  Print("N_ord=", Nord, "  charming m count=", cm, "\n");
  Print("naive budget = ", cm, " * |A15| = ", cm*Size(AlternatingGroup(15)), "\n");
  Print("Xi-restricted budget = ", cm, "*", Size(cy), "*", Size(sx), " = ",
        cm*Size(cy)*Size(sx), "\n");
  Print("JUDGE_S1_IMG := ", s1, ";;\n");
  Print("JUDGE_S2_IMG := ", s2, ";;\n");
end;;

if r9 <> fail then Build(r9); elif r10 <> fail then Build(r10); fi;
Print("\nA15_DONE\n");
QUIT;
