# [U-6] crown census の埋め込み問題への分解(数学者・独立再構成)
#
# 模型: GT(N)/Phi = GT(N) = S_t x AGL(1,ell)   (Sol 便 114 §2.3 の生値)
#   wall24 = (t,ell)=(5,19) / wall28 = (5,23) / wall36 = (5,31) / wall37 = (6,31)
SizeScreen([4096,0]);;

# AGL(1,ell) を ell 点上の置換群として直接構成(GAP の AGL に依存しない)
MakeAGL1 := function(ell)
  local z, g, a, b, i;
  z := PrimitiveRoot(GF(ell));;
  a := PermList(List([1..ell], i -> ((i - 1 + 1) mod ell) + 1));;          # x -> x+1
  b := PermList(List([1..ell], i -> (Int((i-1) * IntFFE(z)) mod ell) + 1));;# x -> g*x
  return Group(a, b);
end;;

OmegaN := function(n) return Length(Set(FactorsInt(n))); end;;

Analyse := function(name, t, ell)
  local St, A, Q, der, mcl, c, M, core, P, soc, ab, inDer,
        nAb, nNonAb, nFree, nPaid, cores, idxNonAb, same, c0, P0,
        ns1, ns2, q1, q2, common;
  St := SymmetricGroup(t);;
  A  := MakeAGL1(ell);;
  Q  := DirectProduct(St, A);;
  der := DerivedSubgroup(Q);;
  Print("=== ", name, "  (t=", t, ", ell=", ell, ") ===\n");
  Print("  |S_t| = ", Size(St), "   |AGL(1,ell)| = ", Size(A), "   |Q| = ", Size(Q), "\n");
  Print("  |[Q,Q]| = ", Size(der), "   |Q^ab| = ", Size(Q)/Size(der),
        "   (theory 2*(ell-1) = ", 2*(ell-1), ")\n");
  Print("  |Phi(Q)| = ", Size(FrattiniSubgroup(Q)), "\n");

  mcl := ConjugacyClassesMaximalSubgroups(Q);;
  nAb := 0;; nNonAb := 0;; nFree := 0;; nPaid := 0;;
  cores := [];; idxNonAb := [];;
  Print("  --- maximal classes (", Length(mcl), ") ---\n");
  for c in mcl do
    M := Representative(c);;
    core := Core(Q, M);;
    P := Q / core;;
    soc := Socle(P);;
    ab := IsAbelian(soc);;
    inDer := IsSubset(M, der);;
    if ab then nAb := nAb + 1;
    else nNonAb := nNonAb + 1; Add(cores, core); Add(idxNonAb, Index(Q,M)); fi;
    if inDer then nFree := nFree + 1; else nPaid := nPaid + 1; fi;
    Print("    idx=", Index(Q,M), "  |core|=", Size(core), "  |Q/core|=", Size(P),
          "  soc=", StructureDescription(soc), "  abelian=", ab,
          "  M>=[Q,Q]=", inDer, "\n");
  od;
  Print("  abelian=", nAb, "  nonabelian=", nNonAb,
        "   (theory ab=", OmegaN(ell-1)+3,
        ", nonab=", Length(ConjugacyClassesMaximalSubgroups(St))-1, ")\n");
  Print("  M >= [Q,Q]  (free 候補) = ", nFree, "   (theory omega(ell-1)+2 = ", OmegaN(ell-1)+2, ")\n");
  Print("  M not >= [Q,Q] (paid 候補) = ", nPaid, "   (theory 1 + nonab)\n");

  Print("  --- nonabelian crowns ---\n");
  Print("    indices = ", idxNonAb, "\n");
  same := Length(Set(cores)) = 1;;
  Print("    core sizes = ", Set(cores, Size), "   ALL CORES EQUAL = ", same,
        "   (theory core = 1 x AGL, size ", ell*(ell-1), ")\n");
  if same then
    c0 := cores[1];;
    P0 := Q / c0;;
    Print("    common primitive quotient = ", StructureDescription(P0), " (order ", Size(P0), ")\n");
    Print("    socle = ", StructureDescription(Socle(P0)),
          "  |Z(socle)| = ", Size(Centre(Socle(P0))),
          "  |Out(socle)| = ", Size(AutomorphismGroup(Socle(P0)))/Size(Socle(P0)), "\n");
  fi;

  Print("  --- common quotients (Goursat / diagonal maximals) ---\n");
  ns1 := Filtered(NormalSubgroups(St), n -> Size(n) < Size(St));;
  ns2 := Filtered(NormalSubgroups(A),  n -> Size(n) < Size(A));;
  q1 := Set(List(ns1, n -> StructureDescription(St/n)));;
  q2 := Set(List(ns2, n -> StructureDescription(A/n)));;
  common := Filtered(Intersection(q1, q2), s -> s <> "1");;
  Print("    quotients of S_t : ", q1, "\n");
  Print("    quotients of AGL : ", q2, "\n");
  Print("    common nontrivial: ", common, "\n\n");
end;;

Analyse("wall24", 5, 19);
Analyse("wall28", 5, 23);
Analyse("wall36", 5, 31);
Analyse("wall37", 6, 31);
QUIT;
