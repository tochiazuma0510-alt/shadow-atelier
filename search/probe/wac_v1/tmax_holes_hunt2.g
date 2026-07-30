#############################################################################
## search/probe/wac_v1/tmax_holes_hunt2.g
##  hunt1 の残り穴。非生成 hit(= 非推移な分解)を捨てて A_n/S_n が出るまで続ける。
##  非生成 hit の個数も数える(= 「解はあるが推移でない」層の存在証拠)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
MakeCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

HuntOnce := function(n, w0, k, maxRestart, maxStep)
  local rs, pts, m, d, step, i, j, m2, d2, Def, mk, sub;
  mk := function(mm) return Product(List(mm, p -> (p[1],p[2])), ()); end;
  Def := function(mm) return NrMovedPoints((mk(mm)*w0^-1)^3); end;
  for rs in [1..maxRestart] do
    pts := Shuffle(ShallowCopy([1..n]));
    m := List([1..k], i -> [pts[2*i-1], pts[2*i]]);
    d := Def(m);
    for step in [1..maxStep] do
      if d = 0 then return mk(m); fi;
      i := Random([1..k]); j := Random([1..k]);
      m2 := List(m, ShallowCopy);
      if i = j then
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

DoHole := function(ell, t, k, rounds)
  local n, w0, r, a1, b1, G, An, Sn, nonGen, orbs, sizes;
  n := ell + t; w0 := MakeCyc([1..ell]);
  An := AlternatingGroup(n); Sn := SymmetricGroup(n);
  nonGen := 0; sizes := [];
  Print("\n=== ell=", ell, " t=", t, " n=", n, " k=", k, " ===\n");
  for r in [1..rounds] do
    a1 := HuntOnce(n, w0, k, 60, 6000);
    if a1 = fail then continue; fi;
    b1 := a1*w0^-1; G := Group(a1,b1);
    if G = An or G = Sn then
      Print("   *** A_n/S_n HIT (round ", r, ") ***  非生成 hit を ", nonGen,
            " 個捨てた\n     a1 = ", a1, "\n     b1 = ", b1, "\n");
      Print("     推移 ", IsTransitive(G,[1..n]), "  = A_n ", G=An, "\n");
      return true;
    fi;
    nonGen := nonGen + 1;
    orbs := List(Orbits(G,[1..n]), Length);
    AddSet(sizes, [Size(G), orbs]);
  od;
  Print("   A_n/S_n 出ず。非生成 hit ", nonGen, " 個。\n");
  Print("   出た群の(位数,軌道長)一覧: ", sizes, "\n");
  return false;
end;;

DoHole(11, 1, 4, 40);;
DoHole(11, 1, 6, 40);;
DoHole(17, 4, 10, 40);;
DoHole(23, 4, 12, 40);;
DoHole(25, 4, 14, 40);;
DoHole(25, 5, 14, 40);;
Print("\nTMAX_HOLES_HUNT2_DONE\n");
QUIT;
