#############################################################################
## search/probe/wac_v1/sat_l1_probe7.g
##  (A) n=12 の 3840 障害の同定(悉皆再現 + 群の構造・原始性・ブロック)
##  (B) Frobenius 計数機構の構築と較正:
##      T(w0) := #{ (a1,b1) : a1^2=1, b1^3=1, b1^-1*a1 = w0 }
##      を対称群指標表の class multiplication coefficient で計算し、
##      直接走査の値と突合する。T/|C(w0)| = 軌道数 N_total(自由作用ゆえ)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
CycFromList := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

## ---- (A) n=12 悉皆の再現と 3840 の同定 ----
Print("=== (A) n=12, w0=(5,5,2) の悉皆再現と障害群の同定 ===\n");
IdentifyN12 := function()
  local n, w0, S, cl, a1, b1, hits, G, orbs, bl, i, sizes, prim;
  n := 12;
  w0 := CycFromList([1,2,3,4,5]) * CycFromList([6,7,8,9,10]) * (11,12);
  S := SymmetricGroup(n);
  Print("  w0 = ", w0, "  型 ", CycleStructurePerm(w0), " ord ", Order(w0), "\n");
  Print("  |C_S12(w0)| = ", Size(Centralizer(S,w0)), "\n");
  cl := First(ConjugacyClasses(S), c -> CycleStructurePerm(Representative(c)) =
             CycleStructurePerm((1,2)(3,4)(5,6)(7,8)(9,10)));
  Print("  a1 類 (2^5 1^2) の大きさ = ", Size(cl), "\n");
  hits := [];
  for a1 in Elements(cl) do
    b1 := a1*w0^-1;
    if b1^3 = () and b1 <> () and
       CycleStructurePerm(b1) = CycleStructurePerm((1,2,3)(4,5,6)(7,8,9)(10,11,12))
    then Add(hits, [a1,b1]); fi;
  od;
  Print("  b1 型 (3^4) 適合対の個数 = ", Length(hits), "\n");
  sizes := Set(List(hits, h -> Size(Group(h[1],h[2]))));
  Print("  生成群の位数(集合) = ", sizes, "\n");
  G := Group(hits[1][1], hits[1][2]);
  Print("  代表: |G| = ", Size(G), "   推移的? ", IsTransitive(G,[1..n]),
        "   原始的? ", IsPrimitive(G,[1..n]), "\n");
  Print("    軌道 = ", List(Orbits(G,[1..n]), Length), "\n");
  Print("    構造 = ", StructureDescription(G), "\n");
  if IsTransitive(G,[1..n]) then
    bl := AllBlocks(G);
    Print("    ブロック系の代表(最初の 6 個)= ", bl{[1..Minimum(6,Length(bl))]}, "\n");
    Print("    ブロックの大きさ(集合)= ", Set(List(bl, Length)), "\n");
  fi;
  Print("    G は互換を含む? ", ForAny(GeneratorsOfGroup(G), x->false) or
        ForAny(Elements(Group(w0)), x -> CycleStructurePerm(x)=CycleStructurePerm((1,2))), "\n");
  Print("    w0^5 = ", w0^5, "  (互換ならこれが G に入る)\n");
  return true;
end;;
IdentifyN12();;

## ---- (B) Frobenius 計数 ----
Print("\n=== (B) Frobenius 計数(指標表)と直接走査の突合 ===\n");
PartOf := function(p, n)   ## 置換 -> 分割(降順・不動点込み)
  local l;
  l := List(Cycles(p, [1..n]), Length);
  Sort(l); return Reversed(l);
end;;

CountFrob := function(n, wpart, verbose)
  local tbl, cp, idx, kk, i, j, tot, ci, cj, part, invs, thr, c, contrib;
  tbl := CharacterTable("Symmetric", n);
  cp := ClassParameters(tbl);
  idx := function(part)
    local t; t := ShallowCopy(part); Sort(t);
    return First([1..Length(cp)], z -> SortedList(cp[z][2]) = t);
  end;
  kk := idx(wpart);
  if kk = fail then Print("  class not found\n"); return fail; fi;
  invs := []; thr := [];
  for i in [1..Length(cp)] do
    part := cp[i][2];
    if ForAll(part, e -> e in [1,2]) then Add(invs, i); fi;
    if ForAll(part, e -> e in [1,3]) then Add(thr, i); fi;
  od;
  tot := 0;
  for i in invs do for j in thr do
    c := ClassMultiplicationCoefficient(tbl, j, i, kk);
    tot := tot + c;
    if verbose and c > 0 then
      Print("      a1 型 ", cp[i][2], " x b1 型 ", cp[j][2], " -> ", c, "\n");
    fi;
  od; od;
  return tot;
end;;

Calib := function(n, wpart, label)
  local Sn, w0, cw, T, l, p;
  Sn := SymmetricGroup(n);
  l := []; p := 1;
  for c in wpart do
    if c > 1 then Add(l, CycFromList([p..p+c-1])); fi;
    p := p + c;
  od;
  w0 := Product(l);
  cw := Size(Centralizer(Sn, w0));
  T := CountFrob(n, wpart, true);
  Print("  ", label, "  w=", wpart, "   |C_Sn(w)| = ", cw,
        "   T(全分解数) = ", T,
        "   N_total = T/|C| = ", T/cw, "\n");
  return true;
end;;

Calib(10, [5,5], "n=10 p=0 (存在しない窓)");;
Calib(10, [10],  "n=10 p=1 (実在する窓 |ker|=10)");;
Calib(12, [5,5,2], "n=12 P-CENT-2 (悉皆陰性)");;
Calib(15, [10,5], "n=15 r=3 (実在する窓 |ker|=50)");;
Print("\nSAT_L1_PROBE7_DONE\n");
QUIT;
