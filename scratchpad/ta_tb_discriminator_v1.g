#############################################################################
## ta_tb_discriminator_v1.g -- mathematician (Opus 5), 2026-08-30
## Q: does the G-1 finding ("conjugate only after inverting all three")
##    discriminate T-a (positional reversal) from T-b (inversion), and does
##    the distinction even SURVIVE for our (9,9,9) target?
## Gates:
##  (1) are all PSL(2,8) classes REAL (g ~ g^-1)?  [then cycle types cannot
##      separate inversion, and only SIMULTANEOUS conjugacy can]
##  (2) for OUR target triple (X,Y,Z), Z=(XY)^-1 :
##       (2a) is (X^-1,Y^-1,Z^-1) simultaneously S9-conjugate to (X,Y,Z)?
##       (2b) is the REVERSED triple (Z,Y,X) simultaneously S9-conjugate?
##      If (2a)=true the T-b ambiguity COLLAPSES for the target (moot).
##      If (2a)=false the pilot's answer is load-bearing.
##  (3) same two questions for the PILOT passport (7,2,3) -- where cycle
##      types already separate reversal.
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;
G := Group(DCP2X4, DCP2Y4);; S9 := SymmetricGroup(9);;
CT := function(p) return SortedList(List(Orbits(Group(p),[1..9]),Length)); end;;

Print("TT_GROUP_ORDER ", Size(G), "\n");
## (1) reality of all classes
cc := ConjugacyClasses(G);;
Print("TT_ALL_CLASSES_REAL ",
  ForAll(cc, c -> Representative(c)^-1 in c), "\n");
for c in cc do
  Print("   ord=", Order(Representative(c)), " size=", Size(c),
        " real=", Representative(c)^-1 in c, "\n");
od;

## (2) our (9,9,9) target
TX := DCP2X4;; TY := DCP2Y4;; TZ := (TX*TY)^-1;;
Print("\nTT_TARGET_TYPES ", [CT(TX),CT(TY),CT(TZ)], "  product_XYZ_is_id ", TX*TY*TZ = (), "\n");
inv := RepresentativeAction(S9, [TX^-1, TY^-1], [TX, TY], OnPairs);;
rev := RepresentativeAction(S9, [TZ, TY], [TX, TY], OnPairs);;
Print("TT_TARGET_INVERSE_CONJUGATE ", inv <> fail, "\n");
Print("TT_TARGET_REVERSED_CONJUGATE ", rev <> fail, "\n");
## also: reversed-and-inverted
ri := RepresentativeAction(S9, [TZ^-1, TY^-1], [TX, TY], OnPairs);;
Print("TT_TARGET_REV_AND_INV_CONJUGATE ", ri <> fail, "\n");

## (3) pilot passport (7,2,3): build ONE such triple inside G and ask the same
nine7 := Filtered(Elements(G), g -> Order(g) = 7);;
two   := Filtered(Elements(G), g -> Order(g) = 2);;
pil := fail;;
for a in nine7 do
  for b in two do
    if Order(a*b) = 3 then pil := [a,b]; break; fi;
  od;
  if pil <> fail then break; fi;
od;
if pil = fail then Print("TT_PILOT_NOT_FOUND\n"); else
  a := pil[1];; b := pil[2];; c := (a*b)^-1;;
  Print("\nTT_PILOT_TYPES ", [CT(a),CT(b),CT(c)], "  product ", a*b*c = (), "\n");
  Print("TT_PILOT_INVERSE_CONJUGATE ",
        RepresentativeAction(S9,[a^-1,b^-1],[a,b],OnPairs) <> fail, "\n");
  Print("TT_PILOT_REVERSED_TYPES_MATCH ", CT(c) = CT(a), "\n");
  Print("TT_PILOT_GENERATES ", Group(a,b) = G, "\n");
fi;
Print("\nTT_DONE\n");
QUIT;
