# u_meas_probe5.g (v2) -- the quotient cover C = W/phi -> P^1_t.
#
# CORRECTION over v1: the two order-3 orbifold generators A,B of
# pi_1^orb(O) = F2 semidirect C3 must satisfy AB in F2 (the puncture loop
# lifts to closed loops, since U -> O has 3 ends over 1 end).  Hence
#   A = (1,omega),  B = (x^{-1},omega^2),  AB = y^{-1},
#   Theta(A) = pi^-1,  Theta(B) = X^-1 * pi,  Theta((AB)^-1) = Y.
# (v1 used B = (x,omega), which maps to the SAME C3-generator as A and is
#  therefore not a standard geometric pair.  Fixed-point counts are unchanged
#  because X^-1*pi is conjugate to (X*pi^-1)^-1.)
# Raw measurements only.

Print("=== u_meas_probe5 v2 : quotient cover C = W/phi -> P^1_t ===\n");
CTd := function(p,d) local l; l := List(Orbits(Group(p),[1..d]),Length); Sort(l); return Reversed(l); end;
GenusRHd := function(gs,d) local ram,g; ram := 0;
  for g in gs do ram := ram + (d - Length(Orbits(Group(g),[1..d]))); od;
  return 1 - d + ram/2; end;

Print("\n-- Window A (d=10) --\n");
a1 := (1,2)(3,5)(4,10)(6,9);; b1 := (2,9,5)(3,4,10)(6,8,7);;
XA := (b1^-1*a1)^2;; YA := (a1*b1^-1)^2;;
piA := b1^-1;;
TA := piA^-1;; TB := XA^-1*piA;; TC := (TA*TB)^-1;;
Print("Theta(A) = pi^-1      type = ", CTd(TA,10), " ord=", Order(TA), " #fix=", Number([1..10],i->i^TA=i), "\n");
Print("Theta(B) = X^-1*pi    type = ", CTd(TB,10), " ord=", Order(TB), " #fix=", Number([1..10],i->i^TB=i), "\n");
Print("Theta(C) = (AB)^-1    type = ", CTd(TC,10), " ord=", Order(TC), "\n");
Print("Theta(C) = Y ? ", TC = YA, "   product=1 ? ", TA*TB*TC = (), "\n");
Print("monodromy = A10 ? ", Group(TA,TB) = AlternatingGroup(10), "\n");
Print("genus(C) via RH = ", GenusRHd([TA,TB,TC],10), "\n");

Print("\n-- Window B (d=9) --\n");
zz := Z(8);;
enc := function(k) local e,i; e := Zero(GF(8));
  for i in [0..2] do if (QuoInt(k,2^i) mod 2)=1 then e := e+zz^i; fi; od; return e; end;;
SM := [[enc(1),enc(0)],[enc(1),enc(1)]];;
TM := [[enc(4),enc(3)],[enc(1),enc(5)]];;
act := ActionHomomorphism(SL(2,8), NormedRowVectors(GF(8)^2), OnLines);;
sB := Image(act,SM);; tB := Image(act,TM);;
PB := Group(sB,tB);;  S9 := SymmetricGroup(9);;
XB := (tB^-1*sB)^2;; YB := (sB*tB^-1)^2;;
piB := tB^-1;;
UA := piB^-1;; UB := XB^-1*piB;; UC := (UA*UB)^-1;;
Print("Theta(A) type = ", CTd(UA,9), " ord=", Order(UA), " #fix=", Number([1..9],i->i^UA=i), "\n");
Print("Theta(B) type = ", CTd(UB,9), " ord=", Order(UB), " #fix=", Number([1..9],i->i^UB=i), "\n");
Print("Theta(C) type = ", CTd(UC,9), " ord=", Order(UC), "\n");
Print("Theta(C) = Y ? ", UC = YB, "   product=1 ? ", UA*UB*UC = (), "\n");
Print("monodromy = P ? ", Group(UA,UB) = PB, "\n");
Print("genus(C) via RH = ", GenusRHd([UA,UB,UC],9), "\n");

# Nielsen classes of the QUOTIENT passport (3^3, 3^3, 9) with monodromy PSL(2,8)
cq := (UC)^-1;;                       # = Theta(A)Theta(B) ; a 9-cycle
Print("\nc_q = Theta(A)Theta(B) : ord=", Order(cq), " type=", CTd(cq,9), "\n");
ord3 := Filtered(Elements(S9), g -> Order(g)=3 and NrMovedPoints(g)=9);;
Print("#fixed-point-free order-3 elements of S9 = ", Length(ord3), "\n");
solq := [];;
for g in ord3 do
  h := g^-1*cq;
  if Order(h)=3 and NrMovedPoints(h)=9 then Add(solq,[g,h]); fi;
od;
Print("#solutions (A,B) with AB=c_q, both of type 3^3 = ", Length(solq), "\n");
gs := List(solq, pr -> Size(Group(pr[1],pr[2])));;
Print("monodromy multiplicities = ", List(Set(gs), s -> [s, Number(gs,x->x=s)]), "\n");
sol504 := Filtered(solq, pr -> Size(Group(pr[1],pr[2]))=504);;
CSq := Centralizer(S9,cq);;
Print("|C_S9(c_q)| = ", Size(CSq), "\n");
orb := [];; seen := [];;
for pr in sol504 do
  if not pr in seen then
    o := Set(List(Elements(CSq), g -> [pr[1]^g,pr[2]^g]));
    Append(seen,o); Add(orb,o);
  fi;
od;
Print("#S9-classes of quotient dessins, monodromy 504 = ", Length(orb),
      "  sizes = ", List(orb,Length), "\n");
Print("ours is class ", First([1..Length(orb)], i -> [UA,UB] in orb[i]), "\n");

Print("\n=== done ===\n");
QUIT;
