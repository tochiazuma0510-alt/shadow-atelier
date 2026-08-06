## falsifier: the MISSING positive control for BIT-252 -- a calibration
## fixture evaluated in P' (the window where the 0/117649 was measured).
## Read-only; writes nothing into search/ or docs/.
##
## Claim under test: HexPass(P', theta', tau', y', m=6, f=1) MUST be TRUE.
## Reason: at m=-1 (=6 mod 7), f=1 the reduced hexagon (3.11) reads
##   tau^2(y^-1) tau(y^-1) y^-1 = x^-1 (xy) y^-1 = 1,
## an identity in the FREE group F2 -- hence true in every quotient
## (= the complex-conjugation shadow, 補題 PIN-A / MIRROR-SHADOW).
## The order-reversed form y^-1 (xy) x^-1 = [y,x^-1] is NOT 1, so this
## fixture has genuine separation power over the W-4 product-order bug.
if LoadPackage("anupq") <> true then Error("anupq missing"); fi;
F2 := FreeGroup("x","y");;
Print("building P (7^8)...\n");
P := Pq(F2 : Prime := 7, ClassBound := 4, Exponent := 7);;
Print("|P| = ", Size(P), "\n");
Print("building P' (7^14)...\n");
Pp := Pq(F2 : Prime := 7, ClassBound := 5, Exponent := 7);;
Print("|P'| = ", Size(Pp), "\n");
gp := GeneratorsOfGroup(Pp);; xPp := gp[1];; yPp := gp[2];;
thetaPp := GroupHomomorphismByImages(Pp, Pp, [xPp,yPp], [yPp,xPp]);;
tauPp   := GroupHomomorphismByImages(Pp, Pp, [xPp,yPp], [yPp,(xPp*yPp)^-1]);;
Print("theta' ok? ", thetaPp <> fail, "  tau' ok? ", tauPp <> fail, "\n");
Print("tau'^3 = id on gens? ",
  ImageElm(tauPp,ImageElm(tauPp,ImageElm(tauPp,xPp))) = xPp and
  ImageElm(tauPp,ImageElm(tauPp,ImageElm(tauPp,yPp))) = yPp, "\n");

## driver's predicate, verbatim
HexPass := function(G, thetaHom, tauHom, yGen, m, f)
  local hex1, ymf, t1v, t2v, hex2;
  hex1 := (f * ImageElm(thetaHom, f) = One(G));;
  ymf := yGen^m * f;;
  t1v := ImageElm(tauHom, ymf);;
  t2v := ImageElm(tauHom, t1v);;
  hex2 := (t2v * t1v * ymf = One(G));;
  return hex1 and hex2;;
end;;
## order-REVERSED variant (what a W-4 slip would compute)
HexPassRev := function(G, thetaHom, tauHom, yGen, m, f)
  local hex1, ymf, t1v, t2v, hex2;
  hex1 := (f * ImageElm(thetaHom, f) = One(G));;
  ymf := yGen^m * f;;
  t1v := ImageElm(tauHom, ymf);;
  t2v := ImageElm(tauHom, t1v);;
  hex2 := (ymf * t1v * t2v = One(G));;
  return hex1 and hex2;;
end;;

Print("\n=== POSITIVE CONTROL IN P' (the missing fixture) ===\n");
Print("  P'-F1  (m=0,f=1)  [trivially true even if tau is broken] : ",
      HexPass(Pp,thetaPp,tauPp,yPp,0,One(Pp)), "\n");
Print("  P'-F2  (m=6,f=1)  MUST BE TRUE (PIN-A, free-group identity): ",
      HexPass(Pp,thetaPp,tauPp,yPp,6,One(Pp)), "\n");
Print("  separation: order-reversed variant at (m=6,f=1) [must be FALSE]: ",
      HexPassRev(Pp,thetaPp,tauPp,yPp,6,One(Pp)), "\n");
Print("  P'-F2 at m=1 (no theorem; informational)                 : ",
      HexPass(Pp,thetaPp,tauPp,yPp,1,One(Pp)), "\n");

## same three in P, for comparison with the driver's recorded F-1/F-2
gpP := GeneratorsOfGroup(P);; xP := gpP[1];; yP := gpP[2];;
thetaP := GroupHomomorphismByImages(P,P,[xP,yP],[yP,xP]);;
tauP := GroupHomomorphismByImages(P,P,[xP,yP],[yP,(xP*yP)^-1]);;
Print("\n=== same fixtures in P (cross-ref to cert F1/F2) ===\n");
Print("  P-F1 (m=0,f=1): ", HexPass(P,thetaP,tauP,yP,0,One(P)), "\n");
Print("  P-F2 (m=6,f=1): ", HexPass(P,thetaP,tauP,yP,6,One(P)), " (cert says true)\n");
Print("  P-F2 reversed : ", HexPassRev(P,thetaP,tauP,yP,6,One(P)), " (must be FALSE)\n");
Print("\nPCONTROL_DONE\n");
