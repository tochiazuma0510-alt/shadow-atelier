## d972_survival_noncomm_inventory_v1.g
## Task 134 engineering probe.  This file deliberately contains only ASCII.
## NOT the official producer: local GAP startup failed before this file was
## read.  Pq's lower exponent-2 central quotients are also a separate family
## from the truncated-Magnus dimension quotient used by the Python producer.
##
## Input/scope:
##   - public M roof quotient through MakeGn(9);
##   - characteristic lower exponent-2 central quotients of F2;
##   - no sealed quantities and no arithmetic/genuine type labels.
## Output (probe phase): raw group orders and kernel structure on stdout.
## Invariants checked: natural epimorphism to G9, theta/tau descent and
## stability of the relative kernel.

Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");

if LoadPackage("anupq") <> true then
  Error("anupq LoadPackage failed");
fi;

F2 := FreeGroup("x", "y");;
g9 := MakeGn(9);;

Print("G9 order=", Size(g9.G), " abinv=", AbelianInvariants(g9.G), "\n");

for cls in [1..5] do
  Print("BEGIN class=", cls, "\n");
  P := Pq(F2 : Prime := 2, ClassBound := cls);;
  pg := GeneratorsOfGroup(P);;
  xP := pg[1];; yP := pg[2];;
  thetaP := GroupHomomorphismByImages(P, P, [xP,yP], [yP,xP]);;
  tauP := GroupHomomorphismByImages(P, P, [xP,yP], [yP,(xP*yP)^-1]);;
  Print("P order=", Size(P), " abinv=", AbelianInvariants(P),
        " theta=", thetaP <> fail, " tau=", tauP <> fail, "\n");

  DP := DirectProduct(g9.G, P);;
  e9 := Embedding(DP, 1);; ep := Embedding(DP, 2);;
  xE := Image(e9, g9.x) * Image(ep, xP);;
  yE := Image(e9, g9.y) * Image(ep, yP);;
  E := Group(xE, yE);;
  pi9 := GroupHomomorphismByImages(E, g9.G, [xE,yE], [g9.x,g9.y]);;
  if pi9 = fail then Error("projection E->G9 failed"); fi;
  Wker := Kernel(pi9);;
  thetaE := GroupHomomorphismByImages(E, E, [xE,yE], [yE,xE]);;
  tauE := GroupHomomorphismByImages(E, E, [xE,yE], [yE,(xE*yE)^-1]);;
  if thetaE = fail or tauE = fail then Error("theta/tau on E failed"); fi;
  Print("E order=", Size(E), " projection_image=", Size(Image(pi9)),
        " Wker_order=", Size(Wker), " Wker_abelian=", IsAbelian(Wker),
        " Wker_abinv=", AbelianInvariants(Wker),
        " theta_stable=", Image(thetaE,Wker)=Wker,
        " tau_stable=", Image(tauE,Wker)=Wker, "\n");
  if Size(Wker) <= 2000 and IdGroupsAvailable(Size(Wker)) then
    Print("Wker_id=", IdGroup(Wker), "\n");
  else
    Print("Wker_id=unavailable\n");
  fi;
  Print("END class=", cls, "\n");
od;

Print("DRIVER_DONE\n");
