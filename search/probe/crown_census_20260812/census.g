# crown census probe — 裁定 1040 発注(手術検定の強化札)の添付実測
# 対象 = Frattini 解像度表 v2(search/certs/frattini_resolution_v2_20260812.json)の 2 商:
#   [36,12]  = GT(K^(9))/Phi   (|X|=108, |Phi|=3)
#   [108,43] = GT(M)/Phi       (|X|=972, |Phi|=9, M = K^(9) cap N_S4)
# 内容 = 極大部分群の共役類 census(= crown/primitive 商の束)+ 非正規極大と導来部分群の交わり(直線対応)
# 純群論・算術入力ゼロ・u/c 非接触・封印非接触。ideator 即席 probe(正式 cert 化は implementer 回し)。
for pair in [[36,12],[108,43]] do
  G := SmallGroup(pair[1],pair[2]);
  Print("IdGroup=", pair, "  StructureDescription=", StructureDescription(G), "\n");
  Print("  d(G) (min gens) = ", Length(MinimalGeneratingSet(G)), "\n");
  Print("  AbelianInvariants = ", AbelianInvariants(G), "\n");
  D := DerivedSubgroup(G);
  Print("  |[G,G]| = ", Size(D), "  struct = ", StructureDescription(D), "\n");
  cls := ConjugacyClassesMaximalSubgroups(G);
  Print("  num conj classes of maximal subgroups = ", Length(cls), "\n");
  lines := [];
  for c in cls do
    M := Representative(c);
    Print("    index=", Index(G,M), "  classSize=", Size(c),
          "  normal=", IsNormal(G,M),
          "  |X/Core|=", Index(G, Core(G,M)),
          "  structM=", StructureDescription(M));
    if not IsNormal(G,M) then
      L := Intersection(M, D);
      Add(lines, L);
      Print("  |M cap [G,G]|=", Size(L), "  L normal=", IsNormal(G,L));
    fi;
    Print("\n");
  od;
  Print("  distinct (M cap [G,G]) among non-normal classes = ",
        Length(Set(lines)), " of ", Length(lines), "\n");
  Print("  |Phi(G)| (sanity, expect 1) = ", Size(FrattiniSubgroup(G)), "\n\n");
od;
QUIT;
