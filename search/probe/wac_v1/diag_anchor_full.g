SizeScreen([4096,0]);;
## Full m=0 scan with the CORRECTED (orientation-consistent) generator:
##   literal acceptance test  <->  f in C_P(y^u) * hRep   (left coset)
## Compare the accepted set with the SURV family F = {(a1^z)*a1 : z in C_S24(v)}.
n := 24;;
a1 := ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23);;
b1 := ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23);;
Snn := SymmetricGroup(n);;
aE := a1*(25,27);;  bE := b1*(25,27,26);;
s1 := bE^-1*aE;;  s2 := aE*bE^2;;
x := s1^2;;  y := s2^2;;
P := Group(x,y);;
v := a1*b1^-1;;
m := 0;;  u := 2*m+1;;
cc := (s1*s2)^3;;

MHex := function(f)
  local l1,r1,l2,r2;
  l1 := s1^u * f^-1 * s2^u * f;
  r1 := f^-1 * s1 * s2 * x^(-m) * cc^m;
  if l1 <> r1 then return false; fi;
  l2 := f^-1 * s2^u * f * s1^u;
  r2 := s2 * s1 * y^(-m) * cc^m * f;
  return l2 = r2;
end;;
GenOK := function(f) return Group(x^u, f^-1*y^u*f) = P; end;;

Stb := Centralizer(Snn, x);;      stabElts := Elements(Stb);;
yu := y^u;;
Cyu := Centralizer(P, yu);;        cElts := Elements(Cyu);;
alpha0 := RepresentativeAction(Snn, x, x^u);;
Print("|Stb|=", Length(stabElts), " |C_P(y^u)|=", Length(cElts),
      " alpha0 found=", alpha0 <> fail, "\n");

acc := [];;  scanned := 0;;  hexPass := 0;;  assertFails := 0;;  si := 0;;
t0 := Runtime();;
for s in stabElts do
  si := si + 1;
  target := y^(s*alpha0);
  hRep := RepresentativeAction(P, yu, target, OnPoints);
  if hRep = fail then continue; fi;
  for c in cElts do
    f := c * hRep;                       ## <-- CORRECTED: left coset
    scanned := scanned + 1;
    if scanned mod 500000 = 0 then
      Print("  ... scanned=", scanned, " hexPass=", hexPass, " acc=", Length(acc),
            " t=", (Runtime()-t0)/1000.0, "s\n");
    fi;
    if not MHex(f) then continue; fi;
    hexPass := hexPass + 1;
    ## orientation self-assert: the constructed f must satisfy the equation the test uses
    if (yu^f) <> target then assertFails := assertFails + 1; fi;
    if not GenOK(f) then continue; fi;
    Add(acc, f);
  od;
od;
Print("scanned=", scanned, "  hex_pass=", hexPass, "  accepted=", Length(acc),
      "  orientation_assert_fails=", assertFails,
      "  elapsed=", (Runtime()-t0)/1000.0, "s\n");

accS := Set(acc);;
Fs := Set(List(Elements(Centralizer(Snn, y)), z -> (a1^z)*a1));;
Print("distinct accepted = ", Length(accS), "   |SURV F| = ", Length(Fs), "\n");
Print("ACCEPTED == SURV F (set equality, bit-level) ? ", accS = Fs, "\n");
Print("accepted subset F ? ", IsSubset(Fs, accS), "   F subset accepted ? ", IsSubset(accS, Fs), "\n");
Print("DIAG_FULL_DONE\n");
QUIT;
