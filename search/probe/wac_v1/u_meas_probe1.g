# u_meas_probe1.g -- M0/M1/M2 for the u-measurement campaign, wave 1
#
# Window A : W-E-A10-9t1   (semilocal frame, Lambda = A10/A9, degree 10)
# Window B : S4 = PSL(2,8) case A, k=9 (BFC (W4) frame, Lambda = P/Borel, degree 9)
#
# Raw measurements only. No prediction values, no comparison to any prediction file.
# GAP 4.16.0, run via .\gap.ps1 (heap cap -o 2g).

Print("=== u_meas_probe1 : M0/M1/M2 ===\n");

# full cycle type (partition of the whole domain, fixed points included)
CycType := function(p, dom)
  local l;
  l := List(Orbits(Group(p), dom), Length);
  Sort(l);
  return Reversed(l);
end;

# genus from an ordered triple of permutations on dom (deg d, 3 branch points)
GenusRH := function(gs, dom)
  local d, s, g, ram;
  d := Length(dom);
  ram := 0;
  for g in gs do
    ram := ram + (d - Length(Orbits(Group(g), dom)));
  od;
  return 1 - d + ram/2;
end;

############################################################
Print("\n---------- Window A : W-E-A10-9t1 ----------\n");

nA   := 10;
domA := [1..10];
a1 := (1,2)(3,5)(4,10)(6,9);
b1 := (2,9,5)(3,4,10)(6,8,7);

Print("A.0  a1^2=() : ", a1^2 = (), "   b1^3=() : ", b1^3 = (), "\n");
Print("A.0  sgn(a1) = ", SignPerm(a1), "   sgn(b1) = ", SignPerm(b1), "\n");
GA := Group(a1,b1);
Print("A.0  |<a1,b1>| = ", Size(GA), "   = |A10| ? ", Size(GA) = Factorial(10)/2, "\n");
Print("A.0  <a1,b1> = A10 ? ", GA = AlternatingGroup(10), "\n");

wA := b1^-1*a1;;  vA := a1*b1^-1;;
XA := wA^2;;      YA := vA^2;;      ZA := (XA*YA)^-1;;

Print("A.0  w  = ", wA, "  ord=", Order(wA), "  type=", CycType(wA,domA), "\n");
Print("A.0  v  = ", vA, "  ord=", Order(vA), "  type=", CycType(vA,domA), "\n");
Print("A.0  X  = ", XA, "  ord=", Order(XA), "\n");
Print("A.0  Y  = ", YA, "  ord=", Order(YA), "\n");
Print("A.0  Z  = ", ZA, "  ord=", Order(ZA), "\n");
Print("A.0  X*Y*Z = () : ", XA*YA*ZA = (), "\n");
Print("A.0  Y = b1*X*b1^-1 ? ", YA = b1*XA*b1^-1, "\n");
Print("A.0  Z = b1*Y*b1^-1 ? ", ZA = b1*YA*b1^-1, "\n");
Print("A.0  Y = a1*X*a1    ? ", YA = a1*XA*a1, "\n");
Print("A.0  X,Y conj in A10 ? ", IsConjugate(AlternatingGroup(10),XA,YA), "\n");
Print("A.0  X,Z conj in A10 ? ", IsConjugate(AlternatingGroup(10),XA,ZA), "\n");

# --- M1 : ordered passport on Lambda = A10/A9 = 10 points (natural action)
Print("A.1  ordered passport (X,Y,Z) on Lambda(10 pts) = ",
      CycType(XA,domA), " ", CycType(YA,domA), " ", CycType(ZA,domA), "\n");
Print("A.1  monodromy group = <X,Y> order = ", Size(Group(XA,YA)),
      "   = A10 ? ", Group(XA,YA) = AlternatingGroup(10), "\n");
Print("A.1  transitive on 10 pts ? ", IsTransitive(Group(XA,YA),domA), "\n");
Print("A.1  TransitiveIdentification = ", TransitiveIdentification(Group(XA,YA)), "\n");

# (W3) check for H = A9 = point stabiliser
HA := Stabilizer(AlternatingGroup(10), 1);
Print("A.1  |H| = ", Size(HA), "  index = ", Index(AlternatingGroup(10),HA),
      "  N_P(H)=H ? ", Normalizer(AlternatingGroup(10),HA) = HA, "\n");

# --- M2 : genus
Print("A.2  genus (RH) = ", GenusRH([XA,YA,ZA],domA), "\n");

# --- order-3 automorphism of the cover (phi over mu: 0->1->infty)
piA := b1^-1;;
Print("A.3  pi = b1^-1 : pi^-1 X pi = Y ? ", XA^piA = YA,
      "   pi^-1 Y pi = Z ? ", YA^piA = ZA,
      "   pi^-1 Z pi = X ? ", ZA^piA = XA, "\n");
Print("A.3  ord(pi) = ", Order(piA), "\n");
Print("A.3  centraliser of <X,Y> in S10 = ", Size(Centralizer(SymmetricGroup(10),Group(XA,YA))), "\n");
ThA := piA^-1;;          # Theta(A) = pi^-1
ThB := XA*piA^-1;;       # Theta(B) = X * pi^-1
Print("A.3  Theta(A) = ", ThA, " ord=", Order(ThA),
      " #fix = ", Number(domA, i -> i^ThA = i), "\n");
Print("A.3  Theta(B) = ", ThB, " ord=", Order(ThB),
      " #fix = ", Number(domA, i -> i^ThB = i), "\n");
Print("A.3  (cross) #fix(X*pi) = ", Number(domA, i -> i^(XA*piA) = i),
      "  #fix(pi*X) = ", Number(domA, i -> i^(piA*XA) = i), "\n");

# minimal faithful transitive degree of A10 (no subgroup of index 9)
Print("A.4  |A10| = ", Factorial(10)/2, "   |S9| = ", Factorial(9),
      "   |A10|>|S9| ? ", Factorial(10)/2 > Factorial(9), "\n");

############################################################
Print("\n---------- Window B : S4 = PSL(2,8) case A, k=9 ----------\n");

q := 8;;
F := GF(q);;
zz := Z(q);;
enc := function(k)
  local e, i;
  e := Zero(GF(8));
  for i in [0..2] do
    if (QuoInt(k, 2^i) mod 2) = 1 then e := e + zz^i; fi;
  od;
  return e;
end;;

SM := [[enc(1),enc(0)],[enc(1),enc(1)]];;
TM := [[enc(4),enc(3)],[enc(1),enc(5)]];;
Print("B.0  det(S) = ", DeterminantMat(SM), "  det(T) = ", DeterminantMat(TM),
      "  (One = ", One(GF(8)), ")\n");
Print("B.0  tr(S) = ", SM[1][1]+SM[2][2], "  tr(T) = ", TM[1][1]+TM[2][2], "\n");

SLg := SL(2,8);;
Print("B.0  S in SL(2,8) ? ", SM in SLg, "   T in SL(2,8) ? ", TM in SLg, "\n");

P1 := NormedRowVectors(GF(8)^2);;
Print("B.0  |P^1(F_8)| = ", Length(P1), "\n");
domB := [1..Length(P1)];;
actB := ActionHomomorphism(SLg, P1, OnLines);;

sB := Image(actB, SM);;
tB := Image(actB, TM);;
Print("B.0  ord(s) = ", Order(sB), "   ord(t) = ", Order(tB), "\n");
PB := Group(sB,tB);;
Print("B.0  |<s,t>| = ", Size(PB), "  = 504 ? ", Size(PB) = 504, "\n");
Print("B.0  <s,t> simple ? ", IsSimpleGroup(PB), "\n");

wB := tB^-1*sB;;  vB := sB*tB^-1;;
XB := wB^2;;      YB := vB^2;;      ZB := (XB*YB)^-1;;
Print("B.0  ord(w) = ", Order(wB), "  type(w) = ", CycType(wB,domB), "\n");
Print("B.0  ord(X) = ", Order(XB), "  ord(Y) = ", Order(YB), "  ord(Z) = ", Order(ZB), "\n");
Print("B.0  X*Y*Z = () : ", XB*YB*ZB = (), "\n");
Print("B.0  Y = t*X*t^-1 ? ", YB = tB*XB*tB^-1, "   Z = t*Y*t^-1 ? ", ZB = tB*YB*tB^-1, "\n");
Print("B.0  X,Y conj in P ? ", IsConjugate(PB,XB,YB),
      "   X,Z conj in P ? ", IsConjugate(PB,XB,ZB), "\n");

# --- M1 : ordered passport on Lambda = P/Borel = 9 points
Print("B.1  ordered passport (X,Y,Z) on Lambda(9 pts) = ",
      CycType(XB,domB), " ", CycType(YB,domB), " ", CycType(ZB,domB), "\n");
Print("B.1  transitive ? ", IsTransitive(PB,domB),
      "   TransitiveIdentification = ", TransitiveIdentification(PB), "\n");
HB := Stabilizer(PB, 1);;
Print("B.1  |H| = ", Size(HB), "  index = ", Index(PB,HB),
      "  N_P(H)=H ? ", Normalizer(PB,HB) = HB,
      "  IdGroup(H) = ", IdGroup(HB), "\n");
Print("B.1  <X> regular on Lambda ? ",
      IsRegular(Group(XB), domB), "\n");
Print("B.1  t fixed-point free on Lambda ? ", Number(domB, i -> i^tB = i) = 0, "\n");

# --- M2 : genus
Print("B.2  genus (RH) = ", GenusRH([XB,YB,ZB],domB), "\n");

# --- order-3 automorphism
piB := tB^-1;;
Print("B.3  pi = t^-1 : pi^-1 X pi = Y ? ", XB^piB = YB,
      "   pi^-1 Y pi = Z ? ", YB^piB = ZB, "\n");
Print("B.3  centraliser of P in S9 = ", Size(Centralizer(SymmetricGroup(9),PB)), "\n");
ThAB := piB^-1;;
ThBB := XB*piB^-1;;
Print("B.3  Theta(A) ord=", Order(ThAB), " #fix = ", Number(domB, i -> i^ThAB = i), "\n");
Print("B.3  Theta(B) ord=", Order(ThBB), " #fix = ", Number(domB, i -> i^ThBB = i), "\n");

# structural: normaliser of <X> in Aut(P) = PGammaL(2,8)
Print("B.4  |N_P(<X>)| = ", Size(Normalizer(PB, Group(XB))), "\n");
Print("B.4  |C_P(X)| = ", Size(Centralizer(PB, XB)), "\n");
Print("B.4  |C_{S9}(X)| = ", Size(Centralizer(SymmetricGroup(9), XB)),
      "   |N_{S9}(<X>)| = ", Size(Normalizer(SymmetricGroup(9), Group(XB))), "\n");

############################################################
Print("\n---------- cross-window comparison ----------\n");
Print("C.0  A: deg=10 passport=(9,1)^3 genus=", GenusRH([XA,YA,ZA],domA), "\n");
Print("C.0  B: deg= 9 passport=(9)^3   genus=", GenusRH([XB,YB,ZB],domB), "\n");
Print("=== done ===\n");
QUIT;
