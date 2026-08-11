## search/xd1_chk_v1.g -- XD-1 machine verification (裁定811, docs/notes/ideas_chi_door_assault_v1.md
## §XD-1, commit c5a02ae). Two objects, per the card's own stated construction and "検証点"/
## "最小構成の答え" text (there is no separate formal DOMAIN-PIN table for XD-1 itself -- the
## card's XD-3 P-XD3 table is the STYLE reference per the commander's instruction; the specific
## quantities measured below are exactly the ones the card's XD-1 prose names, nothing more).
##
## ============ Object A: repair window G' = SL(2,691) x (C690 x_{C2} S3) ============
## Construction (verbatim per card SS XD-1 "修理(最小)"): triple-diagonal map
##   B3 -> SL(2,691) x C690 x S3
## via sigma1,sigma2 |-> (A,B mod 691; 1,1 in C690 (writhe map); (1,2),(2,3) in S3).
## A,B are the CLASSICAL B3->SL(2,Z) generators (independently re-derived and verified here,
## not copied from elsewhere): A=[[1,1],[0,1]], B=[[1,0],[-1,1]] -- braid relation A*B*A=B*A*B
## checked directly below (both sides compute to [[0,1],[-1,0]]), and c:=(sigma1 sigma2 sigma1)^2
## maps to (A*B*A)^2 = -I (checked directly, matching the card's explicit claim "c->-I").
## The image (Goursat, per the card) is the FIBER PRODUCT SL(2,691) x (C690 x_{C2} S3), since
## the two C2-projections (C690's parity map, S3's sign map) AGREE on sigma_i (both are "odd"/
## nontrivial for each generator -- checked directly below, this is the "pattern" check).
##
## Verified points (the "5 points" the commander named: S3 surjection / pattern / N<=PB3 /
## c not in N / e=690):
##   (1) S3 surjection: sigma1,sigma2's S3-coordinate images generate S3 (trivial by
##       construction -- (1,2),(2,3) generate S3 -- checked).
##   (2) pattern (C2-gluing compatibility): parity(writhe image of sigma_i in C690) matches
##       sign(S3 image of sigma_i), for each generator.
##   (3) N<=PB3: the S3-coordinate of this map IS EXACTLY the project's standard B3->S3 map
##       (sigma_i |-> the same transpositions used throughout this project, e.g.
##       search/hcen_ab_v1.g's S3can/(1,2),(2,3) convention) -- so ker(B3->G') is contained in
##       ker(standard B3->S3)=PB3 by construction; checked by confirming the S3-coordinate map
##       literally match that convention (not a different/incompatible S3-realization).
##   (4) c not in N: c's image (-I, 6 mod 690, 1 in S3) is checked to be NOT the identity triple
##       (the SL(2,691)-coordinate alone, -I, already suffices).
##   (5) e=690 (G'^ab = C690): argued via G'=SL(2,691) x H (H:=C690 x_{C2} S3, order 2070,
##       DIRECT product with the SL(2,691) factor per the card's own Goursat argument) -- since
##       SL(2,691) is PERFECT for 691>3 (checked via IsPerfect(SL(2,691)) below, a GAP structural
##       computation on the classical group, NOT full enumeration of its 329,930,280 elements),
##       AbelianInvariants(G') = AbelianInvariants(H) exactly. H itself is small (order 2070) and
##       built/measured directly and exactly below.
##
## ============ Object B: empty carrier G0 = (C691 : (C6 x_{C2} S3)) x C115 ============
## *** DISCLOSED CONSTRUCTION CHOICE (not fully pinned down in the card's prose -- the card says
## only "作用は位数6=六角固有値zeta6経由でB3-実現可能", without specifying WHICH order-6
## quotient of C6 x_{C2} S3 acts) ***: this script uses the NATURAL projection
## pi: C6 x_{C2} S3 -> C6 (first coordinate; well-defined and SURJECTIVE since for any a in C6,
## an element b in S3 with sign(b)=a mod 2 always exists -- checked below), composed with an
## embedding C6 -> Aut(C691)=C690 sending a generator of C6 to an order-6 element of
## (Z/691Z)^* (g^115 for a primitive root g mod 691, since 690=6*115). This is a natural,
## well-motivated choice achieving all the OUTCOME properties the card names (ab=C690 cyclic,
## c not in N, twist order=6) -- but it is disclosed as A choice, not asserted to be the unique
## or originally-intended one, per this project's discipline against silently resolving
## underspecified constructions.
## Verified: both congruences (345 | j via ab, 691 | |G0|), window-adjacent structural checks
## (ab=C690 cyclic per AB-CYC, c not in N), and the twist index of the C691-composition-factor
## (should be 6, i.e. NOT carrying a would-be order-11-type/large twist -- "does not carry
## chi^11" is read as: the C691 chief factor's twist order is 6, far from 690, so no order-690
## (let alone order-11-divisible-in-the-relevant-sense) character passes through it).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

######################## Object A: G' = SL(2,691) x (C690 x_{C2} S3) ########################
p := 691;;
Fp := GF(p);;
A := [[One(Fp), One(Fp)], [Zero(Fp), One(Fp)]] * One(Fp);;
Bm := [[One(Fp), Zero(Fp)], [-One(Fp), One(Fp)]] * One(Fp);;
A := Immutable(A);; Bm := Immutable(Bm);;

## braid relation check (matrices), independently verified here
lhs := A*Bm*A;;
rhs := Bm*A*Bm;;
braidOk := (lhs = rhs);;
Print("braid relation A*B*A = B*A*B (SL(2,691) rep): ", braidOk, " both = ", lhs, "\n");

cMat := (A*Bm*A)^2;;
negI := (-One(Fp)) * IdentityMat(2, Fp);;
cIsNegI := (cMat = negI);;
Print("c = (sigma1 sigma2 sigma1)^2 -> ", cMat, " ; equals -I: ", cIsNegI, "\n");

## SL(2,691) as GAP's own recognized classical-group object (fast structural algorithms, NOT
## full BSGS on a hand-built matrix group -- an EARLIER version of this script instead computed
## Size(Group(A,B)) directly, which does NOT get classical-group recognition hints and was
## measured to take >10 minutes without completing (killed; CPU climbing steadily = genuine slow
## generic Schreier-Sims, not a hang) -- DROPPED as not one of the "5 points" actually requested
## (S3 surjection/pattern/N<=PB3/c not in N/e=690); A,B generating the FULL SL(2,691) (not a
## proper subgroup) is cited here as the CLASSICAL fact that this specific matrix pair (the
## standard B3->SL(2,Z) generators, reduced mod a prime) generates SL(2,Z/pZ) for all primes p
## (strong approximation / well-known surjectivity of the mod-p reduction of SL(2,Z) -- NOT
## independently re-verified via full group-order computation in this script; disclosed, not
## silently assumed as a NEW machine-checked fact).
SL2p := SL(2, p);;
sl2pOrder := Size(SL2p);;  # fast: GAP's classical-group Size is the closed-form q(q-1)(q+1), not enumeration
sl2IsPerfect := IsPerfect(SL2p);;
Print("|SL(2,691)| [formula] = ", sl2pOrder, " IsPerfect(SL(2,691)) [canonical GAP object] = ", sl2IsPerfect, "\n");

## C690 (writhe/parity map): sigma_i |-> 1 in C690 (Z/690)
## S3 factor: sigma_i |-> standard transpositions, SAME convention as this project's other
## scripts (search/hcen_ab_v1.g's S3can/(1,2),(2,3))
S3can := SymmetricGroup(3);;
s1_S3 := (1,2);;  s2_S3 := (2,3);;
s3SurjOk := (Group(s1_S3, s2_S3) = S3can);;
Print("S3-coordinate generates S3 (surjection check): ", s3SurjOk, "\n");

## pattern check: parity of C690-image (both sigma_i map to 1 mod 690, i.e. ODD parity: 1 mod 2=1)
## vs sign of S3-image (both transpositions, ODD permutations, SignPerm=-1 i.e. "1" in C2-additive)
c690Parity_s1 := 1 mod 2;;  c690Parity_s2 := 1 mod 2;;
s3Sign_s1 := (SignPerm(s1_S3) = -1);;  # true = odd
s3Sign_s2 := (SignPerm(s2_S3) = -1);;
patternOk := (c690Parity_s1 = 1) and (c690Parity_s2 = 1) and s3Sign_s1 and s3Sign_s2;;
Print("pattern (C2-gluing compatibility, both generators odd/odd in both factors): ", patternOk, "\n");

## N<=PB3: the S3-coordinate map is literally the standard map; c-nontriviality in S3-coordinate
## is separately NOT required (c IS in PB3's ambient sense: c maps to identity permutation under
## the standard B3->S3 map always, since c=(s1 s2 s1)^2 is central and PB3-membership is about
## the S3 map specifically, not G' as a whole) -- what matters for "N<=PB3" is that ker(B3->G')
## is a subset of ker(B3->S3can) via THIS S3-coordinate, which holds automatically by
## construction (same generators-to-transpositions map). Recorded as a structural fact, not a
## separate numeric check.
nLeqPB3_structural := s3SurjOk;;  # the S3-coordinate literally equals the standard map -> N<=PB3 automatic

## c not in N: c's SL(2,691)-coordinate alone (-I) already shows c's full image in G' is
## nontrivial (nonidentity in the product), hence c is NOT in N=ker(B3->G')
## c's SL(2,691)-coordinate is -I; since -I <> I for p=691>2, cIsNegI=true directly implies
## the coordinate (hence the full triple) is nontrivial -- c not in N=ker(B3->G')
cNotInN := cIsNegI and (negI <> IdentityMat(2,Fp));;
Print("c not in N (SL(2,691)-coordinate alone nontrivial): ", cNotInN, "\n");

## e=690 (G'^ab=C690): H := C690 x_{C2} S3 built directly (order 2070), AbelianInvariants(H)
## computed exactly; SL(2,691) contributes nothing (perfect, checked above)
C690grp := CyclicGroup(690);;
genC690 := GeneratorsOfGroup(C690grp)[1];;
## fiber product H = {(a,b) in C690 x S3 : (exponent of a mod 2) = (sign of b, as 0/1)}
## build via explicit subgroup of DirectProduct(C690grp, S3can), filtering by the matching condition
DP := DirectProduct(C690grp, S3can);;
embed1 := Embedding(DP, 1);;
embed2 := Embedding(DP, 2);;
## Robust construction: H built directly as a subgroup via explicit enumeration of matching
## (a,b) pairs (parity of a's exponent mod 2 = sign-bit of b), small enough (690*6=4140 pair
## checks) to be cheap and unambiguous.
## generic discrete-log-by-table helper for an ABSTRACT cyclic group (LogFFE only applies to
## finite-field multiplicative elements, not general group elements -- this was a bug, caught
## via a GHA... no, a LOCAL run failure: "Error, no 1st choice method found for LogFFE" -- fixed
## here by building an explicit lookup table via repeated multiplication, cheap for |G|<=690).
BuildDiscreteLogTable := function(g, ord)
  local tbl, cur, i;
  tbl := NewDictionary(g, true);
  cur := One(g);
  for i in [0..ord-1] do
    AddDictionary(tbl, cur, i);
    cur := cur * g;
  od;
  return tbl;
end;;

C690elts := Elements(C690grp);;
c690LogTbl := BuildDiscreteLogTable(genC690, 690);;
ParityOfC690Elt := function(x)
  local e;
  e := LookupDictionary(c690LogTbl, x);
  if e = fail then Error("discrete log lookup failed for C690 element ", x); fi;
  return e mod 2;
end;;
SignBitOfS3Elt := function(b)
  if SignPerm(b) = 1 then return 0; else return 1; fi;
end;;
## Build H directly: H = { DP-element from (a,b) : ParityOfC690Elt(a) = SignBitOfS3Elt(b) }
## Count matching pairs directly (list length, no group theory -- this is just verifying the
## FIBER PRODUCT's expected cardinality, not constructing a group object from all of them).
## *** PERFORMANCE FIX ***: an earlier version of this script built H := Group(Hlist) using ALL
## ~2070 matching pairs as generators (one per element!) -- this caused DerivedSubgroup(H) (and
## other operations) to iterate ~2070^2 ~ 4.3M generator-pair commutators, measured to run
## >20 minutes without completing (killed; CPU climbing steadily = genuine O(n^2) slowness, not
## a hang). Fixed here: H is built from a MINIMAL 2-element generating set instead, with the
## full enumeration retained only as a cheap LIST-LENGTH sanity check (no group operations on
## the full list).
matchCount := 0;;
for a in C690elts do
  for b in Elements(S3can) do
    if ParityOfC690Elt(a) = SignBitOfS3Elt(b) then
      matchCount := matchCount + 1;
    fi;
  od;
od;
hOrderExpected := 690*6/2;;
matchCountOk := (matchCount = hOrderExpected);;
Print("matching-pair count (fiber product cardinality check) = ", matchCount,
      " expected ", hOrderExpected, " ok=", matchCountOk, "\n");

## minimal 2-generator construction: g1=(genC690,transposition) [both odd], g2=(1,3-cycle) [both even]
Hg1 := Image(embed1, genC690) * Image(embed2, s1_S3);;
Hg2 := Image(embed2, s1_S3*s2_S3);;   # (1,2)*(2,3) = a 3-cycle, even permutation
H := Group(Hg1, Hg2);;
hOrder := Size(H);;
hOrderOk := (hOrder = hOrderExpected);;
Print("|H| = ", hOrder, " expected ", hOrderExpected, " ok=", hOrderOk, "\n");

hAbInv := AbelianInvariants(H);;
hAbProduct := Product(hAbInv, x->x, 1);;
hAbIsC690 := (Length(hAbInv) = 1) and (hAbProduct = 690);;
# more careful cyclic check (avoid the earlier length<=1 bug): use IsCyclic on H/[H,H]
Hab := H / DerivedSubgroup(H);;
hAbIsCyclicTrue := IsCyclic(Hab);;
hAbOrder := Size(Hab);;
eIs690 := hAbIsCyclicTrue and (hAbOrder = 690);;
Print("H^ab: invariants=", hAbInv, " order=", hAbOrder, " is_cyclic=", hAbIsCyclicTrue, " e=690: ", eIs690, "\n");

gPrimeAbEquals690 := sl2IsPerfect and eIs690;;
Print("G' = SL(2,691) x H, G'^ab = H^ab (SL2 perfect): e(G')=690 confirmed: ", gPrimeAbEquals690, "\n");

xd1_objA := rec(
  braid_relation_ok := braidOk,
  c_maps_to_negI := cIsNegI,
  sl2_691_order := sl2pOrder,
  sl2_691_full_generation_note := "NOT independently re-verified via group-order computation in this script (dropped -- see script comment); cited as the classical fact that the standard B3->SL(2,Z) generators, reduced mod any prime p, generate SL(2,Z/pZ)",
  sl2_691_is_perfect := sl2IsPerfect,
  s3_surjection_ok := s3SurjOk,
  pattern_c2_gluing_ok := patternOk,
  n_leq_pb3_structural := nLeqPB3_structural,
  c_not_in_N := cNotInN,
  H_order := hOrder,
  H_order_expected := hOrderExpected,
  H_order_ok := hOrderOk,
  H_abelianization_order := hAbOrder,
  H_abelianization_is_cyclic := hAbIsCyclicTrue,
  e_equals_690 := gPrimeAbEquals690
);;

######################## Object B: G0 = (C691 : (C6 x_{C2} S3)) x C115 ########################
## Build the small fiber product K := C6 x_{C2} S3 (order 18) directly, same method as H above.
C6grp := CyclicGroup(6);;
genC6 := GeneratorsOfGroup(C6grp)[1];;
C6elts := Elements(C6grp);;
c6LogTbl := BuildDiscreteLogTable(genC6, 6);;
ParityOfC6Elt := function(x)
  local e;
  e := LookupDictionary(c6LogTbl, x);
  if e = fail then Error("discrete log lookup failed for C6 element ", x); fi;
  return e mod 2;
end;;
DPK := DirectProduct(C6grp, S3can);;
embedK1 := Embedding(DPK, 1);;
embedK2 := Embedding(DPK, 2);;
Klist := [];;
for a in C6elts do
  for b in Elements(S3can) do
    if ParityOfC6Elt(a) = SignBitOfS3Elt(b) then
      Add(Klist, Image(embedK1,a)*Image(embedK2,b));
    fi;
  od;
od;
Kgrp := Group(Klist);;
kOrder := Size(Kgrp);;
kOrderExpected := 6*6/2;;
kOrderOk := (kOrder = kOrderExpected);;
Print("|K|=|C6 x_C2 S3| = ", kOrder, " expected ", kOrderExpected, " ok=", kOrderOk, "\n");

## natural projection pi: K -> C6 (first coordinate), checked surjective
piK := Projection(DPK, 1);;
piKimages := List(Klist, x -> Image(piK, x));;
piKimageGrp := Group(piKimages);;
piSurjOk := (Size(piKimageGrp) = 6);;
Print("pi: K -> C6 (first-coordinate projection) surjective: ", piSurjOk, " (image size=", Size(piKimageGrp), ")\n");

## embedding C6 -> Aut(C691) = (Z/691)^* order 690, via a primitive root g mod 691, order-6
## element = g^115 (690/6=115)
g := PrimitiveRootMod(691);;
zeta6 := PowerModInt(g, 115, 691);;
zeta6OrderOk := (OrderMod(zeta6, 691) = 6);;
Print("primitive root g mod 691 = ", g, " ; zeta6 = g^115 mod 691 = ", zeta6, " order(zeta6)=6: ", zeta6OrderOk, "\n");

## build G0 as an explicit finite group via semidirect product: N0 := C691 (additive, as
## Integers mod 691 under +), acted on by K via K -> C6 -> Aut(C691) (k |-> mult by
## zeta6^{pi(k) mod 6}, where pi(k) in Z/6 is read from piK's image identified with Z/6).
## Then G0 := (N0 : K) x C115.
## Represent N0:K as a permutation group on 691 points (N0 = Z/691 acting on itself by
## translation... no: for the SEMIDIRECT product N0:K with K acting by automorphisms, build via
## GAP's SemidirectProduct machinery using an explicit homomorphism K -> AutomorphismGroup(N0).
N0 := CyclicGroup(691);;  # additive group of order 691, as an abstract cyclic group
genN0 := GeneratorsOfGroup(N0)[1];;
AutN0 := AutomorphismGroup(N0);;  # should be cyclic of order 690
autN0Order := Size(AutN0);;
Print("|Aut(C691)| = ", autN0Order, " (expect 690)\n");

## identify pi(k) in Z/6 for each element k of K (via the same discrete-log table as C6grp)
ExpOfC6Elt := function(x)
  local e;
  e := LookupDictionary(c6LogTbl, x);
  if e = fail then Error("discrete log lookup failed for C6 element ", x); fi;
  return e;
end;;

## the automorphism of N0 corresponding to multiplication by zeta6^m: find the specific
## automorphism in AutN0 sending genN0 to genN0^(zeta6^m mod 691) -- build directly via
## GroupHomomorphismByImages on N0 (an automorphism of a cyclic group is determined by where
## the generator goes, to another generator/power coprime to 691)
AutFromMultiplier := function(m)
  local scalar, img;
  scalar := PowerModInt(zeta6, m, 691);
  img := genN0^scalar;
  return GroupHomomorphismByImages(N0, N0, [genN0], [img]);
end;;

## action homomorphism K -> AutN0
actionImages := List(Klist, k -> AutFromMultiplier(ExpOfC6Elt(Image(piK,k))));;
actHom := GroupHomomorphismByImages(Kgrp, AutN0, Klist, actionImages);;
actHomOk := (actHom <> fail);;
Print("action homomorphism K -> Aut(C691) constructed: ", actHomOk, "\n");

G0core := SemidirectProduct(Kgrp, actHom, N0);;
g0coreOrder := Size(G0core);;
g0coreExpected := 691*18;;
Print("|C691:K| = ", g0coreOrder, " expected ", g0coreExpected, "\n");

C115grp := CyclicGroup(115);;
G0 := DirectProduct(G0core, C115grp);;
g0Order := Size(G0);;
g0Expected := 691*18*115;;
Print("|G0| = ", g0Order, " expected ", g0Expected, " (card states 1,430,370)\n");

## AB-CYC / e checks: G0^ab
G0ab := G0 / DerivedSubgroup(G0);;
g0AbOrder := Size(G0ab);;
g0AbIsCyclic := IsCyclic(G0ab);;
Print("G0^ab: order=", g0AbOrder, " is_cyclic=", g0AbIsCyclic, "\n");

## both congruences: 345 | j (j:=e/2) and 691 | |G0|
g0AbEven := (g0AbOrder mod 2 = 0);;
jVal := fail;;
jDiv345 := fail;;
if g0AbIsCyclic and g0AbEven then
  jVal := g0AbOrder/2;
  jDiv345 := (jVal mod 345 = 0);
fi;
order691Divides := (g0Order mod 691 = 0);;
Print("congruence 1 (345|j): j=", jVal, " 345|j: ", jDiv345, "\n");
Print("congruence 2 (691||G0|): ", order691Divides, "\n");

## c-image: c=(sigma1 sigma2 sigma1)^2 -- but G0 is NOT itself a B3-image via explicit sigma_i
## generators in this script (the card's construction of G0's B3-realization is not spelled out
## beyond "作用は位数6でB3-実現可能"); the c-NONTRIVIALITY check the card actually specifies is
## structural: "c |-> (1,1,6 mod 115)" in a THREE-coordinate reading (N0-coord, K-coord,
## C115-coord) -- interpreted here as: within THIS script's G0 = (C691:K) x C115 realization,
## the analogous claim is that a central/twist-generating element maps nontrivially into the
## C115 factor. This script does NOT attempt to construct an explicit B3->G0 homomorphism (that
## would require pinning down K's own B3-realization via K's own sigma1/sigma2-images, which the
## card does not specify beyond the abstract group K itself) -- DISCLOSED GAP, not measured here.

## twist index of the C691 chief factor: by construction, K acts on N0=C691 through the order-6
## multiplier zeta6 -- the twist order (|K / C_K(N0)|, i.e. size of the image of K's action on
## N0) is exactly the order of the multiplier's cyclic image, which is 6 IF the action
## homomorphism K->Aut(N0) has image of order exactly 6 (not smaller) -- checked directly:
actionImageOrder := Size(Image(actHom));;
twistOrderIs6 := (actionImageOrder = 6);;
Print("twist order of the C691 chief factor (|Image(K->Aut(C691))|) = ", actionImageOrder, " equals 6: ", twistOrderIs6, "\n");
doesNotCarryLargeTwist := (actionImageOrder <> 690) and (690 mod actionImageOrder = 0);;
Print("does not carry a large (order-690-class) twist: ", doesNotCarryLargeTwist, "\n");

xd1_objB := rec(
  K_order := kOrder,
  K_order_expected := kOrderExpected,
  K_order_ok := kOrderOk,
  pi_K_to_C6_surjective := piSurjOk,
  zeta6_order_ok := zeta6OrderOk,
  action_hom_constructed := actHomOk,
  G0core_order := g0coreOrder,
  G0core_order_expected := g0coreExpected,
  G0_order := g0Order,
  G0_order_expected := g0Expected,
  G0_ab_order := g0AbOrder,
  G0_ab_is_cyclic := g0AbIsCyclic,
  j := jVal,
  congruence1_345_divides_j := jDiv345,
  congruence2_691_divides_order := order691Divides,
  twist_action_image_order := actionImageOrder,
  twist_order_is_6 := twistOrderIs6,
  does_not_carry_large_twist := doesNotCarryLargeTwist,
  b3_realization_of_G0_note := "NOT constructed/measured in this script (card underspecifies K's own B3-generator images; DISCLOSED GAP, not silently assumed)"
);;

## ============ JSON output ============
out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/xd1_chk_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a811 -- docs/notes/ideas_chi_door_assault_v1.md \\u00a7XD-1 (c5a02ae)\",",
  "\"disclosed_construction_choice_note\":\"Object B (G0)'s action K->Aut(C691) uses the NATURAL first-coordinate projection K=C6x_C2S3->C6 composed with an order-6 embedding into Aut(C691) -- the card's own text ('\\u4f5c\\u7528\\u306f\\u4f4d\\u65706=\\u516d\\u89d2\\u56fa\\u6709\\u5024zeta6\\u7d4c\\u7531\\u3067B3-\\u5b9f\\u73fe\\u53ef\\u80fd') does not pin down the exact quotient map; this is A reasonable choice achieving all named outcome properties, disclosed as a choice not asserted as unique/intended.\",",
  "\"objA_repair_window_G_prime\":{",
    "\"braid_relation_ok\":", JB(xd1_objA.braid_relation_ok), ",",
    "\"c_maps_to_negI\":", JB(xd1_objA.c_maps_to_negI), ",",
    "\"sl2_691_order\":", String(xd1_objA.sl2_691_order), ",",
    "\"sl2_691_full_generation_note\":", JStr(xd1_objA.sl2_691_full_generation_note), ",",
    "\"sl2_691_is_perfect\":", JB(xd1_objA.sl2_691_is_perfect), ",",
    "\"s3_surjection_ok\":", JB(xd1_objA.s3_surjection_ok), ",",
    "\"pattern_c2_gluing_ok\":", JB(xd1_objA.pattern_c2_gluing_ok), ",",
    "\"n_leq_pb3_structural\":", JB(xd1_objA.n_leq_pb3_structural), ",",
    "\"c_not_in_N\":", JB(xd1_objA.c_not_in_N), ",",
    "\"H_order\":", String(xd1_objA.H_order), ",",
    "\"H_order_expected\":", String(xd1_objA.H_order_expected), ",",
    "\"H_order_ok\":", JB(xd1_objA.H_order_ok), ",",
    "\"H_abelianization_order\":", String(xd1_objA.H_abelianization_order), ",",
    "\"H_abelianization_is_cyclic\":", JB(xd1_objA.H_abelianization_is_cyclic), ",",
    "\"e_equals_690\":", JB(xd1_objA.e_equals_690),
  "},",
  "\"objB_empty_carrier_G0\":{",
    "\"K_order\":", String(xd1_objB.K_order), ",",
    "\"K_order_expected\":", String(xd1_objB.K_order_expected), ",",
    "\"K_order_ok\":", JB(xd1_objB.K_order_ok), ",",
    "\"pi_K_to_C6_surjective\":", JB(xd1_objB.pi_K_to_C6_surjective), ",",
    "\"zeta6_order_ok\":", JB(xd1_objB.zeta6_order_ok), ",",
    "\"action_hom_constructed\":", JB(xd1_objB.action_hom_constructed), ",",
    "\"G0core_order\":", String(xd1_objB.G0core_order), ",",
    "\"G0core_order_expected\":", String(xd1_objB.G0core_order_expected), ",",
    "\"G0_order\":", String(xd1_objB.G0_order), ",",
    "\"G0_order_expected\":", String(xd1_objB.G0_order_expected), ",",
    "\"G0_ab_order\":", String(xd1_objB.G0_ab_order), ",",
    "\"G0_ab_is_cyclic\":", JB(xd1_objB.G0_ab_is_cyclic), ",",
    "\"j\":", String(xd1_objB.j), ",",
    "\"congruence1_345_divides_j\":", JB(xd1_objB.congruence1_345_divides_j), ",",
    "\"congruence2_691_divides_order\":", JB(xd1_objB.congruence2_691_divides_order), ",",
    "\"twist_action_image_order\":", String(xd1_objB.twist_action_image_order), ",",
    "\"twist_order_is_6\":", JB(xd1_objB.twist_order_is_6), ",",
    "\"does_not_carry_large_twist\":", JB(xd1_objB.does_not_carry_large_twist), ",",
    "\"b3_realization_of_G0_note\":", JStr(xd1_objB.b3_realization_of_G0_note),
  "},",
  "\"no_verdict_note\":\"raw structural/numeric checks and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/xd1_chk_v1_20260811.json", out);;
Print("Wrote search/certs/xd1_chk_v1_20260811.json\n");
Print("XD1_CHK_DONE\n");
QUIT;
