#############################################################################
## search/probe/wac_v1/tmax_holes_hunt.g
##  裁定 253 の GEN_FAIL 8 穴を、大きめの予算で 2-opt 再ハントする。
##  scan の予算は max_restart=60 / max_step=1500。ここは 800 / 8000(約 70 倍)。
##  窓族: r=1, p=s=0, w0 = (ell-cycle, 1^t), n = ell+t, a1 は k 互換(偶)。
##  ell 素数 かつ t>=3 の穴は「推移 ==> 原始(ell > n/2)==> Jordan ==> A_n」
##  なので、hit すれば窓は自動的に成立する。
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
  local rs, pts, m, d, step, i, j, m2, d2, Def, mk, sub;
  mk := function(mm) return Product(List(mm, p -> (p[1],p[2])), ()); end;
  Def := function(mm) return NrMovedPoints((mk(mm)*w0^-1)^3); end;
  for rs in [1..maxRestart] do
    pts := Shuffle(ShallowCopy([1..n]));
    m := List([1..k], i -> [pts[2*i-1], pts[2*i]]);
    d := Def(m);
    for step in [1..maxStep] do
      if d = 0 then return rec(a1 := mk(m), rs := rs, step := step); fi;
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

DoHole := function(ell, t, ks)
  local n, w0, k, R, a1, b1, G, lbl, An, Sn;
  n := ell + t;
  w0 := MakeCyc([1..ell]);
  Print("\n=== ell=", ell, " t=", t, " n=", n, "  w0=(", ell, ",1^", t, ") ===\n");
  for k in ks do
    R := Hunt(n, w0, k, 800, 8000);
    if R = fail then
      Print("   k=", k, " : NO HIT (800x8000)\n");
    else
      a1 := R.a1; b1 := a1*w0^-1;
      G := Group(a1, b1);
      An := AlternatingGroup(n); Sn := SymmetricGroup(n);
      if G = An then lbl := "A_n"; elif G = Sn then lbl := "S_n";
      else lbl := Concatenation("proper(|G|=", String(Size(G)), ")"); fi;
      Print("   k=", k, " : HIT rs=", R.rs, " step=", R.step,
            "  j=", NrMovedPoints(b1)/3, "  b1^3=1 ", b1^3=(),
            "  gen=", lbl, "\n");
      Print("     a1 = ", a1, "\n     b1 = ", b1, "\n");
      if lbl = "A_n" or lbl = "S_n" then return true; fi;
    fi;
  od;
  return false;
end;;

DoHole(11, 1, [4,6]);;
DoHole(17, 4, [10]);;
DoHole(23, 3, [12]);;
DoHole(23, 4, [12]);;
DoHole(25, 4, [14]);;
DoHole(25, 5, [14]);;
DoHole(29, 5, [16]);;
DoHole(29, 7, [18]);;
Print("\nTMAX_HOLES_HUNT_DONE\n");
QUIT;
