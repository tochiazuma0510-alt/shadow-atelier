# u_meas_probe7.g -- decisive test: is Pbar a Weierstrass point after all?
#
# C -> P^1_t has an automorphism psibar over nu(t) = 3 - t (from the S3 in Aut(W)).
# psibar's fixed points lie over the nu-fixed points t = 3/2 and t = infinity.
#   over t = infinity : exactly 1 (the unique pole Pbar)
#   over t = 3/2      : #Fix_Lambda(varrho), varrho = the lift of nu
# For genus 2 an involution has 0, 2 or 6 fixed points.
#   total 6  <=> psibar = hyperelliptic involution <=> Pbar IS a Weierstrass pt (case (a))
#   total 2  <=> case (b)
# varrho must satisfy  Theta(A)^varrho = Theta(B),  Theta(B)^varrho = Theta(A),  varrho^2 = 1,
# and it normalises <Theta(A),Theta(B)> = PSL(2,8), so varrho in N_{S9}(P) = PGammaL(2,8).
# Raw measurements only.

Print("=== u_meas_probe7 : the involution psibar and #Fix ===\n");
CTd := function(p,d) local l; l := List(Orbits(Group(p),[1..d]),Length); Sort(l); return Reversed(l); end;

zz := Z(8);;
enc := function(k) local e,i; e := Zero(GF(8));
  for i in [0..2] do if (QuoInt(k,2^i) mod 2)=1 then e := e+zz^i; fi; od; return e; end;;
SM := [[enc(1),enc(0)],[enc(1),enc(1)]];;
TM := [[enc(4),enc(3)],[enc(1),enc(5)]];;
act := ActionHomomorphism(SL(2,8), NormedRowVectors(GF(8)^2), OnLines);;
sB := Image(act,SM);; tB := Image(act,TM);;
PB := Group(sB,tB);;  S9 := SymmetricGroup(9);;
XB := (tB^-1*sB)^2;; YB := (sB*tB^-1)^2;; ZB := (XB*YB)^-1;;
piB := tB^-1;;
TA := piB^-1;; TB2 := XB^-1*piB;; TC := (TA*TB2)^-1;;
Print("Theta(A) type=", CTd(TA,9), "  Theta(B) type=", CTd(TB2,9), "  Theta(C) type=", CTd(TC,9), "\n");
Print("Theta(C) = Y ? ", TC = YB, "\n");

Print("\n-- W-level: does psi (lift of lambda -> 1-lambda) exist ? --\n");
Print("  s^-1 X s = Y ? ", XB^sB = YB, "    s^-1 Y s = X ? ", YB^sB = XB, "\n");
Print("  #Fix_Lambda(s) = ", Number([1..9], i -> i^sB = i), "  type(s) = ", CTd(sB,9), "\n");
Print("  #Fix_Lambda(t) = ", Number([1..9], i -> i^tB = i), "  type(t) = ", CTd(tB,9), "\n");

Print("\n-- C-level: solve for varrho --\n");
NP := Normalizer(S9, PB);;
Print("  |N_{S9}(P)| = ", Size(NP), "\n");
cands := Filtered(Elements(NP), r -> TA^r = TB2 and TB2^r = TA);;
Print("  #{r in N_{S9}(P) : Theta(A)^r = Theta(B), Theta(B)^r = Theta(A)} = ", Length(cands), "\n");
for r in cands do
  Print("     ord=", Order(r), "  type=", CTd(r,9), "  #Fix=", Number([1..9], i -> i^r = i),
        "  in P ? ", r in PB, "\n");
od;
# also allow the whole of S9 (no normaliser assumption)
cands2 := Filtered(Elements(S9), r -> TA^r = TB2 and TB2^r = TA);;
Print("  (over all of S9): ", Length(cands2), " solutions; types = ",
      Set(List(cands2, r -> [Order(r), CTd(r,9), Number([1..9], i->i^r=i)])), "\n");

Print("\n-- conclusion inputs --\n");
for r in cands2 do
  if Order(r) = 2 then
    Print("  involution varrho: #Fix over t=3/2 is ", Number([1..9], i -> i^r = i),
          "  => total #Fix(psibar) = ", 1 + Number([1..9], i -> i^r = i), "\n");
  fi;
od;

# cross-check: genus of Y = C/psibar via Riemann-Hurwitz, for each possible f
Print("\n  genus(Y) from 2*g_C-2 = 2*(2*g_Y-2) + f :\n");
for f in [0,2,6] do
  Print("    f=", f, " -> g_Y = ", (2*2-2 - f + 4)/4, "\n");
od;
Print("=== done ===\n");
QUIT;
