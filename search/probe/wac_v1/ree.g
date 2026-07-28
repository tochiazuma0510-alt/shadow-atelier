#############################################################################
## search/probe/wac_v1/ree.g -- Ree/Riemann-Hurwitz gate + targeted A12 search
## Single lane. NOT a ledger claim. No u (sealed symbol). No commit.
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

## ---- part 1: exact class structure constant for A12, (2^6),(3^4),(7,2,2,1)
Print("===== R-1: A12 class structure constant (character table) =====\n");
tbl := CharacterTable("A12");;
oc := OrdersClassRepresentatives(tbl);;
sc := SizesConjugacyClasses(tbl);;
Print("A12 order = ", Size(tbl), "\n");
# identify classes by cycle type via the permutation group (safer than table names)
A12 := AlternatingGroup(12);;
ccl := ConjugacyClasses(A12);;
idx := function(ty)
  return First([1..Length(ccl)], i -> WacCT(Representative(ccl[i]),12) = ty);
end;;
i1 := idx([2,2,2,2,2,2]);; i2 := idx([3,3,3,3]);; i3 := idx([1,2,2,7]);;
Print("class indices: 2^6 -> ", i1, " (size ", Size(ccl[i1]), "), 3^4 -> ", i2,
      " (size ", Size(ccl[i2]), "), (7,2,2,1) -> ", i3,
      " (size ", Size(ccl[i3]), ")\n");
# match the GAP library table ordering to the perm-group classes by (order,size)
mtch := function(i)
  local o, s;
  o := Order(Representative(ccl[i])); s := Size(ccl[i]);
  return Filtered([1..Length(oc)], k -> oc[k] = o and sc[k] = s);
end;;
Print("library-table candidates: ", mtch(i1), " ", mtch(i2), " ", mtch(i3), "\n");
m1 := mtch(i1)[1];; m2 := mtch(i2)[1];;
for m3 in mtch(i3) do
  Print("  ClassMultiplicationCoefficient(", m1, ",", m2, ",", m3, ") = ",
        ClassMultiplicationCoefficient(tbl, m1, m2, m3), "\n");
od;

## ---- part 2: targeted random search in A12
Print("\n===== R-2: targeted search a1 = 2^6, b1 = 3^4, u of type (7,2,2,1) =====\n");
S12 := SymmetricGroup(12);;
hits := 0;; gens := 0;; trans := 0;; found := fail;;
for i in [1..200000] do
  a1 := WacBlock(6,2) ^ Random(S12);
  b1 := WacBlock(4,3) ^ Random(S12);
  u := b1^-1 * a1;
  if WacCT(u,12) = [1,2,2,7] then
    hits := hits + 1;
    G := Group(a1,b1);
    if IsTransitive(G,[1..12]) then
      trans := trans + 1;
      if G = A12 then
        gens := gens + 1;
        if found = fail then found := rec(a1:=a1, b1:=b1, u:=u, n:=12); fi;
      fi;
    fi;
  fi;
od;
Print("u-type hits: ", hits, "   transitive: ", trans, "   = A12: ", gens, "\n");
if found <> fail then
  Print("a1 := ", found.a1, ";;\n");
  Print("b1 := ", found.b1, ";;\n");
  Print("u  := ", found.u, ";;  ord=", Order(found.u), "\n");
  Print("xbar := ", found.u^2, ";;  type ", WacCT(found.u^2,12), "\n");
fi;

## ---- part 3: Ree bound table, n = 9..24
Print("\n===== R-3: Ree bound c(u) <= floor(n/2)_even + 2*floor(n/3) + 2 - n =====\n");
for n in [9..24] do
  kmax := QuoInt(n,2); if kmax mod 2 = 1 then kmax := kmax - 1; fi;
  jmax := QuoInt(n,3);
  Print("  n=", n, "  kmax=", kmax, " jmax=", jmax,
        "  => c(u) <= ", kmax + 2*jmax + 2 - n, "\n");
od;

Print("\nREE_DONE\n");
QUIT;
