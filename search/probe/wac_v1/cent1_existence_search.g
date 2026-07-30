#############################################################################
## search/probe/wac_v1/cent1_existence_search.g
## n=10 judgement-window existence search (裁定238 工程1).  Search for
## realization pairs (a1,b1) in S10 with:
##   a1^2 = 1, cycle type (2,2,2,2,1,1)  [k=4 transpositions, 2 fixed points]
##   b1^3 = 1, cycle type (3,3,3,1)      [j=3 3-cycles, 1 fixed point]
##   w := b1^-1 * a1  has cycle type (5,5)  [no 2*ell-cycle]
##   sign(a1) = +1  (=> <a1,b1> subset A10 branch)
## and assert <a1,b1> = A10 (order 10!/2 = 1814400).
##
## Method (mirrors search/probe/wac_v1/r4_existence_search.g): fix a single
## representative w0 of the target w-type (5,5).  Since w = b1^-1*a1 =>
## b1 = a1*w0^-1, and every pair (a1,b1) with w of type (5,5) is conjugate
## (by transitivity of S10 on the (5,5) conjugacy class) to a pair with
## w = w0 exactly, scanning a1 over the FULL conjugacy class of the target
## a1-type and setting b1 := a1*w0^-1 is exhaustive up to simultaneous
## conjugation -- no representative pair is missed.
##
## Bonus: classify hits by orbits of a1 under conjugation by C_S10(w0)
## (centralizer of w0).  Since b1 = a1*w0^-1 and g in C_S10(w0) satisfies
## (a1*w0^-1)^g = a1^g * w0^-1, conjugating a1 by g in C_S10(w0) carries a
## whole hit-pair to another hit-pair with the SAME w0 -- these orbits are
## a legitimate coarsening of the raw hit list (counted only, not
## interpreted).
##
## Single lane (GAP 4.16.0).  NOT a ledger claim.  No commit.  No sealed
## symbol.  Existence search only -- no judgement, no interpretation.
## No expected/predicted values are encoded anywhere in this script
## (contact isolation).
#############################################################################

n := 10;;
Sn := SymmetricGroup(n);; An := AlternatingGroup(n);;

CT := function(p) return SortedList(List(Orbits(Group(p),[1..n]), Length)); end;;

Print("#########################################################\n");
Print("## STEP 0  fix target w0 (type (5,5)) and a1-class representative\n");
Print("#########################################################\n");

w0 := PermList([2,3,4,5,1, 7,8,9,10,6]);;   ## (1,2,3,4,5)(6,7,8,9,10)
a0 := (1,2)(3,4)(5,6)(7,8);;                 ## (2,2,2,2,1,1); fixed pts 9,10

Print("w0       = ", w0, "\n");
Print("w0 type  = ", CT(w0), "  sign(w0) = ", SignPerm(w0), "  ord(w0) = ", Order(w0), "\n");
Print("a0       = ", a0, "\n");
Print("a0 type  = ", CT(a0), "  sign(a0) = ", SignPerm(a0), "  ord(a0) = ", Order(a0), "\n");

a1classSize := Size(ConjugacyClass(Sn, a0));;
Print("|a1-class (type (2,2,2,2,1,1))| = ", a1classSize, "\n");

Print("\n#########################################################\n");
Print("## STEP 1  exhaustive scan: a1 over full conjugacy class of a0,\n");
Print("##         b1 := a1*w0^-1, keep hits with b1 type (3,3,3,1)\n");
Print("#########################################################\n");

targetBType := [1,3,3,3];;
EXHAUST_THRESH := 1000000;;

t0 := Runtime();;
aClassList := AsList(ConjugacyClass(Sn, a0));;
Print("class enumerated: ", Length(aClassList), " elements  (", (Runtime()-t0)/1000.0, "s)\n");

hits := [];;
tries := 0;; bTypeHits := 0;;
t0 := Runtime();;
for a1 in aClassList do
  tries := tries + 1;
  b1 := a1 * w0^-1;
  if CT(b1) = targetBType then
    bTypeHits := bTypeHits + 1;
    Add(hits, rec(a1:=a1, b1:=b1));
  fi;
od;
Print("tries=", tries, "  b1-type=(3,3,3,1) hits=", bTypeHits,
      "  elapsed=", (Runtime()-t0)/1000.0, "s\n");

Print("\n#########################################################\n");
Print("## STEP 2  among b1-type hits, check generation <a1,b1> = A10\n");
Print("#########################################################\n");

genHits := [];;
t0 := Runtime();;
for h in hits do
  G := Group(h.a1, h.b1);
  if Size(G) = Size(An) and G = An then
    Add(genHits, rec(a1:=h.a1, b1:=h.b1, w:=h.b1^-1*h.a1, gen:="A10", sizeG:=Size(G)));
  elif Size(G) = Size(Sn) and G = Sn then
    Add(genHits, rec(a1:=h.a1, b1:=h.b1, w:=h.b1^-1*h.a1, gen:="S10", sizeG:=Size(G)));
  else
    Add(genHits, rec(a1:=h.a1, b1:=h.b1, w:=h.b1^-1*h.a1, gen:="other", sizeG:=Size(G)));
  fi;
od;
Print("generation check done  elapsed=", (Runtime()-t0)/1000.0, "s\n");

realizationHits := Filtered(genHits, r -> r.gen = "A10");;
Print("realization pairs with <a1,b1> = A10 : ", Length(realizationHits), "\n");
Print("all genHits by category: A10=", Length(Filtered(genHits, r->r.gen="A10")),
      "  S10=", Length(Filtered(genHits, r->r.gen="S10")),
      "  other=", Length(Filtered(genHits, r->r.gen="other")), "\n");
otherSizes := SortedList(DuplicateFreeList(List(Filtered(genHits, r->r.gen="other"), r->r.sizeG)));;
Print("distinct |<a1,b1>| among 'other' hits = ", otherSizes, "\n");
for sz in otherSizes do
  Print("   |<a1,b1>|=", sz, "  count=",
        Length(Filtered(genHits, r -> r.gen="other" and r.sizeG=sz)), "\n");
od;
if Length(genHits) > 0 then
  Print("-- first 5 'other' hits, full data --\n");
  otherHits := Filtered(genHits, r->r.gen="other");;
  for i in [1..Minimum(5,Length(otherHits))] do
    r := otherHits[i];
    Print("   a1=", r.a1, "  b1=", r.b1, "  w=", r.w, "  |<a1,b1>|=", r.sizeG, "\n");
  od;
fi;

Print("\n#########################################################\n");
Print("## STEP 3  sanity re-checks on realization hits (first up to 10)\n");
Print("#########################################################\n");
showN := Minimum(10, Length(realizationHits));;
for i in [1..showN] do
  r := realizationHits[i];
  Print("-- hit ", i, "\n");
  Print("   a1 = ", r.a1, "  type=", CT(r.a1), "  sign=", SignPerm(r.a1), "  ord=", Order(r.a1), "\n");
  Print("   b1 = ", r.b1, "  type=", CT(r.b1), "  sign=", SignPerm(r.b1), "  ord=", Order(r.b1), "\n");
  Print("   w  = b1^-1*a1 = ", r.w, "  type=", CT(r.w), "  ord=", Order(r.w), "\n");
  Print("   <a1,b1> order = ", r.sizeG, "  = A10 order? ", r.sizeG = Size(An), "\n");
od;

Print("\n#########################################################\n");
Print("## STEP 4  orbit classification of realization hits under\n");
Print("##         C_S10(w0)-conjugation on a1 (bonus; counts only)\n");
Print("#########################################################\n");
Cw0 := Centralizer(Sn, w0);;
Print("|C_S10(w0)| = ", Size(Cw0), "\n");
if Length(realizationHits) > 0 then
  aList := List(realizationHits, r -> r.a1);;
  orbs := Orbits(Cw0, aList, OnPoints);;
  Print("realization-hit orbit count under C_S10(w0)-conjugation on a1 = ", Length(orbs), "\n");
  for i in [1..Length(orbs)] do
    Print("   orbit ", i, ": size=", Length(orbs[i]), "\n");
  od;
else
  Print("no realization hits -- orbit classification vacuous (0 orbits)\n");
fi;

Print("\n#########################################################\n");
Print("## SUMMARY\n");
Print("#########################################################\n");
Print("a1-class size (2,2,2,2,1,1)         = ", a1classSize, "\n");
Print("scanned (tries)                      = ", tries, "  (EXHAUSTIVE, tries=class size: ",
      tries = a1classSize, ")\n");
Print("b1-type=(3,3,3,1) hits                = ", bTypeHits, "\n");
Print("generation=A10 hits (realization)     = ", Length(realizationHits), "\n");
Print("generation=S10 hits                   = ", Length(Filtered(genHits, r->r.gen="S10")), "\n");
Print("generation=other hits                 = ", Length(Filtered(genHits, r->r.gen="other")), "\n");
if Length(realizationHits) > 0 then
  Print("orbit count under C_S10(w0)            = ", Length(Orbits(Cw0, List(realizationHits, r->r.a1), OnPoints)), "\n");
fi;
Print("exists_realization_pair                = ", Length(realizationHits) > 0, "\n");

Print("\nCENT1_EXISTENCE_SEARCH_DONE\n");
QUIT;
