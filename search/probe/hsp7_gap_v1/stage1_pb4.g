## search/probe/hsp7_gap_v1/stage1_pb4.g
## Stage 1: build B4 (Artin presentation), PB4 as explicit subgroup via
## x_ij words (formula pinned: litgate_pentagon_v1.md sec6, HS2000 Appendix),
## verify [B4:PB4]=24 by coset enumeration, Reidemeister-Schreier to an
## independent FpGroup presentation of PB4 on generators X12,X13,X14,X23,X24,X34.
## Single GAP lane. Not a ledger claim by itself -- feeds stage2/stage3.

F := FreeGroup("s1","s2","s3");;
s1 := F.1;; s2 := F.2;; s3 := F.3;;
rels := [ s1*s3*s1^-1*s3^-1,
          s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := F / rels;;
b1 := B4.1;; b2 := B4.2;; b3 := B4.3;;

## x_ij := sigma_{j-1}...sigma_{i+1} sigma_i^2 sigma_{i+1}^-1...sigma_{j-1}^-1
## (A.2)/(A.4), litgate_pentagon_v1.md sec6 pin.
X12 := b1^2;;
X23 := b2^2;;
X34 := b3^2;;
X13 := b2*b1^2*b2^-1;;
X24 := b3*b2^2*b3^-1;;
X14 := b3*X13*b3^-1;;

gensPB4 := [X12,X13,X14,X23,X24,X34];;
namesPB4 := ["X12","X13","X14","X23","X24","X34"];;

Print("=== stage1: B4/PB4 construction ===\n");
PB4sub := Subgroup(B4, gensPB4);;
idx := Index(B4, PB4sub);;
Print("[B4:PB4] (coset enumeration) = ", idx, "  (expect 24)\n");

## Reidemeister-Schreier: independent fp presentation of PB4 on the SAME
## 6 named generators (not new Schreier generators), via IsomorphismFpGroupByGenerators.
iso := IsomorphismFpGroupByGenerators(PB4sub, gensPB4);;
PB4fp := Image(iso);;
Print("PB4fp: ", PB4fp, "\n");
Print("Number of generators of PB4fp = ", Length(GeneratorsOfGroup(PB4fp)), "  (expect 6)\n");
Print("Number of relators of PB4fp = ", Length(RelatorsOfFpGroup(PB4fp)), "\n");

## sanity: abelianization of PB4fp should be Z^6 (pure braid group PB4 is
## torsion-free with H_1 = Z^6, one Z per generator X_ij, standard fact).
ab := AbelianInvariants(PB4fp);;
Print("AbelianInvariants(PB4fp) = ", ab, "  (expect [0,0,0,0,0,0] = Z^6)\n");

Print("STAGE1_DONE\n");
QUIT;
