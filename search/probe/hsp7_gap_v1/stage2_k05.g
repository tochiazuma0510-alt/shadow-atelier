## search/probe/hsp7_gap_v1/stage2_k05.g
## Stage 2: K(0,5) := PB4fp / <<Delta4^2>>  (Delta4^2 = (s1 s2 s3)^4, full
## twist, central; CENT-FREE: K(0,5) = PB4/Z(PB4), Sol-audited F100-1.4).
## Build the HS x_{i,i+1} <-> PB4 X_ij dictionary via the sphere row-product
## relation (HS2000 Trans.AMS p.3124-3125, j ascending, pinned by commander):
##   x_{i,5} = (x_{i,1} x_{i,2} x_{i,3} x_{i,4})^-1  (j asc, j<>i skipped)
## Then define rho on the 6 named generators of K(0,5) via rho(x_ij)=x_{i+3,j+3}
## (mod 5) and run fail-closed anchors:
##   (i)   K(0,5)^ab = Z^5
##   (ii)  rho is a well-defined automorphism of K(0,5)fp (relator-preserving)
##   (iii) rho^5 = identity on generators, rho <> identity
##   (iv)  j: F2=K(0,4) -> K(0,5), x|->x12, y|->x23 is well-defined
##         (trivially true since x12,x23 are just two of the generators;
##          real content is that <x12,x23> should behave like a free F2
##          quotient consistent with the K(0,4) embedding -- checked at
##          the p-quotient level in stage 3, not here)
## If (i)-(iii) fail: STOP (S-6), do not patch with Witt assumptions.

F := FreeGroup("s1","s2","s3");;
s1 := F.1;; s2 := F.2;; s3 := F.3;;
rels := [ s1*s3*s1^-1*s3^-1,
          s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := F / rels;;
b1 := B4.1;; b2 := B4.2;; b3 := B4.3;;

X12 := b1^2;;  X23 := b2^2;;  X34 := b3^2;;
X13 := b2*b1^2*b2^-1;;  X24 := b3*b2^2*b3^-1;;  X14 := b3*X13*b3^-1;;
gensPB4 := [X12,X13,X14,X23,X24,X34];;

PB4sub := Subgroup(B4, gensPB4);;
iso := IsomorphismFpGroupByGenerators(PB4sub, gensPB4);;
PB4fp := Image(iso);;
## generator order in PB4fp matches gensPB4 order: X12,X13,X14,X23,X24,X34
gPB4 := GeneratorsOfGroup(PB4fp);;
gX12 := gPB4[1];; gX13 := gPB4[2];; gX14 := gPB4[3];;
gX23 := gPB4[4];; gX24 := gPB4[5];; gX34 := gPB4[6];;

## Delta4^2 = (s1 s2 s3)^4, image in PB4fp via iso (Delta4^2 is central in
## B4 hence lies in PB4; ImageElm needs the element expressed as a PB4sub
## element first).
Delta2 := (b1*b2*b3)^4;;
Print("Delta4^2 in PB4sub? ", Delta2 in PB4sub, "\n");
Delta2img := ImageElm(iso, Delta2);;
Print("image of Delta4^2 in PB4fp (as a word) computed.\n");

## K(0,5)fp := PB4fp / <<Delta2img>>  (central elt -> normal closure = extra relator)
FPB4 := FreeGroupOfFpGroup(PB4fp);;
relsPB4 := RelatorsOfFpGroup(PB4fp);;
Delta2word := UnderlyingElement(Delta2img);;
K05fp := FPB4 / Concatenation(relsPB4, [Delta2word]);;
gK := GeneratorsOfGroup(K05fp);;
kX12 := gK[1];; kX13 := gK[2];; kX14 := gK[3];;
kX23 := gK[4];; kX24 := gK[5];; kX34 := gK[6];;

Print("=== stage2: K(0,5) = PB4fp / <<Delta4^2>> ===\n");
Print("K05fp: ", K05fp, "\n");

## anchor (i): K(0,5)^ab = Z^5
abK := AbelianInvariants(K05fp);;
Print("AbelianInvariants(K05fp) = ", abK, "  (expect [0,0,0,0,0] = Z^5)\n");
anchor_i := (abK = [0,0,0,0,0]);;
Print("anchor(i) K(0,5)^ab=Z^5 : ", anchor_i, "\n");

## sphere row-product dictionary (HS2000 p.3124-3125, j ascending):
##   x_{i,5} := (x_{i,1} x_{i,2} x_{i,3} x_{i,4})^-1  (j asc, j<>i, x_{ji}:=x_{ij})
x15 := (kX12*kX13*kX14)^-1;;
x25 := (kX12*kX23*kX24)^-1;;
x35 := (kX13*kX23*kX34)^-1;;
x45 := (kX14*kX24*kX34)^-1;;

## HS 5-generator set x_{1,2},x_{2,3},x_{3,4},x_{4,5},x_{5,1}:
hs_x12 := kX12;; hs_x23 := kX23;; hs_x34 := kX34;;
hs_x45 := x45;;  hs_x51 := x15;;

## rho(x_ij) = x_{i+3,j+3} mod 5 (indices in {1..5}, unordered pair
## normalised so first < second, i.e. x_{ji}:=x_{ij}), acting on all SIX
## PB4-level generators (X12,X13,X14,X23,X24,X34), each of which is some
## x_{i,j} with i,j in {1,2,3,4}:
##   X12=x12 -> x45          (i=1,j=2 -> i+3=4,j+3=5)
##   X13=x13 -> x14 = X14    (i=1,j=3 -> 4, 6mod5=1 -> pair {1,4})
##   X14=x14 -> x24 = X24    (i=1,j=4 -> 4, 7mod5=2 -> pair {2,4})
##   X23=x23 -> x15 (=x51)   (i=2,j=3 -> 5, 6mod5=1 -> pair {1,5})
##   X24=x24 -> x25          (i=2,j=4 -> 5, 7mod5=2 -> pair {2,5})
##   X34=x34 -> x12 = X12    (i=3,j=4 -> 6mod5=1,7mod5=2 -> pair {1,2})
rhoImages := [ x45, kX14, kX24, x15, x25, kX12 ];;
rhoHom := GroupHomomorphismByImagesNC(K05fp, K05fp, gK, rhoImages);;
Print("rho defined as GroupHomomorphismByImagesNC (NC = no consistency check yet)\n");

## anchor (ii): rho is a well-defined homomorphism, i.e. all relators of
## K05fp map to the identity under the images above. Check directly
## (this is the real consistency check, independent of NC).
relsK := RelatorsOfFpGroup(K05fp);;
FK := FreeGroupOfFpGroup(K05fp);;
CheckRelWD := function()
  local r, w, bad;
  bad := 0;
  for r in relsK do
    w := MappedWord(r, GeneratorsOfGroup(FK), rhoImages);
    if not IsOne(w) then
      bad := bad + 1;
    fi;
  od;
  return bad;
end;;
nbad := CheckRelWD();;
Print("anchor(ii) rho well-defined: relators mapping to non-identity = ", nbad, " / ", Length(relsK), "  (expect 0)\n");

Print("STAGE2_PARTIAL_DONE (rho^5 / rho<>id check deferred to p-quotient level, needs finite image)\n");
QUIT;
