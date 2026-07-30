#############################################################################
## search/probe/wac_v1/sat_l1_probe12.g
##  判別窓 A (n=14, w0=(7,7), k=6) と B (n=18, w0=(9,9), k=8) の witness を
##  局所探索(2-opt 山登り+再出発)で構成する。probe10 と同じ手法の一般化
##  (不動点を許す対合を探索空間にする)。
##  いずれも p=s=0 ゆえ C(w)=C(w^2)=Stab ==> CENT は定理として成立する窓。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
MakeCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

Hunt := function(n, w0, k, maxRestart, maxStep)
  local rs, pts, m, d, step, i, j, m2, d2, a, Def, mk, sub;
  mk := function(mm) return Product(List(mm, p -> (p[1],p[2])), ()); end;
  Def := function(mm) return NrMovedPoints((mk(mm)*w0^-1)^3); end;
  for rs in [1..maxRestart] do
    pts := Shuffle(ShallowCopy([1..n]));
    m := List([1..k], i -> [pts[2*i-1], pts[2*i]]);
    d := Def(m);
    for step in [1..maxStep] do
      if d = 0 then
        Print("    HIT: restart ", rs, " step ", step, "\n");
        return mk(m);
      fi;
      i := Random([1..k]); j := Random([1..k]);
      m2 := List(m, ShallowCopy);
      if i = j then
        ## 1 点を未使用点と交換(不動点の入れ替え)
        sub := Difference([1..n], Concatenation(m));
        if Length(sub) = 0 then continue; fi;
        m2[i] := [m[i][1], Random(sub)];
      elif Random([1,2]) = 1 then
        m2[i] := [m[i][1], m[j][1]]; m2[j] := [m[i][2], m[j][2]];
      else
        m2[i] := [m[i][1], m[j][2]]; m2[j] := [m[i][2], m[j][1]];
      fi;
      d2 := Def(m2);
      if d2 <= d then m := m2; d := d2; fi;
    od;
  od;
  return fail;
end;;

Try := function(n, cycs, k, label)
  local w0, a1, b1, G, Sn, Cw, l;
  Sn := SymmetricGroup(n);
  w0 := Product(List(cycs, MakeCyc));
  Print("\n=== ", label, "  n=", n, "  w0 型 ", CycleStructurePerm(w0), " ===\n");
  a1 := Hunt(n, w0, k, 600, 6000);
  if a1 = fail then Print("    NO HIT\n"); return false; fi;
  b1 := a1*w0^-1;
  G := Group(a1,b1);
  Cw := Centralizer(Sn, w0);
  Print("    a1 = ", a1, "\n    b1 = ", b1, "\n");
  Print("    a1^2=1 ", a1^2=(), "  b1^3=1 ", b1^3=(),
        "  a1 型 ", CycleStructurePerm(a1), "  b1 型 ", CycleStructurePerm(b1), "\n");
  Print("    b1^-1*a1 = w0 ? ", b1^-1*a1 = w0, "   sign(a1) = ", SignPerm(a1), "\n");
  Print("    <a1,b1>: 推移 ", IsTransitive(G,[1..n]),
        "  = A_n ? ", G = AlternatingGroup(n), "  = S_n ? ", G = SymmetricGroup(n), "\n");
  Print("    |C_Sn(w0)| = ", Size(Cw), "  ", StructureDescription(Cw), "\n");
  Print("    |C_Sn(w0^2)| = |Stab(xbar)| = ", Size(Centralizer(Sn, w0^2)),
        "   一致(=> CENT が定理)? ", Centralizer(Sn,w0) = Centralizer(Sn,w0^2), "\n");
  return true;
end;;

Try(14, [[1..7],[8..14]], 6, "候補 A: ell=7, r=2, CENT 98 vs PRUNE 14");;
Try(18, [[1..9],[10..18]], 8, "候補 B: ell=9, r=2, CENT 162 vs PRUNE 18");;
Print("\nSAT_L1_PROBE12_DONE\n");
QUIT;
