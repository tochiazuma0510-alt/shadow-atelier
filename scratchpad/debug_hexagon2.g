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
  return rec(x := x, y := y, G := Group(x, y), r:=r, s:=s, tr:=tr);
end;;

gn := MakeGn(3);;
Print("|G3|=", Size(gn.G), "\n");
chat0 := Identity(gn.G);;

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
  return rec(hex33 := (lhs33 = rhs33), hex34 := (lhs34 = rhs34), lhs33:=lhs33,rhs33:=rhs33,lhs34:=lhs34,rhs34:=rhs34);
end;;

# Thm 4.3 for n=3: K_ord=6, X_3={0,2,3,5}, kappa(m)=m+1 (odd)/ -m (even) mod 3 (r order 3)
# genuine shadow: m=2,k=0 -> triple=(r^0,r^0,r^{-2 mod 3}) = (1,1,r)
fShadow := gn.tr(gn.r,3);;   # identity on blocks1,2, r-rotation on block3
Print("f (genuine Thm4.3 shadow candidate, m=2): ", fShadow, "\n");
r1 := EvalFullHexagon(2, fShadow, gn.x, gn.y, chat0);;
Print("GENUINE shadow m=2: hex33=", r1.hex33, " hex34=", r1.hex34, "\n");

# also test m=3 (odd), kappa(3)=3+1=4 mod3=1 -> triple=(1,1,r)
r2 := EvalFullHexagon(3, fShadow, gn.x, gn.y, chat0);;
Print("m=3 with SAME f (should differ from a real m=3 shadow, sanity/negative check): hex33=", r2.hex33, " hex34=", r2.hex34, "\n");

# m=5 (odd), kappa(5)=5+1=6mod3=0 -> triple=(1,1,1) i.e f=identity
r3 := EvalFullHexagon(5, Identity(gn.G), gn.x, gn.y, chat0);;
Print("GENUINE shadow m=5,f=1: hex33=", r3.hex33, " hex34=", r3.hex34, "\n");

# m=0 (even), kappa(0)=0 -> f=identity (trivial)
r4 := EvalFullHexagon(0, Identity(gn.G), gn.x, gn.y, chat0);;
Print("GENUINE shadow m=0,f=1: hex33=", r4.hex33, " hex34=", r4.hex34, "\n");
QUIT;
