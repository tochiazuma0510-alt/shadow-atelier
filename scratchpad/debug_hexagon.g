Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");

MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  return [r, s];
end;;
MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y));
end;;

gn := MakeGn(3);;
chat0 := Identity(gn.G);;
qt := BuildQTGeneral(gn.G, gn.x, gn.y, chat0);;
qt.xx := qt.s1^2;; qt.yy := qt.s2^2;; qt.cc := (qt.s1*qt.s2*qt.s1)^2;;
Print("qt.cc order (should be 1, since main window / dihedral c->1): ", Order(qt.cc), "\n");

# EvalFullHexagon via state machine (copy of logic from driver_step4)
EvalFullHexagon := function(m, f, phiX, phiY, phiC)
  local u, base, finv, xm, cm, lhs33, rhs33, lhs34, rhs34, s, ym;
  u := 2*m+1;
  finv := f^-1;
  xm := phiX^(-m);
  cm := phiC^m;
  base := [1, Identity(f)];
  s := ApplyGenPow(base, 1, u, phiX, phiY, phiC);
  s := ApplyQElt(s, finv);
  s := ApplyGenPow(s, 2, u, phiX, phiY, phiC);
  s := ApplyQElt(s, f);
  lhs33 := s;
  s := ApplyQElt(base, finv);
  s := ApplyGenPow(s, 1, 1, phiX, phiY, phiC);
  s := ApplyGenPow(s, 2, 1, phiX, phiY, phiC);
  s := ApplyQElt(s, xm);
  s := ApplyQElt(s, cm);
  rhs33 := s;
  s := ApplyQElt(base, finv);
  s := ApplyGenPow(s, 2, u, phiX, phiY, phiC);
  s := ApplyQElt(s, f);
  s := ApplyGenPow(s, 1, u, phiX, phiY, phiC);
  lhs34 := s;
  ym := phiY^(-m);
  s := ApplyGenPow(base, 2, 1, phiX, phiY, phiC);
  s := ApplyGenPow(s, 1, 1, phiX, phiY, phiC);
  s := ApplyQElt(s, ym);
  s := ApplyQElt(s, cm);
  s := ApplyQElt(s, f);
  rhs34 := s;
  return rec(hex33 := (lhs33 = rhs33), hex34 := (lhs34 = rhs34));
end;;

# EvalFullHexagon via literal PermList products (M5-script-style)
EvalFullHexagonPerm := function(m, fhat, s1, s2, xx, yy, cc)
  local u, fhatInv, lhs33, rhs33, lhs34, rhs34;
  u := 2*m+1; fhatInv := fhat^-1;
  lhs33 := s1^u * fhatInv * s2^u * fhat;
  rhs33 := fhatInv * s1*s2 * xx^(-m) * cc^m;
  lhs34 := fhatInv * s2^u * fhat * s1^u;
  rhs34 := s2*s1 * yy^(-m) * cc^m * fhat;
  return rec(hex33 := (lhs33=rhs33), hex34 := (lhs34=rhs34));
end;;

testElts := [Identity(gn.G), gn.x, gn.y, gn.x*gn.y, gn.x^2, (gn.x*gn.y)^3];;
for f in testElts do
  r1 := EvalFullHexagon(0, f, gn.x, gn.y, chat0);
  r2 := EvalFullHexagonPerm(0, f, qt.s1, qt.s2, qt.xx, qt.yy, qt.cc);
  Print("f=", f, "  stateMachine: hex33=", r1.hex33, " hex34=", r1.hex34,
        "   PermList: hex33=", r2.hex33, " hex34=", r2.hex34,
        "   AGREE=", (r1.hex33=r2.hex33) and (r1.hex34=r2.hex34), "\n");
od;
QUIT;
