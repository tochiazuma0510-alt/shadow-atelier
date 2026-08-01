SizeScreen([4096,0]);;
## Reproduce the SHIPPED (mixed-orientation) generator of wall_canary_24_20260801.g
## at m=0 and identify its 120 accepted elements exactly.
n := 24;;
a1 := ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23);;
b1 := ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23);;
Snn := SymmetricGroup(n);;
aE := a1*(25,27);;  bE := b1*(25,27,26);;
s1 := bE^-1*aE;;  s2 := aE*bE^2;;
x := s1^2;;  y := s2^2;;
P := Group(x,y);;
v := a1*b1^-1;;
m := 0;;  u := 2*m+1;;  cc := (s1*s2)^3;;

MHex := function(f)
  local l1,r1,l2,r2;
  l1 := s1^u * f^-1 * s2^u * f;   r1 := f^-1 * s1 * s2 * x^(-m) * cc^m;
  if l1 <> r1 then return false; fi;
  l2 := f^-1 * s2^u * f * s1^u;   r2 := s2 * s1 * y^(-m) * cc^m * f;
  return l2 = r2;
end;;
GenOK := function(f) return Group(x^u, f^-1*y^u*f) = P; end;;

Stb := Centralizer(Snn, x);;  stabElts := Elements(Stb);;
yu := y^u;;  Cyu := Centralizer(P, yu);;  cElts := Elements(Cyu);;
alpha0 := RepresentativeAction(Snn, x, x^u);;
acc := [];;  scanned := 0;;
t0 := Runtime();;
for s in stabElts do
  target := y^(s*alpha0);
  hRep := RepresentativeAction(P, yu, target, OnPoints);
  if hRep = fail then continue; fi;
  f0 := hRep^-1;
  for c in cElts do
    f := f0 * c;                     ## <-- SHIPPED (judge-orientation right coset)
    scanned := scanned + 1;
    if not MHex(f) then continue; fi;
    if not GenOK(f) then continue; fi;
    Add(acc, f);
  od;
od;
Print("scanned=", scanned, "  accepted=", Length(acc),
      "  elapsed=", (Runtime()-t0)/1000.0, "s\n");
accS := Set(acc);;
Cv := Centralizer(Snn, y);;
Fs := Set(List(Elements(Cv), z -> (a1^z)*a1));;
FinvS := Set(List(Fs, f -> f^-1));;
FFint := Intersection(Fs, FinvS);;
Print("|accepted set|=", Length(accS), "  |F cap F^-1|=", Length(FFint),
      "   accepted == F cap F^-1 ? ", accS = FFint, "\n");
Fixy := Difference([1..24], MovedPoints(y));;
zs := Filtered(Elements(Cv), z -> ((a1^z)*a1) in accS);;
Print("z-parameters of the accepted set: ", Length(zs),
      "  == Sym(Fix(ybar)) ? ", Set(zs) = Set(Elements(SymmetricGroup(Fixy))), "\n");
Print("ord(v)=", Order(v), "  N_ord=", Lcm(Order(x),Order(y),Order(cc)),
      "  |Cv| / |accepted| = ", 2280/Length(accS), "\n");
Print("DIAG_SHIPPED_DONE\n");
QUIT;
