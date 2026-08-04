## search/probe/hsp7_gap_v1/stage4_eval.g
## Stage 4: load the batch-pq outputs for P (=F2/(gamma5(F2)F2^7)) and
## Q (=K05fp/(gamma5*K05fp^7)), then run P101-1 conditions 2-4:
##  (2) |P|, LCS layers of P, |Q|, dim gamma4(Q)
##  (3) h4 <> 1 in gamma4(P)  (DUM-FIN word, no Exp/BCH/Lazard)
##  (4) j(h4) and rho evaluated from the presentation; direct test of
##      prod_{i=0}^4 rho^i(j(h4)) <> 1 in Q
## Stop rules S-6 / S-7' / NW-P8 checked and reported (not silently patched).

## --- load P ---
Read("search/probe/hsp7_gap_v1/PQ_OUTPUT_P.g");;
P := F;;  MapImagesP := ShallowCopy(MapImages);;
Unbind(F);; Unbind(MapImages);;

xP := MapImagesP[1];;  yP := MapImagesP[2];;

Print("=== P = F2 / (gamma_5(F2) F2^7) ===\n");
Print("|P| = ", Size(P), "  (NW-P2 predicts 7^8 = ", 7^8, ")\n");

lcsP := LowerCentralSeriesOfGroup(P);;
Print("LCS layer sizes of P: ");
lcsDimsP := List([1..Length(lcsP)-1], i -> LogInt(Size(lcsP[i])/Size(lcsP[i+1]), 7));;
Print(lcsDimsP, "  (NW-P2/8.7.2 Witt prediction: [2,1,2,3])\n");
Print("gamma_5(P) trivial? ", Size(lcsP[Length(lcsP)]) = 1, "\n");
DP := DerivedSubgroup(P);;
Print("|[P,P]| = ", Size(DP), "  (NW-P2 predicts 7^6 = ", 7^6, ")\n");

## DUM-FIN: h4 := [[[x,y],x],x] * [[[x,y],x],y]^4 * [[[x,y],y],y]
## group commutator convention Comm(a,b) = a^-1*b^-1*a*b (GAP native).
c1P := Comm(xP,yP);;             ## [x,y]
u1P := Comm(c1P,xP);;            ## [[x,y],x]  = v1
u2P := Comm(c1P,yP);;            ## [[x,y],y]
v1P := Comm(u1P,xP);;            ## [[[x,y],x],x]
v2P := Comm(u1P,yP);;            ## [[[x,y],x],y]
v3P := Comm(u2P,yP);;            ## [[[x,y],y],y]
h4P := v1P * v2P^4 * v3P;;

Print("h4 in P: identity? ", IsOne(h4P), "  (NW-P3 predicts h4<>1, i.e. FALSE expected)\n");
Print("h4 in gamma4(P) (i.e. in gamma_4 subgroup)? ", h4P in lcsP[4], "\n");
dimG4P := LogInt(Size(lcsP[4]), 7);;
Print("dim_F7 gamma4(P) = ", dimG4P, "  (NW-P3 predicts 3)\n");

## --- load Q ---
Read("search/probe/hsp7_gap_v1/PQ_OUTPUT_Q.g");;
Q := F;;  MapImagesQ := ShallowCopy(MapImages);;
Unbind(F);; Unbind(MapImages);;

## MapImagesQ[1..6] = images of gK = [kX12,kX13,kX14,kX23,kX24,kX34] in Q
qX12 := MapImagesQ[1];;  qX13 := MapImagesQ[2];;  qX14 := MapImagesQ[3];;
qX23 := MapImagesQ[4];;  qX24 := MapImagesQ[5];;  qX34 := MapImagesQ[6];;

Print("\n=== Q = K05fp / (gamma_5 K05fp^7) ===\n");
Print("|Q| = ", Size(Q), "  (NW-P4 predicts 7^40 = ", 7^40, ")\n");
lcsQ := LowerCentralSeriesOfGroup(Q);;
Print("gamma_5(Q) trivial? ", Size(lcsQ[Length(lcsQ)]) = 1, "\n");
dimG4Q := LogInt(Size(lcsQ[4]), 7);;
Print("dim_F7 gamma4(Q) = ", dimG4Q, "  (NW-P4 predicts 21)\n");

## rho on Q, via the sphere row-product dictionary (same formula as stage2,
## now evaluated with the actual images MapImagesQ instead of free words):
qx15 := (qX12*qX13*qX14)^-1;;
qx25 := (qX12*qX23*qX24)^-1;;
qx45 := (qX14*qX24*qX34)^-1;;
rhoImgQ := [ qx45, qX14, qX24, qx15, qx25, qX12 ];;

rhoQ := GroupHomomorphismByImages(Q, Q, MapImagesQ, rhoImgQ);;
Print("\nrho: GroupHomomorphismByImages succeeded (fail would mean inconsistent)? ",
      rhoQ <> fail, "\n");
if rhoQ = fail then
  Print("STOP S-6: rho is not a well-defined homomorphism on Q. INTEGRITY_STOP.\n");
  Print("STAGE4_ABORT_S6\n");
  Error("PREREGISTRATION_FALSIFIED / INTEGRITY_STOP (S-6: rho ill-defined)");
fi;
Print("rho bijective (automorphism)? ", IsBijective(rhoQ), "\n");

## rho^5 = id ?  rho <> id ?  (avoid CompositionMapping order ambiguity:
## apply ImageElm iteratively by hand instead)
RhoPow := function(g, k)
  local r, i;
  r := g;
  for i in [1..k] do
    r := ImageElm(rhoQ, r);
  od;
  return r;
end;;
isId5 := ForAll(MapImagesQ, g -> RhoPow(g,5) = g);;
isNotId1 := ForAny(MapImagesQ, g -> RhoPow(g,1) <> g);;
Print("rho^5 = identity on generators? ", isId5, "  (expect true)\n");
Print("rho <> identity? ", isNotId1, "  (expect true)\n");
if not isId5 or not isNotId1 then
  Print("STOP S-6: rho^5<>id or rho=id. INTEGRITY_STOP.\n");
  Print("STAGE4_ABORT_S6\n");
  Error("PREREGISTRATION_FALSIFIED / INTEGRITY_STOP (S-6: rho order check failed)");
fi;

## j(h4): x |-> qX12, y |-> qX23 (HS: x=x12, y=x23)
c1Q := Comm(qX12,qX23);;
u1Q := Comm(c1Q,qX12);;
u2Q := Comm(c1Q,qX23);;
v1Q := Comm(u1Q,qX12);;
v2Q := Comm(u1Q,qX23);;
v3Q := Comm(u2Q,qX23);;
jh4 := v1Q * v2Q^4 * v3Q;;
Print("\nj(h4) computed in Q. identity? ", IsOne(jh4), "\n");

## N_rho(j(h4)) = rho^4(jh4) * rho^3(jh4) * rho^2(jh4) * rho(jh4) * jh4
r1 := RhoPow(jh4,1);;
r2 := RhoPow(jh4,2);;
r3 := RhoPow(jh4,3);;
r4 := RhoPow(jh4,4);;
Nrho_jh4 := r4 * r3 * r2 * r1 * jh4;;
Print("N_rho(j(h4)) = rho^4(jh4)*rho^3(jh4)*rho^2(jh4)*rho(jh4)*jh4\n");
Print("N_rho(j(h4)) = identity? ", IsOne(Nrho_jh4), "  (NW-P5 predicts FALSE, i.e. nu4(j h4)<>0)\n");

Print("\nSTAGE4_DONE\n");
QUIT;
