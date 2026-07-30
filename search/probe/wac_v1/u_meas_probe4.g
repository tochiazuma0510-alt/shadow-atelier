# u_meas_probe4.g -- class vectors of the 6 S4 dessins (C1' refinement of the passport)
# and the Galois-type twist X -> X^u.  Raw measurements only.

Print("=== u_meas_probe4 : class vectors ===\n");
zz := Z(8);;
enc := function(k) local e,i; e := Zero(GF(8));
  for i in [0..2] do if (QuoInt(k,2^i) mod 2)=1 then e := e+zz^i; fi; od; return e; end;;
SM := [[enc(1),enc(0)],[enc(1),enc(1)]];;
TM := [[enc(4),enc(3)],[enc(1),enc(5)]];;
act := ActionHomomorphism(SL(2,8), NormedRowVectors(GF(8)^2), OnLines);;
sB := Image(act,SM);; tB := Image(act,TM);;
PB := Group(sB,tB);;  S9 := SymmetricGroup(9);;
X0 := (tB^-1*sB)^2;; Y0 := (sB*tB^-1)^2;; c := X0*Y0;;

cc := ConjugacyClasses(PB);;
Print("P conj classes (order, size) = ", List(cc, k -> [Order(Representative(k)), Size(k)]), "\n");
whichcl := function(g) return First([1..Length(cc)], i -> g in cc[i]); end;;

ord9 := Filtered(Elements(S9), g -> Order(g)=9 and NrMovedPoints(g)=9);;
sols := [];;
for XX in ord9 do
  YY := XX^-1*c;
  if Order(YY)=9 and NrMovedPoints(YY)=9 and Size(Group(XX,YY))=504 then Add(sols,[XX,YY]); fi;
od;
CS := Centralizer(S9,c);;
classes := [];; seen := [];;
for pr in sols do
  if not pr in seen then
    o := Set(List(Elements(CS), g -> [pr[1]^g, pr[2]^g]));
    Append(seen,o); Add(classes,o);
  fi;
od;
Print("#classes = ", Length(classes), "\n");
for i in [1..Length(classes)] do
  pr := classes[i][1];
  Print("class ", i, "  class-vector (X,Y,Z) = ",
        [whichcl(pr[1]), whichcl(pr[2]), whichcl((pr[1]*pr[2])^-1)], "\n");
od;
Print("window triple class-vector = ",
      [whichcl(X0), whichcl(Y0), whichcl((X0*Y0)^-1)],
      "  in class ", First([1..6], i -> [X0,Y0] in classes[i]), "\n");

# powering map on the order-9 classes: u -> class of X^u
i9 := Filtered([1..Length(cc)], i -> Order(Representative(cc[i]))=9);;
Print("order-9 class indices = ", i9, "\n");
for u in [1,2,4,5,7,8] do
  Print("  u=", u, " : ", List(i9, i -> whichcl(Representative(cc[i])^u)), "\n");
od;
Print("=== done ===\n");
QUIT;
